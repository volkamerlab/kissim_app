# When running sbatch for different conda environments, the previous job must be done before you can switch the conda environment
# Use --dependency=afterok

# Examples run from ~/kissim_app/src/kissim

# Full fingerprint
sbatch --time=08:00:00 curta.sh 20210904-1 dfg_in 20210902_KLIFS_HUMAN normalized full
sbatch --time=01:00:00 curta.sh 20210904-1 dfg_out 20210902_KLIFS_HUMAN normalized full
sbatch --time=08:00:00 curta.sh 20210904-1 dfg_all 20210902_KLIFS_HUMAN normalized full
sbatch --time=08:00:00 curta.sh 20210904-2 dfg_in 20210902_KLIFS_HUMAN normalized subset
sbatch --time=01:00:00 curta.sh 20210904-2 dfg_out 20210902_KLIFS_HUMAN normalized subset
sbatch --time=08:00:00 curta.sh 20210904-2 dfg_all 20210902_KLIFS_HUMAN normalized subset

ln -s /media/dominique/eeb680ce-eb5c-49a8-918f-e4d381867bb3/dominique/Documents/GitHub/kissim_app/results_archive /home/dominique/Documents/GitHub/kissim_app/results_archive

rsync -a -e ssh curta:/home/sydowd/kissim_app/results/20210904-1/dfg_in.zip /home/dominique/Documents/GitHub/kissim_app/results_archive/20210904-1 -v --stats --progress
rsync -a -e ssh curta:/home/sydowd/kissim_app/results/20210904-1/dfg_out.zip /home/dominique/Documents/GitHub/kissim_app/results_archive/20210904-1 -v --stats --progress
rsync -a -e ssh curta:/home/sydowd/kissim_app/results/20210904-1/dfg_all.zip /home/dominique/Documents/GitHub/kissim_app/results_archive/20210904-1 -v --stats --progress
rsync -a -e ssh curta:/home/sydowd/kissim_app/results/20210904-2/dfg_in.zip /home/dominique/Documents/GitHub/kissim_app/results_archive/20210904-2 -v --stats --progress
rsync -a -e ssh curta:/home/sydowd/kissim_app/results/20210904-2/dfg_out.zip /home/dominique/Documents/GitHub/kissim_app/results_archive/20210904-2 -v --stats --progress
rsync -a -e ssh curta:/home/sydowd/kissim_app/results/20210904-2/dfg_all.zip /home/dominique/Documents/GitHub/kissim_app/results_archive/20210904-2 -v --stats --progress

