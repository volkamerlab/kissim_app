## `001_profiling_summary.ipynb`

Evaluate performace of `kissim` vs. profiling datasets

Summarize ligand-kinase pair performances based on multiple profiling datasets:

- Profiling datasets: Karaman and Davis
- `kissim` datasets: Different feature weighting schemes


## `002_profiling_karaman.ipynb`

Predict ligand profiling using `kissim` using the Karaman dataset

In order to assess the predictive power of `kissim`, we here choose a ligand-centric evaluation. 
We will compare if `kissim` can predict on- and off-targets determined in ligand profiling studies.

- Kinase-kinase distance dataset (use KinMap kinase names): Select kinases from profiling dataset by query ligand
- Kinase-ligand profiling dataset (use KinMap kinase names and PKIDB ligand names): Select kinases from distances dataset by the ligand's on-target
- Merge both datasets and keep only kinases that have measurements in both datasets
- Rank kinases by distances
- Calculuate enrichment factors and enrichment plots
- Calculate ROC curves


## `003_profiling_davis.ipynb`

Predict ligand profiling using `kissim` using the Davis dataset

In order to assess the predictive power of `kissim`, we here choose a ligand-centric evaluation. 
We will compare if `kissim` can predict on- and off-targets determined in ligand profiling studies.

- Kinase-kinase distance dataset (use KinMap kinase names): Select kinases from profiling dataset by query ligand
- Kinase-ligand profiling dataset (use KinMap kinase names and PKIDB ligand names): Select kinases from distances dataset by the ligand's on-target
- Merge both datasets and keep only kinases that have measurements in both datasets
- Rank kinases by distances
- Calculuate enrichment factors and enrichment plots
- Calculate ROC curves


## `004_profiling_karaman_davis.ipynb`

Predict ligand profiling using `kissim` (pooled Karaman and Davis dataset)

In order to assess the predictive power of `kissim`, we here choose a ligand-centric evaluation. 
We will compare if `kissim` can predict on- and off-targets determined in ligand profiling studies.

- Kinase-kinase distance dataset (use KinMap kinase names): Select kinases from profiling dataset by query ligand
- Kinase-ligand profiling dataset (use KinMap kinase names and PKIDB ligand names): Select kinases from distances dataset by the ligand's on-target
- Merge both datasets and keep only kinases that have measurements in both datasets
- Rank kinases by distances
- Calculuate enrichment factors and enrichment plots
- Calculate ROC curves


## `005_profiling_details.ipynb`

Predict ligand profiling using `kissim` - detailed inspection

Let's take a closer look at an example kinase-ligand pair. 

- What are measured on- and off-targets?
- How does bioactivity data correlate with `kissim` ranks?
- Is the kinase an easy target (a) because underlying structures are co-crystallized with the same ligands or (b) because detected off-targets are very close (kinase group, family)? 
- Is the kinase a difficult target (a) because the tested ligand is a type II ligand although most structures bind type I ligands or (b) because we only have a low structural coverage for the kinase?


## `006_kinmap_trees.ipynb`

Ligand-based validation mapped on KinMap tree

Check if we can retrieve on-/off-targets for a selected ligand (as reported by Karaman et al.) solely based on the structurally most similar kinases to respective main target of that ligand.

1. Select ligands to investigate: Erlotinib and Imatinib (target ligands).
2. Get target of Erlotinib and Imatinib: EGFR and ABL1 (target kinases).
3. Find top20 and top30 similar kinases to target kinase.
4. Save these top kinases in KinMap format for visualization using the KinMap website.


## `007_ligands_targeting_multiple_kinase_groups.ipynb`

Ligands targeting multiple kinase groups

Extract from the pooled Karaman-Davis profiling dataset ligands that target mulitple kinase groups. We can treat those as "unexpected off-targets".


## `008_summary_auc_tree_distances.ipynb`

Performance summary over different `kissim` setups

Summarize performance of different `kissim` setups:

- Profiling vs. `kissim` AUCs: How well does `kissim` reflect profiling data?
- Phylogenetic `kissim` tree: How well do selected on- and off-targets cluster together?
- Top `kissim` ranks: How high do selected on- and off-targets rank in `kissim`?

DFG-in conformations only!


## `009_vectorize_pairwise_similarities.ipynb`

Demo: Vectorize pairwise similarities

