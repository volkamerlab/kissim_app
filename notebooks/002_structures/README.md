## `001_prepare_dataset.ipynb`

Data preparation and exploration

We prepare the KLIFS dataset to be used for `kissim` encoding and comparison.

- Fetch all structures in KLIFS (metadata).
- Filter dataset by
  - Species
  - DFG conformation (optional)
  - Resolution
  - Quality score
  - Maximum number of mutations in the pocket
  - Maximum number of missing residues in the pocket (most will be caught by quality score already) 
  - Best struture per kinase-PDB pair
- Save the KLIFS structure IDs for the filtered dataset.

__Note__: The KLIFS data is prepared only on the basis of the structures' metadata from KLIFS. Additional filtering will happen during fingerprint generation, where the actual structural data (coordiantes ect.) are used.


## `002_explore_dataset.ipynb`

Data exploration

We explore the KLIFS dataset used to generate `kissim` fingerprints.

- Load filtered structures from `prepare_dataset.ipynb` by structure KLIFS IDs.
- Explore kinases in dataset
- Explore structures in dataset


## `003_pocket_residue_ca_atom_coordinates.ipynb`

Extract pocket residue CA atom coordinates

We extract the coordinates for all pockets' residue CA atoms to be used in other notebooks.


## `004_mutated_structures.ipynb`

KLIFS structures with mutated pockets

Explore KLIFS structures with mutations in their pocket:
- Number of structures with mutations
- Distribution of number of mutations per structure
- Number of mutations per KLIFS pocket position
- Type of mutations
- Type of mutations per KLIFS position


## `005_missing_pocket_residues.ipynb`

Missing residues

We check the number and position of missing residues in kinase structures (fetched from KLIFS).


## `006_alphafold.ipynb`

AlphaFold DB kinase dataset

So `kissim` can only reach the structurally covered kinome? Well, we are in luck! 

Let's use the predicted kinase structures provided in the AlphaFold DB (AF) and use these structures to generate a AF-based `kissim` tree.

In this notebook we prepare a kinase subset of the AF human dataset.
