# When running sbatch for different conda environments, the previous job must be done before you can switch the conda environment
# Use --dependency=afterok

# Examples run from ~/kissim_app/src/kissim

# Test
sbatch --time=00:05:00 curta.sh test-1 test 20210630_KLIFS_HUMAN unnormalized full main
sbatch --time=00:05:00 --dependency=afterok:7500442 curta.sh test-2 test 20210630_KLIFS_HUMAN normalized full main
sbatch --time=00:05:00 --dependency=afterok:7500445 curta.sh test-3 test 20210630_KLIFS_HUMAN normalized full discrete-sco-exp
sbatch --time=00:05:00 --dependency=afterok:7500446 curta.sh test-4 test 20210630_KLIFS_HUMAN normalized full l1-norm-only
sbatch --time=00:05:00 --dependency=afterok:7500447 curta.sh test-5 test 20210630_KLIFS_HUMAN normalized full l2-norm-only
sbatch --time=00:05:00 --dependency=afterok:7500448 curta.sh test-6 test 20210630_KLIFS_HUMAN normalized full discrete-sco-exp-l1-norm-only

# Check output
head kissim_app/results/test-1/test/fingerprint_distances.csv
head kissim_app/results/test-2/test/fingerprint_distances.csv
head kissim_app/results/test-3/test/fingerprint_distances.csv
head kissim_app/results/test-4/test/fingerprint_distances.csv
head kissim_app/results/test-5/test/fingerprint_distances.csv
head kissim_app/results/test-6/test/fingerprint_distances.csv

# DFG-in
sbatch --time=08:00:00 curta.sh 20210804-1 dfg_in 20210630_KLIFS_HUMAN normalized full main
sbatch --time=08:00:00 --dependency=afterok:7500458 curta.sh 20210804-2 dfg_in 20210630_KLIFS_HUMAN normalized full discrete-sco-exp
sbatch --time=08:00:00 --dependency=afterok:7500459 curta.sh 20210804-3 dfg_in 20210630_KLIFS_HUMAN normalized full l1-norm-only
sbatch --time=08:00:00 --dependency=afterok:7500460 curta.sh 20210804-4 dfg_in 20210630_KLIFS_HUMAN normalized full l2-norm-only
sbatch --time=08:00:00 --dependency=afterok:7500461 curta.sh 20210804-5 dfg_in 20210630_KLIFS_HUMAN normalized full discrete-sco-exp-l1-norm-only

