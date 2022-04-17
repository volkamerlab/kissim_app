# @dominiquesydow
# Subset and compare fingerprints
# - DFG-in focused residues
# - Martin et al. residues
# 
# Run this script only after having results from running the main script
# https://github.com/volkamerlab/kissim_app/blob/master/scripts/kissim_encode_compare.sh
#
# Usage
# -----
# cd /path/to/kissim_app
# bash kissim_subsets.sh

KISSIM_APP="."
NCORES=7

# DFG-in focused residues
for name_subset in dfg_in martin_set
do
    RESULTS=$KISSIM_APP/results/dfg_in_subset_${name_subset}
    echo $RESULTS
    echo "Select fingerprint subset..."
    kissim subset -i $RESULTS/fingerprints_normalized.json -o $RESULTS/fingerprints_subset.json -s $name_subset
    echo "Done."
    echo "Compare fingerprints..."
    kissim compare -i $RESULTS/fingerprints_subset.json -o $RESULTS -c $NCORES
    echo "Done."
done