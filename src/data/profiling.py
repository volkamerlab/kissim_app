"""
Load profiling datasets (in unified output format).
"""

import logging
from pathlib import Path
import json

import pandas as pd

from . import ligands, kinases

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent / "../../data/external/profiling"
KARAMAN_PATH = DATA_PATH / "Karaman/Karaman_profiling.js"
DAVIS_PATH = DATA_PATH / "Davis/Davis_profiling.js"
PKIS2_PATH = DATA_PATH / "PKIS2/pone.0181585.s004.xlsx"


def load(dataset_name, pkidb_ligands=False, fda_approved=False):
    """
    Utility function to load different profiling datasets via the same API.

    Parameters
    ----------
    dataset_name : str
        Dataset name: 'karaman' or 'davis'
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

    if dataset_name == "karaman":
        return karaman(pkidb_ligands, fda_approved)
    elif dataset_name == "davis":
        return davis(pkidb_ligands, fda_approved)
    else:
        raise KeyError("Unknown dataset name. Use 'karaman' or 'davis'.")


def karaman(pkidb_ligands=False, fda_approved=False, data_path=KARAMAN_PATH):
    """
    Load Karaman profiling dataset [1] from KinMap [2].
    Optionally: Keep only (a) all PKIDB ligands or (b) all FDA-approved PKIDB ligands (while
    renaming all ligands to their names in PKIDB).

    [1] https://www.nature.com/articles/nbt1358
    [2] https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-016-1433-7

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
    Load Davis profiling dataset [1] from KinMap [2].
    Optionally: Keep only (a) all PKIDB ligands or (b) all FDA-approved PKIDB ligands (while
    renaming all ligands to their names in PKIDB).

    [1] https://www.nature.com/articles/nbt.1990
    [2] https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-016-1433-7

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
        data_df = _pkidb_ligands(data_df, fda_approved=False)

    return data_df


def _pkidb_ligands(profiling_df, fda_approved=False):

    ligand_names_new = ligands._pkidb_ligand_names(profiling_df.columns, fda_approved)
    # Cast column name for all unknown ligands to "unknown" and drop these columns
    ligand_names_new = [
        "unknown" if column_name.startswith("unknown") else column_name
        for column_name in ligand_names_new
    ]
    # Rename ligands
    profiling_df.columns = ligand_names_new
    # Remove ligands that could not be mapped to PKIDB
    profiling_df = profiling_df.drop("unknown", axis=1)

    return profiling_df


def pkis2(kinmap_kinases=False, data_path=PKIS2_PATH):

    df = pd.read_excel(data_path)
    # Remove empty line
    df = df[:-1]
    # Set compound name as index and drop a few columns
    df = df.set_index("Compound")
    df = df.iloc[:, 6:]
    # Transpose matrix and set columns/index name
    df = df.transpose()
    df.columns.name = "compound"
    df.index.name = "kinase"

    # Delete information in brackets
    """
    Affects the following kinases:
    [
        'GCN2(Kin.Dom.2,S808G)',
        'JAK1(JH1domain-catalytic)',
        'JAK1(JH2domain-pseudokinase)',
        'JAK2(JH1domain-catalytic)',
        'JAK3(JH1domain-catalytic)',
        'RPS6KA4(Kin.Dom.1-N-terminal)',
        'RPS6KA4(Kin.Dom.2-C-terminal)',
        'RPS6KA5(Kin.Dom.1-N-terminal)',
        'RPS6KA5(Kin.Dom.2-C-terminal)',
        'RSK1(Kin.Dom.1-N-terminal)',
        'RSK1(Kin.Dom.2-C-terminal)',
        'RSK2(Kin.Dom.1-N-terminal)',
        'RSK2(Kin.Dom.2-C-terminal)',
        'RSK3(Kin.Dom.1-N-terminal)',
        'RSK3(Kin.Dom.2-C-terminal)',
        'RSK4(Kin.Dom.1-N-terminal)',
        'RSK4(Kin.Dom.2-C-terminal)',
        'TYK2(JH1domain-catalytic)',
        'TYK2(JH2domain-pseudokinase)'
    ]
    """
    query = "("
    kinase_names = df.index
    kinase_names = [
        kinase_name.split(query)[0] if contains_query else kinase_name
        for kinase_name, contains_query in zip(
            kinase_names, kinase_names.str.contains(f"\\{query}")
        )
    ]
    df.index = kinase_names

    # Convert abbreviate Greek letters
    df_index = df.index
    df_index = df_index.str.replace("-alpha", "a")
    df_index = df_index.str.replace("-beta", "b")
    df_index = df_index.str.replace("-delta", "d")
    df_index = df_index.str.replace("-gamma", "g")
    df_index = df_index.str.replace("-epsilon", "e")
    df.index = df_index

    # Delete information after dash
    """
    Affects the following kinases:
    [
        'ABL1-nonphosphorylated',
        'ABL1-phosphorylated',
        'CDK4-cyclinD1',
        'CDK4-cyclinD3',
        'CSF1R-autoinhibited',
        'FLT3-autoinhibited',
        'KIT-autoinhibited'
    ]
    """
    query = "-"
    kinase_names = df.index
    kinase_names = [
        kinase_name.split(query)[0] if contains_query else kinase_name
        for kinase_name, contains_query in zip(kinase_names, kinase_names.str.contains(query))
    ]
    df.index = kinase_names

    # Drop duplicate kinases (keep first)
    df = df.reset_index().drop_duplicates("index").set_index("index")
    df.index.name = "kinase"

    if kinmap_kinases:
        kinase_names_new = kinases._kinmap_kinase_names(df.index)
        # Cast column name for all unknown kinases to "unknown" and drop these columns
        kinase_names_new = [
            "unknown" if column_name.startswith("unknown") else column_name
            for column_name in kinase_names_new
        ]
        # Rename kinases
        df.index = kinase_names_new
        # Remove kinases that could not be mapped to KinMap
        df = df.drop("unknown", axis=0)

    return df
