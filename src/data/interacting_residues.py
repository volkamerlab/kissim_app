"""
Load interacting residues in KLIFS pocket based on the KLIFS IFPs.
"""

import numpy as np
import pandas as pd
from opencadd.databases.klifs import setup_remote


def residues_interacting_with_ligand(ligand_expo_id):
    """
    For a query ligand, get all interacting residues across all available ligand-bound
    structures in KLIFS.
    Based on KLIFS IFP (covers interactions between ligands and KLIFS pocket).

    Parameters
    ----------
    ligand_expo_id : str
        Ligand expo ID.

    Returns
    -------
    list of int
        List of KLIFS pocket residue positions.
    """

    session = setup_remote()

    # Get ligand KLIFS ID
    ligand_klifs_id = session.ligands.by_ligand_expo_id(ligand_expo_id)["ligand.klifs_id"][0]

    # Get all IFPs for this ligand
    ifp_series = session.interactions.by_ligand_klifs_id(ligand_klifs_id)[
        "interaction.fingerprint"
    ]
    print(f"Number of IFPs for {ligand_expo_id}: {len(ifp_series)}")
    ifp_series_bool = ifp_series.apply(lambda x: [True if i == "1" else False for i in x])
    # Prepare multi-index for columns
    iterables = [range(1, 86), range(1, 8)]
    columns_index = pd.MultiIndex.from_product(iterables, names=["residue", "feature"])
    # Generate DataFrame
    ifp_df = pd.DataFrame(np.array(ifp_series_bool.to_list()), columns=columns_index)

    # Number of features per residue
    n_features_per_residue = ifp_df.groupby("residue", axis=1).sum().sum()
    # Print stats
    print("(residue position, number of features across all IFPs)")
    print(list(n_features_per_residue[n_features_per_residue > 0].items()))

    # Get residues with features
    interacting_residues = n_features_per_residue[n_features_per_residue > 0].index.to_list()
    print(f"Residues interacting with {ligand_expo_id}:")
    print(*interacting_residues)

    return interacting_residues
