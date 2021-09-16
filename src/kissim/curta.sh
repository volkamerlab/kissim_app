#!/bin/bash
#SBATCH --job-name=kissim_app
#SBATCH --mail-user=dominique.sydow@fu-berlin.de
#SBATCH --mail-type=begin,end
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --mem-per-cpu=4096
#SBATCH --qos=standard

# @dominiquesydow
# Encode structures and compare fingerprints on the curta cluster using the kissim package

# Usage
# -----
# sbatch --time=10:00:00 
#   curta.sh 
#       <run ID = output folder name> 
#       <Structure subset [all, dfg_in , dfg_out, test]> 
#       <KLIFS download folder name>
#       <Normalize fingerprint? [normalized, unnormalized]>
#       <Subset fingerprint? [subset, full]>
#
# Example
# -------
# sbatch --time=10:00:00 curta.sh 20210804 dfg_in 20210902_KLIFS_HUMAN normalized full

conda list kissim

ID=$1
STRUCTURE_SUBSET=$2
KLIFS_DOWNLOAD=$3
NORMALIZE=$4
SUBSET=$5

KISSIM_APP=/home/${USER}/kissim_app
#KISSIM_APP=/home/${USER}/Documents/GitHub/kissim_app
RESULTS=$KISSIM_APP/results/${ID}/${STRUCTURE_SUBSET}
# If you change this number, make sure to change it also in the SBATCH comments
NCORES=8

echo "Job settings"
echo "------------" 
echo "Run ID:" $1 
echo "Structure subset:" $2 
echo "KLIFS download folder:" $3 
echo "Normalized?" $4
echo "Residue subset?" $5

if [[ $4 != normalized ]] && [[ $4 != unnormalized ]]
then
    echo "Normalization parameter can be: normalized, unnormalized - cannot be "$4
    exit 1
fi

if [[ $5 != subset ]] && [[ $5 != full ]]
then
    echo "Subset parameter can be: subset, full - cannot be "$5
    exit 1
fi

mkdir -p $RESULTS

# Encode structures
kissim encode -i $KISSIM_APP/data/processed/structure_klifs_ids_${STRUCTURE_SUBSET}.txt -o $RESULTS/fingerprints.json -c $NCORES -l $KISSIM_APP/data/external/structures/$KLIFS_DOWNLOAD
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
if [ $SUBSET == "subset" ]
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

# Weight features
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_100.csv -w 0.125 0.125 0.125 0.125 0.125 0.125 0.125 0.125 0 0 0 0 0 0 0 
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_010.csv -w 0 0 0 0 0 0 0 0 0.25 0.25 0.25 0.25 0 0 0
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_001.csv -w 0 0 0 0 0 0 0 0 0 0 0 0 0.333 0.333 0.333
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_110.csv -w 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.125 0.125 0.125 0.125 0 0 0
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_101.csv -w 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0 0 0 0 0.166 0.166 0.166
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_011.csv -w 0 0 0 0 0 0 0 0 0.125 0.125 0.125 0.125 0.166 0.166 0.166
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_111.csv -w 0.041 0.041 0.041 0.041 0.041 0.041 0.041 0.041 0.083 0.083 0.083 0.083 0.111 0.111 0.111 

# Zip results
cd $RESULTS/..
zip -r ${STRUCTURE_SUBSET}.zip ${STRUCTURE_SUBSET}
