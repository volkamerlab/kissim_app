#!/bin/bash
#SBATCH --job-name=kissim_app
#SBATCH --mail-user=dominique.sydow@fu-berlin.de
#SBATCH --mail-type=begin,end
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=4096
#SBATCH --time=10:00:00
#SBATCH --qos=standard

# @dominiquesydow
# Encode structures and compare fingerprints on the curta cluster using the kissim package


##################
# Before the job #
##################

# # Install mamba on curta.
# # Go to curta home:
# cd /home/${USER}

# # Clone kissim repo:
#  git clone https://github.com/volkamerlab/kissim.git

# # Create kissim environment and install kissim package:
#  mamba env create -f kissim/devtools/conda-envs/test_env.yaml -n kissim
#  conda activate kissim
#  pip install kissim

# # Clone kissim_app repo:
#  git clone https://github.com/volkamerlab/kissim_app.git

# # Rsync KLIFS dataset from local computer to cluster using (from local computer terminal):
# rsync -a /home/dominique/Documents/GitHub/kissim_app/data/external/20210114_KLIFS_HUMAN -e ssh sydowd@curta.zedat.fu-berlin.de:/home/sydowd/kissim_app/data/external


##################
#   Curta job    #
##################

# Encode structures
cd /home/${USER}
kissim encode -i "kissim_app/data/processed/structure_klifs_ids.txt" -o "kissim_app/results/fingerprints.json" -c 32 -l "kissim_app/data/external/20210114_KLIFS_HUMAN"
# Zip fingerprints

# Remove structural outliers
cd /home/${USER}/kissim_app/src/encoding
python remove_outliers.py

# Compare fingerprints
cd /home/${USER}
kissim compare \
-i "kissim_app/results/fingerprints_clean.json" -o "kissim_app/results/" -c 32

# Weight features
cd /home/${USER}/kissim_app/src/comparison
python weight_feature_distances.py

# Zip results
cd /home/${USER}/kissim_app
zip -r results.zip results



##################
#  Afte the job  #
##################

# # Rsync output files from local computer to cluster using (from local computer terminal):
# rsync -a -e ssh sydowd@curta.zedat.fu-berlin.de:/home/sydowd/kissim_app/results.zip /home/dominique/Documents/GitHub/kissim_app 