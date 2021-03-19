# Notebooks

In this folder all notebooks are collected to analyze the all-against-all comparison of KLIFS 
structures.

## Structures

`structures/`: Notebooks preparing and analyzing the structures that are used for the all-against-all comparison.

- `prepare_dataset.ipynb`: Prepare the KLIFS _structure dataset_ (filter available KLIFS structures following certain criteria). Save all selected structure KLIFS IDs to file.
- `explore_dataset.ipynb`: Perform a few statistics on the kinases and structures covered by the selected _structure dataset_.
- `pocket_residue_ca_atom_coordinates.ipynb`: Extract pocket residue CA atom coordinates for the selected _structure dataset_ and save to file for investigations later.

## Subpockets

`subpockets/`: Notebooks analyzing the subpocket centers which are the bases for the spatial bits in the `kissim` fingerprint.

- `anchor_residue_selection.ipynb`: Select the anchor residues defining the `kissim` subpockets.
- `subpocket_robustness.ipynb`: Analyze variablility of subpocket centers between and across subpockets in the selected _structure dataset_.
- `subpocket_to_target_residues.ipynb`: Analyze distances between subpocket centers and their target residues in the selected _structure dataset_.
- `subpocket_vs_conformations.ipynb`: Compare subpocket center positions for different kinase conformations.

## Fingerprints

`fingerprints/`: Notebooks analyzing the encoded structures (fingerprints).

- `remove_spatial_outliers.ipynb`: Remove spatial outliers from fingerprint set.
- `feature_distributions.ipynb`: Analyze feature distributions in the fingerprint set.
- `feature_distribution_per_residue.ipynb`: Analyse bit distributions in the fingeprint set.
- `spatial_feature_cutoffs.ipynb`: Define the min-max cutoffs for the min-max normalization of continuous features such as the distances and moments features.
- `fingerprint_bit_coverage_variability.ipynb`: Analyze the coverage and variability of fingerprint bit positions in the fingerprint set.

## Comparison

`comparison`: Notebooks analyzing the all-against-all comparison. 

- TBA