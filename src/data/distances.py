"""
Load kinase distances matrices.
- KiSSim
- KLIFS pocket seq
- KLIFS pocket IFP
- SiteAlign pocket structure
"""

import logging

import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from opencadd.databases import klifs

from . import kinases
from src.definitions import COVERAGE_CUTOFF
from src.paths import PATH_RESULTS, PATH_DATA

logger = logging.getLogger(__name__)

PATH_KISSIM = PATH_RESULTS / "dfg_in/fingerprint_distances_to_kinase_matrix.csv"
PATH_SITEALIGN = PATH_DATA / "external/sitealign/sitealign_kinase_distance_matrix.csv"


def load(
    dataset_name,
    kinmap_kinases=False,
    distances_path=None,
):
    """
    Utility function to load different kinase similarity datasets via the same API.


    Parameters
    ----------
    dataset_name : str
        Dataset name: 'kissim' or 'xxx'
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).
    distances_path : str or pathlib.Path or None
        Path to dataset file. If None, use default path for respective dataset.

    Returns
    -------
    pandas.DataFrame
        Profiling data for different kinases (rows) and ligands (columns).
    """

    dataset_names = [
        "kissim",
        "klifs-pocket-sequence",
        "klifs-pocket-ifp",
        "sitealign-pocket-structure",
    ]

    # DO NOT USE underscores in dataset name
    if dataset_name == dataset_names[0]:
        if distances_path is None:
            distances_path = PATH_KISSIM
        return kissim(kinmap_kinases, distances_path)
    elif dataset_name == dataset_names[1]:
        return klifs_pocket_sequence(kinmap_kinases=kinmap_kinases)
    elif dataset_name == dataset_names[2]:
        return klifs_pocket_ifp(kinmap_kinases=kinmap_kinases)
    elif dataset_name == dataset_names[3]:
        return sitealign_pocket_structure(kinmap_kinases=kinmap_kinases)
    else:
        raise KeyError(f"Unknown dataset name. Use one of these: {', '.join(dataset_names)}.")


def kissim(
    kinmap_kinases=False,
    distances_path=PATH_KISSIM,
):
    """
    Get kinase distance matrix from `kissim` using a user-defined structure-kinase mapping method.

    Parameters
    ----------
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).
    distances_path : str or pathlib.Path
        Path to fingerprint distances CSV `kissim` file.

    Returns
    -------
    pandas.DataFrame
        Kinase distance matrix.
    """

    distance_matrix = pd.read_csv(distances_path, index_col=0)

    if kinmap_kinases:
        distance_matrix = _use_kinmap_kinase_names(distance_matrix)

    return distance_matrix


def klifs_pocket_sequence(kinmap_kinases=False):
    """
    Get kinase distance matrix describing the KLIFS pocket sequence identity.

    Parameters
    ----------
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).

    Returns
    -------
    pandas.DataFrame
        Kinase distance matrix.
    """

    logger.info("Set up KLIFS session...")
    klifs_session = klifs.setup_remote()
    logger.info("Fetch kinases...")
    kinase_klifs_ids = klifs_session.kinases.all_kinases(species="Human")[
        "kinase.klifs_id"
    ].to_list()
    kinases = klifs_session.kinases.by_kinase_klifs_id(kinase_klifs_ids)
    logger.info(f"Number of kinases: {len(kinases)}")
    kinases = kinases[kinases["kinase.pocket"].apply(len) == 85]
    logger.info(f"Number of kinases with full pocket sequence: {len(kinases)}")

    logger.info("Calculate kinase matrix...")
    seq_matrix = kinases["kinase.pocket"].apply(list)
    X = np.array(seq_matrix.to_list())
    # Expand: Identical position?
    identity = X[:, None, :] == X[None, :, :]
    # Reduce
    similarity_matrix = identity.sum(axis=-1) / X.shape[1]
    # Similarity > distances
    distance_matrix = 1 - similarity_matrix
    kinase_names = kinases["kinase.klifs_name"].to_list()
    distance_matrix = pd.DataFrame(distance_matrix, index=kinase_names, columns=kinase_names)

    if kinmap_kinases:
        distance_matrix = _use_kinmap_kinase_names(distance_matrix)

    return distance_matrix


