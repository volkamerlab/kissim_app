#!/bin/bash
#SBATCH --job-name=kissim_app
#SBATCH --mail-user=dominique.sydow@fu-berlin.de
#SBATCH --mail-type=begin,end
#SBATCH --nodes=1
#SBATCH --qos=standard

# @dominiquesydow
# Apply different weighting schemes and zip data

# Usage
# -----
# Run after finished kissim_encode_compare.sh run
#
# sbatch --time=2:00:00 --ntasks=1 --mem-per-cpu=1024
#   kissim_weights.sh 
#       <Structure subset [all, dfg_in , dfg_out, test]> 
#
# Example
# -------
# sbatch --time=2:00:00 --ntasks=1 --mem-per-cpu=1024 
#   kissim_weights.sh 
#       dfg_in

conda list kissim

STRUCTURE_SUBSET=$1

#KISSIM_APP=/home/${USER}/kissim_app
KISSIM_APP=/home/${USER}/Documents/GitHub/kissim_app
RESULTS=$KISSIM_APP/results_test/${STRUCTURE_SUBSET}

echo "Job settings"
echo "------------" 
echo "Structure subset:" $STRUCTURE_SUBSET

mkdir -p $RESULTS

# Weight features
kissim weights -i $RESULTS/feature_distances.csv.bz2 -o $RESULTS/fingerprint_distances_100.csv.bz2 -w 0.125 0.125 0.125 0.125 0.125 0.125 0.125 0.125 0 0 0 0 0 0 0 
kissim weights -i $RESULTS/feature_distances.csv.bz2 -o $RESULTS/fingerprint_distances_010.csv.bz2 -w 0 0 0 0 0 0 0 0 0.25 0.25 0.25 0.25 0 0 0
kissim weights -i $RESULTS/feature_distances.csv.bz2 -o $RESULTS/fingerprint_distances_001.csv.bz2 -w 0 0 0 0 0 0 0 0 0 0 0 0 0.333 0.333 0.333
kissim weights -i $RESULTS/feature_distances.csv.bz2 -o $RESULTS/fingerprint_distances_110.csv.bz2 -w 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.125 0.125 0.125 0.125 0 0 0
kissim weights -i $RESULTS/feature_distances.csv.bz2 -o $RESULTS/fingerprint_distances_101.csv.bz2 -w 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0 0 0 0 0.166 0.166 0.166
kissim weights -i $RESULTS/feature_distances.csv.bz2 -o $RESULTS/fingerprint_distances_011.csv.bz2 -w 0 0 0 0 0 0 0 0 0.125 0.125 0.125 0.125 0.166 0.166 0.166
kissim weights -i $RESULTS/feature_distances.csv.bz2 -o $RESULTS/fingerprint_distances_111.csv.bz2 -w 0.041 0.041 0.041 0.041 0.041 0.041 0.041 0.041 0.083 0.083 0.083 0.083 0.111 0.111 0.111 
