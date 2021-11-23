## `001_kissim_matrix_by_version.ipynb`

Compare the results from different `kissim` runs

Compare results (kinase matrices) from different runs:

- `matrix_wbug`: **Run on 20210508**; based on KLIFS dataset from 20210114; **with** charged-THR bug
- `matrix_wobug`: **Run on 20210708**; based on KLIFS dataset from 20210114; without charged-THR bug
- `matrix_2019`: 2019 dataset


## `101_pooled_profiling.ipynb`

Evaluate performace of `kissim` vs. profiling datasets

Summarize ligand-kinase pair performances based on multiple profiling datasets:

- Profiling datasets: Karaman and Davis
- `kissim` datasets: Different feature weighting schemes
- Saves AUC values per setting combination


## `201_kinome_tree_versions.ipynb`

`kissim`-based kinome tree

We generate `kissim`-based kinome matrices and trees based on three different parameters:

- `kissim` runs: With/without charged-THR bug, different KLIFS datasets
- Feature weighting schemes
- DFG conformations
  - Kinase matrix based on all structures/fingerprints (**DFG-in and DFG-out**)
  - Kinase matrix based on structure/fingerprints in **DFG-in** conformation only
  - Kinase matrix based on structure/fingerprints in **DFG-out** conformation only
- Clustering methods


## `202_kinome_tree_20210804.ipynb`

`kissim`-based kinome tree

We generate `kissim`-based kinome matrices and trees based on for the 20210804 runs.


## `203_kinome_tree_20210810.ipynb`

`kissim`-based kinome tree

We generate `kissim`-based kinome matrices and trees based on for the 20210810 runs.


## `204_kinome_tree_20210812.ipynb`

`kissim`-based kinome tree

We generate `kissim`-based kinome matrices and trees based on for the 20210812 runs.


## `301_summary_auc_tree_distances.ipynb`

Performance summary over different `kissim` setups

Summarize performance of different `kissim` setups:

- Profiling vs. `kissim` AUCs: How well does `kissim` reflect profiling data?
- Phylogenetic `kissim` tree: How well do selected on- and off-targets cluster together?
- Top `kissim` ranks: How high do selected on- and off-targets rank in `kissim`?

DFG-in conformations only!