def klifs_pocket_ifp(structure_klifs_ids=None, dfg="in", metric="jaccard", kinmap_kinases=False):
    """
    Get kinase distance matrix describing the KLIFS pocket IFP similarity.

    Parameters
    ----------
    structure_klifs_ids : list of int or None
        KLIFS structures to be used for the comparison.
        If None, use all structures that have an IFP.
    dfg : str
        DFG conformation: in (default) or out.
    metric : str
        Distance metrics as allowed in sklearn.metrics.pairwise_distances.
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).

    Returns
    -------
    pandas.DataFrame
        Kinase distance matrix.
    """

    logger.info("Set up KLIFS session...")
    klifs_session = klifs.setup_remote()
    logger.info("Fetch IFPs...")
    if structure_klifs_ids is None:
        ifps = klifs_session.interactions.all_interactions()
    else:
        ifps = klifs_session.interactions.by_structure_klifs_id(structure_klifs_ids)
    # Drop structures without IFPs
    ifps.dropna(subset=["interaction.fingerprint"], inplace=True)
    structure_klifs_ids = ifps["structure.klifs_id"].to_list()

    logger.info(f"Fetch structures and keep IFPs in DFG-{dfg} only...")
    structures = klifs_session.structures.by_structure_klifs_id(structure_klifs_ids)
    structures = structures[
        (structures["structure.dfg"] == dfg) & (structures["species.klifs"] == "Human")
    ]
    # Drop IFP columns in `structures` (is empty when fetched from remote KLIFS session);
    # We will use the IFP column in `ifps` instead
    structures = structures.drop("interaction.fingerprint", axis=1)

    # Merge IFP and structure data
    ifps = ifps.merge(structures, on="structure.klifs_id", how="inner")
    ifps = ifps.set_index(["structure.klifs_id", "kinase.klifs_name"])

    logger.info("Calculate structure distance matrix...")
    # Generate list of lists
    ifps_list_of_lists = (
        ifps["interaction.fingerprint"]
        .apply(list)
        .apply(lambda x: [True if i == "1" else False for i in x])
        .to_list()
    )
    # Convert to array
    ifps_array = np.array(ifps_list_of_lists)

    # Calculate pairwise distances
    structure_distance_matrix = pairwise_distances(ifps_array, metric=metric)
    # Create DataFrame with structure KLIFS IDs as index/columns
    structure_klifs_ids = ifps.index.get_level_values(0)
    structure_distance_matrix = pd.DataFrame(
        structure_distance_matrix, index=structure_klifs_ids, columns=structure_klifs_ids
    )
    logger.info(f"Structure matrix: {structure_distance_matrix.shape}")

    logger.info("Calculate kinase distance matrix...")
    # Copy distance matrix to kinase matrix
    kinase_distance_matrix = structure_distance_matrix
    # Replace structure KLIFS IDs with the structures' kinase names
    kinase_names = ifps.index.get_level_values(1)
    kinase_distance_matrix.index = kinase_names
    kinase_distance_matrix.columns = kinase_names
    # Select the minimum structure pair distance for each kinase pair
    kinase_distance_matrix = (
        kinase_distance_matrix.stack().groupby(level=[0, 1]).min().unstack(level=1)
    )
    logger.info(f"Kinase matrix: {kinase_distance_matrix.shape}")

    if kinmap_kinases:
        kinase_distance_matrix = _use_kinmap_kinase_names(kinase_distance_matrix)

    return kinase_distance_matrix


def sitealign_pocket_structure(kinmap_kinases=False):
    """
    Get kinase distance matrix describing the KLIFS pocket IFP similarity.

    Parameters
    ----------
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).

    Returns
    -------
    pandas.DataFrame
        Kinase distance matrix.
    """

    kinase_distance_matrix = pd.read_csv(PATH_SITEALIGN, index_col=0)

    if kinmap_kinases:
        kinase_distance_matrix = _use_kinmap_kinase_names(kinase_distance_matrix)

    return kinase_distance_matrix


def _use_kinmap_kinase_names(kinase_df):

    kinase_names_new = kinases._kinmap_kinase_names(kinase_df.columns)
    # Cast column name for all unknown kinases to "unknown" and drop these columns
    kinase_names_new = [
        "unknown" if column_name.startswith("unknown") else column_name
        for column_name in kinase_names_new
    ]
    # Rename kinases
    kinase_df.columns = kinase_names_new
    kinase_df.index = kinase_names_new
    # Remove kinases that could not be mapped to KinMap
    if "unknown" in kinase_df.columns:
        kinase_df = kinase_df.drop("unknown", axis=0).drop("unknown", axis=1)

    return kinase_df
