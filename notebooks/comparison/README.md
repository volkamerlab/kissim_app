## `structure_distances_vs_feature_weights.ipynb`

### Fingerprint distances distribution

In this notebook, we investigate the ranges of fingerprint distances for different feature weighting schemes.
Feature weighting schemes are denoted as follows: 

_\<physicochemical\>\<distances\>\<moments\>_

- $100$: Include only bits for physicochemical features (_physicochemical_)
- $010$: Include only bits for spatial distances features (_distances_)
- $001$: Include only bits for moments of spatial distances features (_moments_)
- $110$: Include only bits for physicochemical and distances (1:1)
- $101$: Include only bits for physicochemical and moments (1:1)
- $011$: Include only bits for distances and moments (1:1)
- $111$: Include all bits equally weighted by physicochemical, distances, and moments
- $15$: Include all bits equally by bit


## `structure_distances_coverage.ipynb`

### Fingerprint distances between structures for the same kinase

In this notebook, we investigate the ranges of fingerprint distances for each kinase pair.


## `structure_kinase_mapping.ipynb`

### Fingerprint distances between structures for the same kinase

In this notebook, we investigate the ranges of fingerprint distances for each kinase pair.


## `kissim_kinome_tree.ipynb`

### `kissim`-based kinome tree

This notebook generates `kissim`-based kinome trees based on three different kinase matrices:

- Kinase matrix based on all structures/fingerprints (**DFG-in and DFG-out**)
- Kinase matrix based on structure/fingerprints in **DFG-in** conformation only
- Kinase matrix based on structure/fingerprints in **DFG-out** conformation only

Check which kinases are covered by the DFG-in *and* the DFG-out `kissim` trees. 


## `feature_distances.ipynb`

### Feature distances


## `structure_distances_vs_dfg.ipynb`

### Can fingerprint distances discriminate DFG conformations?

The `kissim` fingerprint encodes the pocket residues' spatial distance to four centers&mdash;the pocket centroid, hinge region, DFG region and front pocket&mdash;and should therefore discriminate between two structures in different conformations; when we compare two structures in *different* conformations the fingerprint distance should be higher than for two structures in *similar* conformations.

Let's check if this is true using DFG conformations from KLIFS. Plot distribution of fingerprint distances grouped by in/in, out/out, and in/out pairs.

- Use fingerprint distances for structure pairs between all kinases
- Use fingerprint distances for structure pairs between the same kinase
