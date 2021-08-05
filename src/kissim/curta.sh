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
#       <Normalize? [normalized - or leave black]>
#
# Example
# -------
# Use normalization:
# sbatch --time=10:00:00 curta.sh 20210804 dfg_in 20210630_KLIFS_HUMAN normalized
# Do not use normalization:
# sbatch --time=10:00:00 curta.sh 20210804 dfg_in 20210630_KLIFS_HUMAN

ID=$1
STRUCTURE_SUBSET=$2
KLIFS_DOWNLOAD=$3
NORMALIZE=${4:-unnormalized}
RESULTS=$KISSIM_APP/results/${ID}/${STRUCTURE_SUBSET}
# If you change this number, make sure to change it also in the SBATCH comments
NCORES=8

echo "Job settings"
echo "------------" 
echo "Run ID:" $1 
echo "Structure subset:" $2 
echo "KLIFS download folder:" $3 
echo "Normalized?" $4

mkdir -p $RESULTS

# Encode structures
kissim encode -i $KISSIM_APP/data/processed/structure_klifs_ids_${STRUCTURE_SUBSET}.txt -o $RESULTS/fingerprints.json -c $NCORES -l $KISSIM_APP/data/external/structures/$KLIFS_DOWNLOAD

# Remove structural outliers
kissim outliers -i $RESULTS/fingerprints.json -d 34 -o $RESULTS/fingerprints_clean.json

# Normalize fingerprints
if [ $NORMALIZE == "normalized" ]
then
    echo "Normalize fingerprints..."
    python normalize_fp.py $RESULTS/fingerprints.json $RESULTS/fingerprints_normalized.json
    FILENAME_FINGERPRINT=fingerprints_normalized.json
else
    FILENAME_FINGERPRINT=fingerprints_clean.json
fi
echo $FILENAME_FINGERPRINT

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
