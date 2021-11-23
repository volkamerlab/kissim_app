# Rsync cluster results to workstation

ID=$1
ln -s /media/dominique/eeb680ce-eb5c-49a8-918f-e4d381867bb3/dominique/Documents/GitHub/kissim_app/results_archive /home/dominique/Documents/GitHub/kissim_app/results_archive
rsync -a -e ssh curta:/home/sydowd/kissim_app/results/$ID /home/dominique/Documents/GitHub/kissim_app/results_archive/$ID -v --stats --progress