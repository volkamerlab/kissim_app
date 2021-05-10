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
NCORES=8

# Encode structures
kissim encode -i $KISSIM_APP/data/processed/structure_klifs_ids.txt -o $RESULTS/fingerprints.json -c $NCORES -l $KISSIM_APP/data/external/20210114_KLIFS_HUMAN

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
zip -r results.zip results


##################
#  Afte the job  #
##################

# # Rsync output files from local computer to cluster using (from local computer terminal):
# rsync -a -e ssh sydowd@curta.zedat.fu-berlin.de:/home/sydowd/kissim_app/results.zip /home/dominique/Documents/GitHub/kissim_app -v --stats --progress