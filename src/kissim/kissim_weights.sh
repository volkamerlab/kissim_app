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
#       <run ID = output folder name> 
#       <Structure subset [all, dfg_in , dfg_out, test]> 
#
# Example
# -------
# sbatch --time=2:00:00 --ntasks=1 --mem-per-cpu=1024 
#   kissim_weights.sh 
#       20210804 
#       dfg_in

conda list kissim

ID=$1
STRUCTURE_SUBSET=$2

KISSIM_APP=/home/${USER}/kissim_app
#KISSIM_APP=/home/${USER}/Documents/GitHub/kissim_app
RESULTS=$KISSIM_APP/results/${ID}/${STRUCTURE_SUBSET}

echo "Job settings"
echo "------------" 
echo "Run ID:" $1 
echo "Structure subset:" $2 

mkdir -p $RESULTS

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
