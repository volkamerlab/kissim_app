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
# Encode structures and compare fingerprints on the curta cluster using the kissim package


##################
# Before the job #
##################

# 0. Install mamba on curta.
# 1. Go to curta home:
#    cd /home/${USER}
# 2. Clone kissim repo:
#    git clone https://github.com/volkamerlab/kissim.git
# 3. Create kissim environment and install kissim package:
#    mamba env create -f kissim/devtools/conda-envs/test_env.yaml -n kissim
#    conda activate kissim
#    pip install kissim
# 4. Clone kissim_app repo:
#    git clone git clone https://github.com/volkamerlab/kissim_app.git
# 5. Rsync KLIFS dataset from local computer to cluster using (from local computer terminal):
#    rsync -a /home/dominique/Documents/GitHub/kissim_app/data/external/20210114_KLIFS_HUMAN -e ssh sydowd@curta.zedat.fu-berlin.de:/home/sydowd/kissim_app/data/external


##################
#   Curta job    #
##################

cd /home/${USER}

# Activate environment
#conda activate kissim

# Encode structures
#cd /home/${USER}
#kissim encode \
#-i "kissim_app/data/processed/structure_klifs_ids.txt" \
#-o "kissim_app/results/fingerprints.json" \
#-c 32 \
#-l "kissim_app/data/external/20210114_KLIFS_HUMAN"
# Zip fingerprints
#cd /home/${USER}/kissim_app/results/
#zip fingerprints.zip fingerprints.json

# Compare fingerprints
#cd /home/${USER}
#kissim compare \
#-i "kissim_app/results/fingerprints.json" \
#-o "kissim_app/results/" \
#-c 32
# Zip distances
#cd /home/${USER}/kissim_app/results/
#zip feature_distances.zip feature_distances.json
#zip fingerprint_distances.zip fingerprint_distances.json

# Weight features
cd /home/${USER}/kissim_app/src/comparison
python weight_feature_distances.py


##################
#  Afte the job  #
##################

# Rsync zip files to local computer and unzip