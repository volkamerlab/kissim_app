## `001_remove_spatial_outliers.ipynb`

Investigate spatial outliers

We take a look at all structures that contain residues (CA atoms) with a distance to the `kissim` subpocket centers below/above a certain minimum/maximum cutoff. 

This allows us to identify outlier structures that we want to exclude from our dataset (in our `kissim` pipeline this is done with the `kissim outlier` CLI).


## `002_spatial_feature_cutoffs.ipynb`

Normalize for continuous (=spatial) features

Get min-max values for distances and moments:
- over all positions*/subpockets** (coarse grained)
- per position*/subpocket** (fine grained)

\* positions in context of distances
\** subpockets in context of moments


## `003_feature_distributions.ipynb`

Feature distributions

We look at the distribution of features values observed in almost 5000 structures in order to get an impression on the feature value ranges and frequencies.

Recap - in the `kissim` fingerprint we have three feature groups:

- Physicochemical features (discrete/categorial values)
- Distances between residues and subpocket centers (continuous values)
- Moments (mean, standard deviation, skewness) of aforementioned distance distributions (continuous values)


## `004_feature_distribution_per_residue.ipynb`

Per-residue feature values

We investigate the defined features per residue

- over all structures (boxplots/heatmaps)
- for example structures (in 3D)


## `005_fingerprint_bit_coverage_variability.ipynb`

Fingerprint bit coverage and variability

We check the coverage and variability of fingerprint bit positions across all fingerprints in our dataset.

- Investigate missing bits across fingerprints
- Investigate bit variability across fingerprints (standard deviation)
- Get top X bit positions with no/high standard deviation


## `999_fetch_sitealign_features.ipynb`

SiteAlign features

We read the SiteAlign features from the respective [paper](https://onlinelibrary.wiley.com/doi/full/10.1002/prot.21858) and [SI table](https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fprot.21858&file=prot21858-SupplementaryTable.pdf) to verify `kissim`'s implementation of the SiteAlign definitions:
