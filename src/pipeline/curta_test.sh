#!/bin/bash
#SBATCH --job-name=kissim_app
#SBATCH --mail-user=dominique.sydow@fu-berlin.de
#SBATCH --mail-type=end
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=4096
#SBATCH --time=10:00:00
#SBATCH --qos=standard

# @dominiquesydow
# Test script: Encode structures and compare fingerprints on the curta cluster using the kissim package

cd /home/${USER}

# Activate environment
#conda activate kissim

# Encode structures
cd /home/${USER}
kissim encode \
-i "kissim_app/data/processed/structure_klifs_ids.txt" \
-o "kissim_app/results/test/fingerprints.json" \
-c 32 \
-l "kissim_app/data/external/20210114_KLIFS_HUMAN"
# Zip fingerprints
cd /home/${USER}/kissim_app/results/test/
zip fingerprints.zip fingerprints.json

# Compare fingerprints
cd /home/${USER}
kissim compare \
-i "kissim_app/results/test/fingerprints.json" \
-o "kissim_app/results/" \
-c 32
# Zip distances
cd /home/${USER}/kissim_app/results/test/
zip feature_distances.zip feature_distances.json
zip fingerprint_distances.zip fingerprint_distances.json
