"""
Load profiling datasets (in unified output format).
"""

import logging

import json
import pandas as pd

from pathlib import Path

from . import ligands

logger = logging.getLogger(__name__)

PATH_DATA = Path(__name__).parent / "../../data/external/profiling"
PATH_DATA_KARAMAN = PATH_DATA / "Karaman/Karaman_profiling.js"


def karaman(pkidb_ligands=False, fda_approved=False):
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

    Returns
    -------
    pandas.DataFrame
        Karaman profiling data for different kinases (rows) and ligands (columns).
    """

    with open(PATH_DATA_KARAMAN, "r") as f:
        json_string = f.read()

    json_string_cleaned = json_string.replace("=", ": ").replace(";", ", ").replace("\n", "")
    json_string_cleaned = json_string_cleaned.replace("karaman_compounds", '"karaman_compounds"')
    json_string_cleaned = json_string_cleaned.replace("karaman_profiling", '"karaman_profiling"')
    json_string_cleaned = json_string_cleaned[:-3] + "}"
    karaman_dict = json.loads(json_string_cleaned)

    karaman_df = {}
    for ligand, measures in karaman_dict["karaman_profiling"].items():
        karaman_df[ligand] = {measure["xName"]: measure["Kd(nM)"] for measure in measures}
    karaman_df = pd.DataFrame(karaman_df)

    if pkidb_ligands:
        ligand_names_new = ligands._pkidb_ligand_names(karaman_df.columns, fda_approved)
        # Cast column name for all unknown ligands to "unknown" and drop these columns
        ligand_names_new = [
            "unknown" if column_name.startswith("unknown") else column_name
            for column_name in ligand_names_new
        ]
        # Rename ligands
        karaman_df.columns = ligand_names_new
        # Remove ligands that could not be mapped to PKIDB
        karaman_df = karaman_df.drop("unknown", axis=1)
        karaman_df

    return karaman_df
