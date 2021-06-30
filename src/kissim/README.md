# Run `kissim` workflow on Curta HPC

## Curta HPC

The `kissim` workflow is run on Curta, the central HPC cluster of Freie Universität Berlin, provided by Zedat ([DOI](https://refubium.fu-berlin.de/handle/fub188/26993)).

## Before running the job

- Log on to the cluster
- [Install](https://mamba.readthedocs.io/en/latest/getting_started.html#for-new-users) `mamba` on Curta
- Go to Curta home:
    ```bash
    cd /home/${USER}
    ```
- Clone `kissim` repo
    ```bash
    git clone https://github.com/volkamerlab/kissim.git
    ```
- Create `kissim` environment and install `kissim` package
    ```bash
    mamba env create -f kissim/devtools/conda-envs/test_env.yaml -n kissim
    conda activate kissim
    pip install -e kissim
    ```
- Clone `kissim_app` repo
    ```bash
    git clone https://github.com/volkamerlab/kissim_app.git
    ```
- Rsync KLIFS dataset from local computer to cluster
    ```bash
    # Execute from local computer terminal
    rsync -a /home/dominique/Documents/GitHub/kissim_app/data/external/structures/20210630_KLIFS_HUMAN -e ssh sydowd@curta.zedat.fu-berlin.de:/home/sydowd/kissim_app/data/external/structures/
    # If transferred data contains zip file, unzip it
    unzip xxx.zip
    ```

## Run job on cluster

```bash
cd kissim_app/src/kissim
sbatch curta.sh
# Check if job is running
squeue -u sydowd
```

Check out the cluster [documentation](https://www.fu-berlin.de/sites/high-performance-computing/Dokumentation/index.html).

## After the job has finished

Rsync output files from local computer to cluster using:

```bash
# Execute from local computer terminal
rsync -a -e ssh sydowd@curta.zedat.fu-berlin.de:/home/sydowd/kissim_app/results.zip /home/dominique/Documents/GitHub/kissim_app -v --stats --progress
```


