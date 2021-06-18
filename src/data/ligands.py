"""
Load ligand datasets.
"""

import logging
from pathlib import Path

import pandas as pd
from rdkit.Chem import PandasTools

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent / "../../data/external/ligands"
PKIDB_PATH = DATA_PATH / "PKIDB/pkidb_2021-04-19.sdf"


def pkidb(pkidb_path=PKIDB_PATH, fda_approved=False):
    """
    Load PKIDB ligand dataset.

    Parameters
    ----------
    pkidb_path : str or pathlib.Path
        Path to PKIDB SDF download.
    fda_approved : bool
        Keep only FDA-approved PKIDB ligands (default: `False`).

    Returns
    -------
    pandas.DataFrame
        PKIDB data (columns) for all PKIDB ligands (rows).
    """

    pkidb_df = PandasTools.LoadSDF(str(pkidb_path))
    pkidb_df["Synonyms"] = [i.split(" | ") for i in pkidb_df["Synonyms"].to_list()]
    pkidb_df["Targets"] = [i.split("; ") for i in pkidb_df["Targets"]]
    pkidb_df["lig_pdbID"] = [i if len(i) == 0 else i[1:-1] for i in pkidb_df["lig_pdbID"]]

    # Filter for FDA-approved drugs
    if fda_approved:
        pkidb_df = pkidb_df[pkidb_df["FDA_approved"] == "Y"]

    return pkidb_df


def _pkidb_ligand_names(ligand_names, fda_approved=False):
    """
    Cast given ligand names to the PKIDB ligand IDs.

    Parameters
    ----------
    ligand_names : list of str
        Ligand names.
    fda_approved : bool
        Keep only FDA-approved PKIDB ligands (default: `False`).

    Returns
    -------
    list of str
        List of PKIDB ligand names.
    """

    pkidb_df = pkidb(fda_approved=fda_approved)
    pkidb_ligand_names = [
        _pkidb_ligand_name(ligand_name, pkidb_df) for ligand_name in ligand_names
    ]

    change_log = pd.DataFrame({"ligand.input": ligand_names, "ligand.pkidb": pkidb_ligand_names})
    change_log = change_log[change_log["ligand.input"] != change_log["ligand.pkidb"]]
    if change_log.shape[0] > 0:
        logger.warning(
            f"Changed ligand names (unknown names may be discarded"
            f" - see function docstring):\n{change_log}"
        )

    return pkidb_ligand_names


def _pkidb_ligand_name(ligand_name, pkidb_df):
    """
    Cast a given ligand name to the PKIDB ligand ID.

    Parameters
    ----------
    ligand_name : str
        Ligand name.
    pkidb_df : pandas.DataFrame
        PKIDB data (columns) for all PKIDB ligands (rows) from `ligands.pkidb()`.

    Returns
    -------
    str
        PKIDB ligand name. If input ligand name unknown or ambiguous return "unknown (why?)".
    """

    if pkidb_df["ID"].isin([ligand_name]).any():
        return ligand_name
    else:
        ligand_name_pkidb = pkidb_df[pkidb_df["Synonyms"].apply(lambda x: ligand_name in x)]
        if len(ligand_name_pkidb) == 0:
            return "unknown (not in PKIDB)"
        elif len(ligand_name_pkidb) == 1:
            return ligand_name_pkidb.squeeze()["ID"]
        else:
            return "unknown (ambiguous ligand name)"
