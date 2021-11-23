## `001_feature_distances.ipynb`

Feature distances

We check the per-feature distributions (e.g. size distances or hinge region distances) based on all pairwise fingerprint feature distances. Which features show the most/fewest variations?


## `002_fingerprint_distances_vs_feature_weights.ipynb`

Fingerprint distances distribution

In this notebook, we investigate the ranges of fingerprint distances for different feature weighting schemes.
Feature weighting schemes are denoted as follows: 

> physicochemical/distances/moments

- 100: Include only bits for physicochemical features (_physicochemical_)
- 010: Include only bits for spatial distances features (_distances_)
- 001: Include only bits for moments of spatial distances features (_moments_)
- 110: Include only bits for physicochemical and distances (1:1)
- 101: Include only bits for physicochemical and moments (1:1)
- 011: Include only bits for distances and moments (1:1)
- 111: Include all bits equally weighted by physicochemical, distances, and moments
- 15: Include all bits equally by bit


## `003_fingerprint_distances_coverage.ipynb`

Fingerprint pair bit coverages

We investigate the bit coverage of the fingerprint pairs in the `kissim` dataset.

List the following numbers based on (a) all distances and (b) only distances matching a given bit coverage cutoff
- Number of structures
- Number of structure pairs (theory)
- Number of structure pairs (experimental)
- Number of kinases
- Number of kinase pairs (theory)
- Number of kinase pairs (experimental)


## `004_fingerprint_distances_vs_dfg.ipynb`

Can fingerprint distances discriminate DFG conformations?

The `kissim` fingerprint encodes the pocket residues' spatial distance to four centers&mdash;the pocket centroid, hinge region, DFG region and front pocket&mdash;and should therefore discriminate between two structures in different conformations; when we compare two structures in *different* conformations the fingerprint distance should be higher than for two structures in *similar* conformations.

Let's check if this is true using DFG conformations from KLIFS. Plot distribution of fingerprint distances grouped by in/in, out/out, and in/out pairs.

- Use fingerprint distances for structure pairs between all kinases
- Use fingerprint distances for structure pairs between the same kinase


## `005_structure_kinase_mapping.ipynb`

Fingerprint distances between structures for the same kinase

We investigate the ranges of fingerprint distances for each kinase pair:

- Compare the fingerprint distance distribution for intra-kinase pairs and inter-kinase pairs
- For the kinase pairs with highest structure pair coverage, show the range of fingerprint distances (consider minimum or median for structure-to-kinase mapping)
- Generate `kissim` kinase matrix for kinase subset investigated in the paper ["Analyzing Kinase Similarity in Small Molecule and Protein Structural Space to Explore the Limits of Multi-Target Screening"](https://www.mdpi.com/1420-3049/26/3/629)


## `006_kissim_kinome_tree.ipynb`

`kissim`-based kinome tree

We generate `kissim`-based kinome matrices and trees based on three different parameters:

- Feature weighting schemes
- DFG conformations
  - Kinase matrix based on all structures/fingerprints (**DFG-in and DFG-out**)
  - Kinase matrix based on structure/fingerprints in **DFG-in** conformation only
  - Kinase matrix based on structure/fingerprints in **DFG-out** conformation only
- Clustering methods
