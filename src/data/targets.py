"""
Load ligand-target pair datasets.
"""

import logging

import pandas as pd

from . import ligands, kinases

logger = logging.getLogger(__name__)


def pkidb(ligand_names, fda_approved=False):
    """
    Get targets for input ligands based on PKIDB data.
    Ligand names will be mapped onto the PKIDB ligand IDs (mismatching ligands are removed).
    Kinase names will be mapped onto the KinMap kinase names (mismatching kinases are removed).

    Parameters
    ----------
    ligand_names : str or list of str
        Ligand names.
    fda_approved : bool
        Optional: Input ligand names will only be considered if they are part of the FDA-approved
        subset of the PKIDB dataset.

    Returns
    -------
    pandas.DataFrame
        For each input ligand (row) that is reported in PKIDB, get reported PKIDB kinase targets
        and their KinMap name (columns). Kinases that have no name in KinMap will be discarded.
    """

    if isinstance(ligand_names, str):
        ligand_names = [ligand_names]

    pkidb_df = ligands.pkidb(fda_approved=fda_approved)

    # Get targets (listed in PKIDB) for each of the input ligands
    ligand_target_sets = [_pkidb(ligand_name, pkidb_df) for ligand_name in ligand_names]
    ligand_target_sets = pd.DataFrame(
        {"ligand.input": ligand_names, "targets.pkidb": ligand_target_sets}
    )
    # Explode DataFrame (one row per ligand-kinase pair)
    ligand_targets = ligand_target_sets.explode("targets.pkidb", ignore_index=True)

    # Cast PKIDB to KinMap kinase names
    ligand_targets["targets.kinmap"] = kinases._kinmap_kinase_names(
        ligand_targets["targets.pkidb"]
    )
    # Remove ligands without target information
    ligand_targets = ligand_targets[~(ligand_targets["targets.kinmap"].str.startswith("unknown"))]

    # Implode DataFrame (one row per ligand)
    ligand_target_sets = pd.DataFrame(
        [
            ligand_targets.groupby("ligand.input")["targets.pkidb"].apply(list),
            ligand_targets.groupby("ligand.input")["targets.kinmap"].apply(list),
        ]
    ).transpose()
    # Sort by number of targets (ascending)
    ligand_target_sets = ligand_target_sets.loc[
        ligand_target_sets["targets.pkidb"].apply(len).sort_values().index, :
    ].reset_index()

    return ligand_target_sets


def _pkidb(ligand_name, pkidb_df):
    """
    Get reported PKIDB targets for input ligand.

    Parameters
    ----------
    ligand_name : str
        Ligand name.
    pkidb_df : pandas.DataFrame
        PKIDB data (columns) for all PKIDB ligands (rows) from `ligands.pkidb()`.

    Returns
    -------
    list or str
        PKIDB target names. If input ligand name unknown or ambiguous return "unknown (why?)".
    """

    targets = pkidb_df[pkidb_df["ID"] == ligand_name]["Targets"]

    if len(targets) == 0:
        return "unknown (not in PKIDB)"
    elif len(targets) == 1:
        return targets.reset_index(drop=True)[0]
    else:
        return "unknown (ambiguous ligand name)"
