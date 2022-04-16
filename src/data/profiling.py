"""
Load profiling datasets (in unified output format).
"""

import logging
from pathlib import Path
import json

import pandas as pd
import numpy as np

from . import ligands, kinases

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent / "../../data/external/profiling"
KARAMAN_PATH = DATA_PATH / "Karaman/Karaman_profiling.js"
DAVIS_PATH = DATA_PATH / "Davis/Davis_profiling.js"
PKIS2_PATH = DATA_PATH / "PKIS2/pone.0181585.s004.xlsx"
MORET_PATH = DATA_PATH / "Moret/compound-library-2022-04-16.csv"


def load(dataset_name, pkidb_ligands=False, fda_approved=False, kinmap_kinases=False):
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
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).

    Returns
    -------
    pandas.DataFrame
        Profiling data for different kinases (rows) and ligands (columns).
    """

    if dataset_name == "karaman":
        return karaman(pkidb_ligands, fda_approved, kinmap_kinases)
    elif dataset_name == "davis":
        return davis(pkidb_ligands, fda_approved, kinmap_kinases)
    elif dataset_name == "karaman-davis":
        return karaman_davis(pkidb_ligands, fda_approved, kinmap_kinases)
    elif dataset_name == "moret":
        return moret(pkidb_ligands, fda_approved, kinmap_kinases)
    else:
        raise KeyError(
            "Unknown dataset name. Use 'karaman', 'davis', 'karaman-davis', or 'moret'."
        )


def karaman(pkidb_ligands=False, fda_approved=False, kinmap_kinases=False, data_path=KARAMAN_PATH):
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
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).
    data_path : str or pathlib.Path
        Path to Karaman dataset (JS file from KinMap).

    Returns
    -------
    pandas.DataFrame
        Karaman profiling data for different kinases (rows) and ligands (columns).
    """
    return _kinmap_profiling(data_path, "karaman", pkidb_ligands, fda_approved, kinmap_kinases)


