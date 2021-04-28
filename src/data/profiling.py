"""
Load profiling datasets (in unified output format).
"""

import logging
from pathlib import Path
import json

import pandas as pd

from . import ligands

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent / "../../data/external/profiling"
KARAMAN_PATH = DATA_PATH / "Karaman/Karaman_profiling.js"
DAVIS_PATH = DATA_PATH / "Davis/Davis_profiling.js"


def karaman(pkidb_ligands=False, fda_approved=False, data_path=KARAMAN_PATH):
    """
    Load Karaman profiling dataset from KinMap.
    Optionally: Keep only (a) all PKIDB ligands or (b) all FDA-approved PKIDB ligands (while
    renaming all ligands to their names in PKIDB).

    Parameters
    ----------
    pkidb_ligands : bool
        Keep only PKIDB ligands (will rename ligands to their names in PKIDB). Default is False.
    fda_approved : bool
        Has only effect if `pkidb_ligands` is True. Keep only FDA-approved PKIDB ligands.
        Default is False.
    data_path : str or pathlib.Path
        Path to Karaman dataset (JS file from KinMap).

    Returns
    -------
    pandas.DataFrame
        Karaman profiling data for different kinases (rows) and ligands (columns).
    """
    return _kinmap_profiling(data_path, "karaman", pkidb_ligands, fda_approved)


def davis(pkidb_ligands=False, fda_approved=False, data_path=DAVIS_PATH):
    """
    Load Davis profiling dataset from KinMap.
    Optionally: Keep only (a) all PKIDB ligands or (b) all FDA-approved PKIDB ligands (while
    renaming all ligands to their names in PKIDB).

    Parameters
    ----------
    pkidb_ligands : bool
        Keep only PKIDB ligands (will rename ligands to their names in PKIDB). Default is False.
    fda_approved : bool
        Has only effect if `pkidb_ligands` is True. Keep only FDA-approved PKIDB ligands.
        Default is False.
    data_path : str or pathlib.Path
        Path to Davis dataset (JS file from KinMap).

    Returns
    -------
    pandas.DataFrame
        Davis profiling data for different kinases (rows) and ligands (columns).
    """
    return _kinmap_profiling(data_path, "davis", pkidb_ligands, fda_approved)


def _kinmap_profiling(data_path, data_name, pkidb_ligands=False, fda_approved=False):
    """
    Load profiling dataset from KinMap (JS file).
    Optionally: Keep only (a) all PKIDB ligands or (b) all FDA-approved PKIDB ligands (while
    renaming all ligands to their names in PKIDB).

    Parameters
    ----------
    data_path : str or pathlib.Path
        Path to profiling dataset (JS file from KinMap).
    data_name : str
        Dataset name as used in the JS file.
    pkidb_ligands : bool
        Keep only PKIDB ligands (will rename ligands to their names in PKIDB). Default is False.
    fda_approved : bool
        Has only effect if `pkidb_ligands` is True. Keep only FDA-approved PKIDB ligands.
        Default is False.

    Returns
    -------
    pandas.DataFrame
        Profiling data for different kinases (rows) and ligands (columns).
    """

    with open(data_path, "r") as f:
        json_string = f.read()

    json_string_cleaned = json_string.replace("=", ": ").replace(";", ", ").replace("\n", "")
    json_string_cleaned = json_string_cleaned.replace(
        f"{data_name}_compounds", f'"{data_name}_compounds"'
    )
    json_string_cleaned = json_string_cleaned.replace(
        f"{data_name}_profiling", f'"{data_name}_profiling"'
    )
    json_string_cleaned = json_string_cleaned[:-3] + "}"
    data_dict = json.loads(json_string_cleaned)

    data_df = {}
    for ligand, measures in data_dict[f"{data_name}_profiling"].items():
        data_df[ligand] = {measure["xName"]: measure["Kd(nM)"] for measure in measures}
    data_df = pd.DataFrame(data_df)

    if pkidb_ligands:
        ligand_names_new = ligands._pkidb_ligand_names(data_df.columns, fda_approved)
        # Cast column name for all unknown ligands to "unknown" and drop these columns
        ligand_names_new = [
            "unknown" if column_name.startswith("unknown") else column_name
            for column_name in ligand_names_new
        ]
        # Rename ligands
        data_df.columns = ligand_names_new
        # Remove ligands that could not be mapped to PKIDB
        data_df = data_df.drop("unknown", axis=1)
        data_df

    return data_df
