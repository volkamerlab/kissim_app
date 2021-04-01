#!/bin/bash
#SBATCH --job-name=kissim_app
#SBATCH --mail-user=dominique.sydow@fu-berlin.de
#SBATCH --mail-type=begin,end
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

KISSIM_APP=/home/${USER}/kissim_app
RESULTS=$KISSIM_APP/results
NCORES=32

# Encode structures
kissim encode -i $KISSIM_APP/data/processed/structure_klifs_ids.txt -o $RESULTS/fingerprints.json -c $NCORES -l $KISSIM_APP/data/external/20210114_KLIFS_HUMAN
# Zip fingerprints

# Remove structural outliers
cd $KISSIM_APP/src/encoding
python remove_outliers.py -i $RESULTS/fingerprints.json

# Compare fingerprints
kissim compare -i $RESULTS/fingerprints_clean.json -o $RESULTS -c $NCORES

# Weight features
cd $KISSIM_APP/src/comparison
python weight_feature_distances.py -i $RESULTS/feature_distances.json -c $NCORES

# Zip results
cd $KISSIM_APP
zip -r results.zip results



##################
#  Afte the job  #
##################

# # Rsync output files from local computer to cluster using (from local computer terminal):
# rsync -a -e ssh sydowd@curta.zedat.fu-berlin.de:/home/sydowd/kissim_app/results.zip /home/dominique/Documents/GitHub/kissim_app 