def davis(pkidb_ligands=False, fda_approved=False, kinmap_kinases=False, data_path=DAVIS_PATH):
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
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).
    data_path : str or pathlib.Path
        Path to Davis dataset (JS file from KinMap).

    Returns
    -------
    pandas.DataFrame
        Davis profiling data for different kinases (rows) and ligands (columns).
    """
    return _kinmap_profiling(data_path, "davis", pkidb_ligands, fda_approved, kinmap_kinases)


def karaman_davis(
    pkidb_ligands=False,
    fda_approved=False,
    kinmap_kinases=False,
    activity_max=100,
    activity_diff=100,
):
    """
    Combine profiling data from Karaman and Davis datasets.
    - (1) If no measurement, return None.
    - (2) If one measurement, return that value.
    - (3) If two identical measurements, return that value.
    - (4) If both measurements are <= or > cutoff, keep lower value.
    - If one is below and one above,
      - (5) keep lower value if difference between values is <= cutoff,
      - (6) else remove measurements.

    Parameters
    ----------
    pkidb_ligands : bool
        Keep only PKIDB ligands (will rename ligands to their names in PKIDB). Default is False.
    fda_approved : bool
        Has only effect if `pkidb_ligands` is True. Keep only FDA-approved PKIDB ligands.
        Default is False.
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).
    activity_max : int
        Maximum cutoff for activity definition.
    activity_diff : int
        Allowed activity difference for case (5).

    Returns
    -------
    pandas.DataFrame
        Combined profiling data from Karaman and Davis datasets.
    """

    cases = {
        1: "No measurements",
        2: "One measurement",
        3: "Two identical measurements",
        4: f"Two measurements <= or > cutoff {activity_max}; keep lower value",
        5: (
            f"One measurement <=, one > cutoff {activity_max} "
            f"but difference <= {activity_diff}; keep lower value"
        ),
        6: (
            f"One measurement <=, one > cutoff {activity_max} "
            f"but difference > {activity_diff}; remove values"
        ),
    }

    def _choose_from_multiple_activities(x, activity_max=100, _stats=False):
        """
        Choose an activity from zero, one, or two activities.
        """

        if len(x) == 0:
            return None if not _stats else 1
        elif len(x) == 1:
            return x[0] if not _stats else 2
        else:
            if x[0] == x[1]:
                return x[0] if not _stats else 3
            else:
                # If both measurements are below or above cutoff, keep lower value
                if (x[0] > activity_max and x[1] > activity_max) or (
                    x[0] <= activity_max and x[1] <= activity_max
                ):
                    return min(x) if not _stats else 4
                # If one is below and one above
                else:
                    # Keep lower value if difference between values is <100
                    if abs(x[0] - x[1]) <= activity_diff:
                        return min(x) if not _stats else 5
                    # Else remove measurements completely (unreliable)
                    else:
                        return None if not _stats else 6

    df_karaman = karaman(pkidb_ligands, fda_approved, kinmap_kinases)
    logger.info(f"Karaman matrix: {df_karaman.shape}")
    df_davis = davis(pkidb_ligands, fda_approved, kinmap_kinases)
    logger.info(f"Davis matrix: {df_davis.shape}")

    logger.info(
        f"Number of shared ligands: {len(set(df_karaman.columns) & set(df_davis.columns))}"
    )
    logger.info(f"Number of shared kinases: {len(set(df_karaman.index) & set(df_davis.index))}")

    logger.info(
        f"Number of total ligands: {len(set(df_karaman.columns).union(set(df_davis.columns)))}"
    )
    logger.info(
        f"Number of total kinases: {len(set(df_karaman.index).union(set(df_davis.index)))}"
    )

    df_combined = pd.concat([df_karaman, df_davis])
    df_combined = (
        df_combined.reset_index()
        .groupby("index")
        .agg(lambda x: [i for i in x.tolist() if not np.isnan(i)])
    )
    logger.info(f"Karaman-Davis matrix: {df_combined.shape}")

    df_combined_selected = df_combined.applymap(
        lambda x: _choose_from_multiple_activities(x, activity_max)
    )
    df_combined_selected.index.name = None
    logger.info(f"Karaman-Davis matrix: {df_combined.shape}")

    # Print statistics on different cases
    stats = df_combined.applymap(
        lambda x: _choose_from_multiple_activities(x, activity_max, _stats=True)
    )
    logger.info(stats.unstack().value_counts().sort_index().rename(cases))

    return df_combined_selected


def _kinmap_profiling(
    data_path, data_name, pkidb_ligands=False, fda_approved=False, kinmap_kinases=False
):
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
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).

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
        data_df = _pkidb_ligands(data_df, fda_approved)
    if kinmap_kinases:
        data_df = _kinmap_kinases(data_df)

    return data_df


def _pkidb_ligands(profiling_df, fda_approved=False):
    """
    Cast ligand names in DataFrame (columns) to PKIDB ligand names.
    """

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


def _kinmap_kinases(profiling_df):
    """
    Cast kinase names in DataFrame (index) to KinMap kinase names.
    """

    kinase_names_new = kinases._kinmap_kinase_names(profiling_df.index)
    # Cast column name for all unknown kinases to "unknown" and drop these columns
    kinase_names_new = [
        "unknown" if column_name.startswith("unknown") else column_name
        for column_name in kinase_names_new
    ]
    # Rename kinases
    profiling_df.index = kinase_names_new
    # Remove kinases that could not be mapped to KinMap
    profiling_df = profiling_df.drop("unknown", axis=0)

    return profiling_df


def pkis2(kinmap_kinases=False, data_path=PKIS2_PATH):
    """
    Load PKIS2 dataset.
    TODO cast ligand names to PKIDB ligand names.

    Parameters
    ----------
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).
    data_path : str or pathlib.Path
        Path to PKIS2 dataset.

    Returns
    -------
    pandas.DataFrame
        PKIS2 profiling data for different kinases (rows) and ligands (columns).
    """

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
        df = _kinmap_kinases(df)

    return df


def moret(pkidb_ligands=False, fda_approved=False, kinmap_kinases=False, data_path=MORET_PATH):
    """
    Load Moret profiling dataset from [1]. Dataset was downloaded as described in
    ´kissim_app/data/external/profiling/Moret/README.md`.
    Optionally: Keep only (a) all PKIDB ligands or (b) all FDA-approved PKIDB ligands (while
    renaming all ligands to their names in PKIDB).

    [1] https://doi.org/10.1016/j.chembiol.2019.02.018

    Parameters
    ----------
    pkidb_ligands : bool
        Keep only PKIDB ligands (will rename ligands to their names in PKIDB). Default is False.
    fda_approved : bool
        Has only effect if `pkidb_ligands` is True. Keep only FDA-approved PKIDB ligands.
        Default is False.
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).
    data_path : str or pathlib.Path
        Path to Moret dataset.

    Returns
    -------
    pandas.DataFrame
        Moret profiling data for different kinases (rows) and ligands (columns).
    """

    data_df = pd.read_csv(data_path)
    # Sort kinase-ligand pairs by ascending IC50 values
    data_df = data_df.sort_values(["symbol", "name", "ontarget_ic50_q1"])
    # Per kinase-ligand pair select lowest IC50 value
    data_df = data_df.groupby(["symbol", "name"]).first().reset_index()

    # Transpose kinase-ligand pairs to kinase-ligand matrix
    matrix_df = data_df.pivot(index="symbol", columns="name", values="ontarget_ic50_q1")

    if pkidb_ligands:
        matrix_df = _pkidb_ligands(matrix_df, fda_approved)

    if kinmap_kinases:
        matrix_df = _kinmap_kinases(matrix_df)

    return matrix_df
