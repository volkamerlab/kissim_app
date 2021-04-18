#!/bin/bash

# @dominiquesydow
# Encode structures and compare fingerprints on the curta cluster using the kissim package
# SMALL TEST SET ONLY

KISSIM_APP=/home/${USER}/Documents/GitHub/kissim_app
RESULTS=$KISSIM_APP/results
NCORES=8

# Encode structures
kissim encode -i $KISSIM_APP/data/processed/structure_klifs_ids_test.txt -o $RESULTS/fingerprints.json -c $NCORES -l $KISSIM_APP/data/external/20210114_KLIFS_HUMAN
# Zip fingerprints

# Remove structural outliers
cd $KISSIM_APP/src/encoding
python remove_outliers.py -i $RESULTS/fingerprints.json

# Compare fingerprints
kissim compare -i $RESULTS/fingerprints_clean.json -o $RESULTS -c $NCORES

# Weight features
cd $KISSIM_APP/src/comparison
python weight_feature_distances.py -i $RESULTS/feature_distances.json -c $NCORES
