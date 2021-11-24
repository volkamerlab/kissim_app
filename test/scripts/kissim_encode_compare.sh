#!/bin/bash
#SBATCH --job-name=kissim_app
#SBATCH --mail-user=dominique.sydow@fu-berlin.de
#SBATCH --mail-type=begin,end
#SBATCH --nodes=1
#SBATCH --qos=standard

# @dominiquesydow
# Encode structures and compare fingerprints on the curta cluster using the kissim package

# Usage
# -----
# sbatch --time=10:00:00 --ntasks=8 --mem-per-cpu=4096
#   kissim_encode_compare.sh 
#       <Structure subset [all, dfg_in , dfg_out, test]> 
#       <KLIFS download folder name>
#       <Normalize fingerprint? [normalized, unnormalized]>
#       <Subset fingerprint? [subset, full]>
#
# Example
# -------
# sbatch --time=10:00:00 --ntasks=8 --mem-per-cpu=4096 
#   kissim_encode_compare.sh 
#       dfg_in 
#       20210902_KLIFS_HUMAN
#       normalized 
#       full

conda list kissim

STRUCTURE_SUBSET=$1
KLIFS_DOWNLOAD=$2
NORMALIZE=$3
RESIDUE_SUBSET=$4

#KISSIM_APP=/home/${USER}/kissim_app
KISSIM_APP=/home/${USER}/Documents/GitHub/kissim_app
RESULTS=$KISSIM_APP/test/results/${STRUCTURE_SUBSET}
# If you change this number, make sure to change it also in the SBATCH comments
NCORES=8

echo "Job settings"
echo "------------" 
echo "Structure subset:" $STRUCTURE_SUBSET
echo "KLIFS download folder:" $KLIFS_DOWNLOAD
echo "Normalized?" $NORMALIZE
echo "Residue subset?" $RESIDUE_SUBSET

if [[ $NORMALIZE != normalized ]] && [[ $NORMALIZE != unnormalized ]]
then
    echo "Normalization parameter can be: normalized, unnormalized - cannot be "$4
    exit 1
fi

if [[ $RESIDUE_SUBSET != subset ]] && [[ $RESIDUE_SUBSET != full ]]
then
    echo "Subset parameter can be: subset, full - cannot be "$5
    exit 1
fi

mkdir -p $RESULTS

# Encode structures
kissim encode -i $KISSIM_APP/test/data/processed/structure_klifs_ids_${STRUCTURE_SUBSET}.txt -o $RESULTS/fingerprints.json -c $NCORES -l $KISSIM_APP/test/data/external/$KLIFS_DOWNLOAD
FILENAME_FINGERPRINT=fingerprints.json
echo "Fingerprints used for next step: "$FILENAME_FINGERPRINT

# Remove structural outliers
kissim outliers -i $RESULTS/$FILENAME_FINGERPRINT -d 34 -o $RESULTS/fingerprints_clean.json
FILENAME_FINGERPRINT=fingerprints_clean.json
echo "Fingerprints used for next step: "$FILENAME_FINGERPRINT

# Optional: Normalize fingerprints
if [ $NORMALIZE == "normalized" ]
then
    echo "Normalize fingerprints..."
    kissim normalize -i $RESULTS/$FILENAME_FINGERPRINT -o $RESULTS/fingerprints_normalized.json -f
    FILENAME_FINGERPRINT=fingerprints_normalized.json
else
    echo "Do not normalize fingerprints - carry on..."
fi
echo "Fingerprints used for next step: "$FILENAME_FINGERPRINT

# Optional: Subset fingerprints
if [ $RESIDUE_SUBSET == "subset" ]
then
    echo "Subset fingerprints..."
    kissim subset -i $RESULTS/$FILENAME_FINGERPRINT -o $RESULTS/fingerprints_subset.json -s $2
    FILENAME_FINGERPRINT=fingerprints_subset.json
else
    echo "Do not subset fingerprints - carry on..."
fi
echo "Fingerprints used for next step: "$FILENAME_FINGERPRINT

# Compare fingerprints
kissim compare -i $RESULTS/$FILENAME_FINGERPRINT -o $RESULTS -c $NCORES