Demo on "How to vectorize pairwise (dis)similarity metrics"

> A straightforward pattern for vectorizing metrics like L1 distance and Intersection over Union for all pairs of points.

Taken from: https://towardsdatascience.com/how-to-vectorize-pairwise-dis-similarity-metrics-5d522715fb4e


## `010_comparative_analyses.ipynb`

Compare different similarity methods

- Pocket structure similarity (`kissim`)
- Pocket sequence identity (KLIFS seq)
- Interaction similarity (KLIFS IFP)
- Compare matrices!


## `011_profiling_karaman_davis__ifp.ipynb`

Predict ligand profiling using IFPs (pooled Karaman and Davis dataset)

In order to assess the predictive power of `kissim`, we here choose a ligand-centric evaluation. 
We will compare if `kissim` can predict on- and off-targets determined in ligand profiling studies.

- Kinase-kinase distance dataset (use KinMap kinase names): Select kinases from profiling dataset by query ligand
- Kinase-ligand profiling dataset (use KinMap kinase names and PKIDB ligand names): Select kinases from distances dataset by the ligand's on-target
- Merge both datasets and keep only kinases that have measurements in both datasets
- Rank kinases by distances
- Calculuate enrichment factors and enrichment plots
- Calculate ROC curves


## `012_profiling_karaman_davis__seq.ipynb`

Predict ligand profiling using sequence (pooled Karaman and Davis dataset)

In order to assess the predictive power of `kissim`, we here choose a ligand-centric evaluation. 
We will compare if `kissim` can predict on- and off-targets determined in ligand profiling studies.

- Kinase-kinase distance dataset (use KinMap kinase names): Select kinases from profiling dataset by query ligand
- Kinase-ligand profiling dataset (use KinMap kinase names and PKIDB ligand names): Select kinases from distances dataset by the ligand's on-target
- Merge both datasets and keep only kinases that have measurements in both datasets
- Rank kinases by distances
- Calculuate enrichment factors and enrichment plots
- Calculate ROC curves


## `013_profiling_karaman_davis__sitealign.ipynb`

Predict ligand profiling using SiteAlign (pooled Karaman and Davis dataset)

In order to assess the predictive power of `kissim`, we here choose a ligand-centric evaluation. 
We will compare if `kissim` can predict on- and off-targets determined in ligand profiling studies.

- Kinase-kinase distance dataset (use KinMap kinase names): Select kinases from profiling dataset by query ligand
- Kinase-ligand profiling dataset (use KinMap kinase names and PKIDB ligand names): Select kinases from distances dataset by the ligand's on-target
- Merge both datasets and keep only kinases that have measurements in both datasets
- Rank kinases by distances
- Calculuate enrichment factors and enrichment plots
- Calculate ROC curves


## `014_comparative_analyses_auc.ipynb`

Compare AUC values between KiSSim and other methods

AUC values are calculated w.r.t. to Karaman-Davis profiling data for:

- KiSSim (notebook 006/004)
- KLIFS pocket sequence (notebook 006/012)
- KLIFS pocket IFP (notebook 006/011)
- SiteAlign (notebook 006/013)

Show scatter plots KiSSim's AUC vs. other methods' AUC.


## `015_subset_kissim_fingerprints.ipynb`

 KiSSim matrix only based on ligand-interacting residues

> The advantage of IFPs is that they emphasize important residues and interactions as seen based on one or more ligands; the disadvantage is that not all possibly relevant interactions have been seen, yet.

How about KiSSim? Does it outperform the IFP approach still if we focus on residues that are covered by IFPs for a single residue.


## `016_profiling_moret.ipynb`

Predict ligand profiling using `kissim` (pooled Karaman and Davis dataset)

In order to assess the predictive power of `kissim`, we here choose a ligand-centric evaluation. 
We will compare if `kissim` can predict on- and off-targets determined in ligand profiling studies.

- Kinase-kinase distance dataset (use KinMap kinase names): Select kinases from profiling dataset by query ligand
- Kinase-ligand profiling dataset (use KinMap kinase names and PKIDB ligand names): Select kinases from distances dataset by the ligand's on-target
- Merge both datasets and keep only kinases that have measurements in both datasets
- Rank kinases by distances
- Calculuate enrichment factors and enrichment plots
- Calculate ROC curves
