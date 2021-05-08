#!/bin/bash

# @dominiquesydow
# Encode structures and compare fingerprints on the curta cluster using the kissim package
# SMALL TEST SET ONLY

KISSIM_APP=/home/${USER}/Documents/GitHub/kissim_app
RESULTS=$KISSIM_APP/results/test1/
NCORES=7

# Encode structures
kissim encode -i $KISSIM_APP/data/processed/structure_klifs_ids_test.txt -o $RESULTS/fingerprints.json -c $NCORES -l $KISSIM_APP/data/external/20210114_KLIFS_HUMAN
# Zip fingerprints

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

