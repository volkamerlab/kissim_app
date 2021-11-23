# When running sbatch for different conda environments, the previous job must be done before you can switch the conda environment
# Use --dependency=afterok

# Examples run from ~/kissim_app/src/kissim

# Encode and compare
# 4120 structures ~16GB RAM used
sbatch --time=03:30:00 --ntasks=8 --mem-per-cpu=2048 kissim_encode_compare.sh 20210904 dfg_in 20210902_KLIFS_HUMAN normalized full
# 407 structures ~1GB RAM used
sbatch --time=01:00:00 --ntasks=2 --mem-per-cpu=1024 kissim_encode_compare.sh 20210904 dfg_out 20210902_KLIFS_HUMAN normalized full
# 4690 structures ~21GB RAM used
sbatch --time=04:00:00 --ntasks=8 --mem-per-cpu=3072 kissim_encode_compare.sh 20210904 all 20210902_KLIFS_HUMAN normalized full

# Weights
#sbatch --time=01:30:00 --ntasks=1 --mem-per-cpu=1024 kissim_weights.sh 20210904 dfg_in
#sbatch --time=00:10:00 --ntasks=1 --mem-per-cpu=1024 kissim_weights.sh 20210904 dfg_out
#sbatch --time=02:00:00 --ntasks=1 --mem-per-cpu=1024 kissim_weights.sh 20210904 all
