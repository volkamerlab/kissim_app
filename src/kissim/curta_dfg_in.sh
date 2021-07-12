#!/bin/bash
#SBATCH --job-name=kissim_app
#SBATCH --mail-user=dominique.sydow@fu-berlin.de
#SBATCH --mail-type=begin,end
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --mem-per-cpu=4096
#SBATCH --time=10:00:00
#SBATCH --qos=standard

# @dominiquesydow
# Encode structures and compare fingerprints on the curta cluster using the kissim package

DFG="in"
ID="20210712"
KLIFS_DOWNLOAD=20210630_KLIFS_HUMAN
KISSIM_APP=/home/${USER}/kissim_app
RESULTS=$KISSIM_APP/results/${ID}/dfg_${DFG}
NCORES=8

mkdir -R $RESULTS

# Encode structures
kissim encode -i $KISSIM_APP/data/processed/structure_klifs_ids_dfg_${DFG}.txt -o $RESULTS/fingerprints.json -c $NCORES -l $KISSIM_APP/data/external/structures/$KLIFS_DOWNLOAD

# Remove structural outliers
kissim outliers -i $RESULTS/fingerprints.json -d 34 -o $RESULTS/fingerprints_clean.json

# Compare fingerprints
kissim compare -i $RESULTS/fingerprints_clean.json -o $RESULTS -c $NCORES

# Weight features
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_100.csv -w 0.125 0.125 0.125 0.125 0.125 0.125 0.125 0.125 0 0 0 0 0 0 0 
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_010.csv -w 0 0 0 0 0 0 0 0 0.25 0.25 0.25 0.25 0 0 0
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_001.csv -w 0 0 0 0 0 0 0 0 0 0 0 0 0.333 0.333 0.333
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_110.csv -w 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.125 0.125 0.125 0.125 0 0 0
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_101.csv -w 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0 0 0 0 0.166 0.166 0.166
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_011.csv -w 0 0 0 0 0 0 0 0 0.125 0.125 0.125 0.125 0.166 0.166 0.166
kissim weights -i $RESULTS/feature_distances.csv -o $RESULTS/fingerprint_distances_111.csv -w 0.041 0.041 0.041 0.041 0.041 0.041 0.041 0.041 0.083 0.083 0.083 0.083 0.111 0.111 0.111 

# Zip results
cd $KISSIM_APP
zip -r ${RESULTS}.zip $RESULTS
