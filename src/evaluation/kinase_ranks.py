"""
Ranks kinases based on different measures.
"""

import logging

import pandas as pd

from ..data import distances

logger = logging.getLogger(__name__)


def kinase_ranks_by_ligand_vs_kinase_data(
    ligand_query,
    kinase_query,
    ligand_kinase_matrix,
    kinase_kinase_matrix,
    ligand_kinase_method,
    kinase_kinase_method,
    kinase_activity_cutoff,
    kinase_activity_max=True,
):
    """
    Compare kinase ranks between a ligand profiling dataset and a kinase distances dataset.
    The profiling dataset contains kinases for the query ligand extracted from the ligand-kinase
    matrix. The distances dataset contains kinases for the query kinase extracted from the
    kinase-kinase matrix.

    Parameters
    ----------
    ligand_query : str
        Ligand name (kinases are extracted from `ligand_kinase_matrix` by this ligand).
    kinase_query : str
        Kinase name (kinases are extracted from `kinase_kinase_matrix` by this kinase).
    ligand_kinase_matrix : pandas.DataFrame
        Profiling data for a ligand set against a kinase set loaded from `src.data.profiling`.
    kinase_kinase_matrix : pandas.DataFrame
        Pairwise kinase distances values loaded from `src.data.distances`.
    ligand_kinase_method : str
        Name for ligand profiling method to be used as identifier.
    kinase_kinase_method : str
        Name for kinase distances method to be used as identifier.
    kinase_activity_cutoff : float
        Cutoff value to be used to determine activity. By default this cutoff is the maximum value.
        Set `kinase_activity_max=False` if cutoff is the minimum value.
    kinase_activity_max : bool
        If `True` (default), the `kinase_activity_cutoff` is used as the maximum cutoff, else as
        the minimum cutoff.

    Returns
    -------
    ranks : pandas.DataFrame
        Contains for each kinase (rows) details on profiling and distances ranks (columns):
        <ligand_kinase_method>.measure : float
            Ligand profiling data.
        <ligand_kinase_method>.active : bool
            Active kinase?
        <ligand_kinase_method>.rank1 : float
            Kinase rank by profiling data based on all ligand-kinase method data points.
        <ligand_kinase_method>.rank2 : float
            Kinase rank by profiling distances based on shared data points only.
        <kinase_kinase_method>.measure : float
            Kinase distances
        <kinase_kinase_method>.rank1 : float
            Kinase rank by kinase distances based on all kinase-kinase method data points.
        <kinase_kinase_method>.rank2 : float
            Kinase rank by kinase distances based on shared data points only.
    log : list
        - Kinase name
        - Ligand name
        - Number of kinases in kinase-kinase method
        - Number of kinases in ligand-kinase method
        - Number of shared kinases
        - Number of shared active kinases
    """

    # Load datasets
    ranks_by_kinase = _ranked_kinases_by_query_kinase(kinase_query, kinase_kinase_matrix)
    n_kinases_by_kinase = ranks_by_kinase.shape[0]
    ranks_by_ligand = _ranked_kinases_by_query_ligand(ligand_query, ligand_kinase_matrix)
    if kinase_activity_max:
        ranks_by_ligand[f"active_{ligand_kinase_method}"] = (
            ranks_by_ligand[f"measure"] <= kinase_activity_cutoff
        )
    else:
        ranks_by_ligand[f"active_{ligand_kinase_method}"] = (
            ranks_by_ligand[f"measure"] >= kinase_activity_cutoff
        )
    n_kinases_by_ligand = ranks_by_ligand.shape[0]

    # Merge two datasets while keeping only common kinases
    ranks = pd.merge(
        ranks_by_kinase,
        ranks_by_ligand,
        how="inner",
        on="kinase",
        suffixes=(f"_{kinase_kinase_method}", f"_{ligand_kinase_method}"),
    )
    ranks = ranks.set_index("kinase")

    # Now rank kinases again based only on the shared kinases
    ranks[f"rank2_{kinase_kinase_method}"] = ranks[f"measure_{kinase_kinase_method}"].rank()
    ranks[f"rank2_{ligand_kinase_method}"] = ranks[f"measure_{ligand_kinase_method}"].rank()

    # Rearange columns
    ranks = ranks[
        [
            f"measure_{ligand_kinase_method}",
            f"active_{ligand_kinase_method}",
            f"rank1_{ligand_kinase_method}",
            f"rank2_{ligand_kinase_method}",
            f"measure_{kinase_kinase_method}",
            f"rank1_{kinase_kinase_method}",
            f"rank2_{kinase_kinase_method}",
        ]
    ]
    ranks.columns = [f"{i.split('_')[1]}.{i.split('_')[0]}" for i in ranks.columns]

    # Log number of kinases for different criteria
    n_kinases_shared = ranks.shape[0]
    n_active_kinases_shared = ranks[ranks[f"{ligand_kinase_method}.active"]].shape[0]
    log = [n_kinases_by_kinase, n_kinases_by_ligand, n_kinases_shared, n_active_kinases_shared]

    # Sort rows (by profiling data)
    ranks = ranks.sort_values(f"{kinase_kinase_method}.measure")

    return ranks, log


def kinase_ranks_by_kinase_vs_kinase_data(
    kinase_query,
    kinase_kinase_matrix1,
    kinase_kinase_method1,
    kinase_kinase_matrix2,
    kinase_kinase_method2,
):
    pass


def _ranked_kinases_by_query_kinase(kinase_query, kinase_kinase_matrix):
    """
    Select kinase data based on query kinase and rank by distances.


    Parameters
    ----------
    kinase_query : str
        Kinase name (kinases are extracted from `kinase_kinase_matrix` by this kinase).
    kinase_kinase_matrix : pandas.DataFrame
        Pairwise kinase distances values loaded from `src.data.distances`.

    Returns
    -------
    pandas.DataFrame
        Contains for each kinase (rows) details on profiling and distances ranks (columns):
        kinase : name
            Kinase name.
        measure : float
            Kinase distances
        rank1 : float
            Kinase rank by kinase distances based on all kinase-kinase method data points.
    """

    try:
        ranks = kinase_kinase_matrix[kinase_query]
        ranks = _ranked_kinases(ranks)
        return ranks
    except KeyError:
        logging.info(f"Query kinase {kinase_query} is not part of dataset.")
        raise KeyError(f"Query kinase {kinase_query} is not part of dataset.")


def _ranked_kinases_by_query_ligand(ligand_query, ligand_kinase_matrix):
    """

    Parameters
    ----------
    ligand_query : str
        Ligand name (kinases are extracted from `ligand_kinase_matrix` by this ligand).
    ligand_kinase_matrix : pandas.DataFrame
        Profiling data for a ligand set against a kinase set loaded from `src.data.profiling`.

    Returns
    -------
    pandas.DataFrame
        Contains for each kinase (rows) details on profiling and distances ranks (columns):
        kinase : name
            Kinase name.
        measure : float
            Ligand profiling data.
        rank1 : float
            Kinase rank by profiling data based on all ligand-kinase method data points.
    """

    try:
        ranks = ligand_kinase_matrix[ligand_query]
        ranks = _ranked_kinases(ranks)
        return ranks
    except KeyError:
        logging.info(f"Query ligand {ligand_query} is not part of dataset.")
        raise KeyError(f"Query ligand {ligand_query} is not part of dataset.")


def _ranked_kinases(ranks):

    ranks = ranks.reset_index()
    ranks.columns = ["kinase", "measure"]
    ranks = ranks.dropna(subset=["measure"])
    ranks["rank1"] = ranks["measure"].rank()

    return ranks


def curate_ligand_kinase_pairs(
    ligand_kinase_pairs,
    ligand_kinase_matrix,
    kinase_kinase_matrix,
    ligand_kinase_method,
    kinase_kinase_method,
    kinase_activity_cutoff,
    kinase_activity_max=True,
    min_n_shared_kinases=10,
    min_n_shared_active_kinases=3,
):
    """
    Curate input ligand-kinase pairs. Keep only pair that
    - have a minimum of `min_n_shared_kinases` shared kinases
    - have a minimum of `min_n_shared_active_kinases` shared active kinases, while activity is
      defined as <=/=> `min_n_shared_kinases` with `kinase_activity_max=True/False`, respectively

    Parameters
    ----------
    ligand_kinase_pairs : list of tuple
        One or more ligand and kinase name pairs.
    ligand_kinase_matrix : pandas.DataFrame
        Profiling data for a ligand set against a kinase set loaded from `src.data.profiling`.
    kinase_kinase_matrix : pandas.DataFrame
        Pairwise kinase distances values loaded from `src.data.distances`.
    ligand_kinase_method : str
        Name for ligand profiling method to be used as identifier.
    kinase_kinase_method : str
        Name for kinase distances method to be used as identifier.
    kinase_activity_cutoff : float
        Cutoff value to be used to determine activity. By default this cutoff is the maximum value.
        Set `kinase_activity_max=False` if cutoff is the minimum value.
    kinase_activity_max : bool
        If `True` (default), the `kinase_activity_cutoff` is used as the maximum cutoff, else as
        the minimum cutoff.
    min_n_shared_kinases : int
        Datasets must share at least `min_n_shared_kinases` kinases.
    min_n_shared_active_kinases : int
        Datasets must share at least `min_n_shared_active_kinases` active kinases.

    Returns
    -------
    list of tuple
        Curate list of ligand and kinase name pairs.
    """

    ligand_kinase_logs = []
    for ligand_name, kinase_name in ligand_kinase_pairs:
        try:
            _, log = kinase_ranks_by_ligand_vs_kinase_data(
                ligand_name,
                kinase_name,
                ligand_kinase_matrix,
                kinase_kinase_matrix,
                ligand_kinase_method,
                kinase_kinase_method,
                kinase_activity_cutoff,
                kinase_activity_max,
            )
            ligand_kinase_logs.append([ligand_name, kinase_name] + log)
        except KeyError:
            pass

    ligand_kinase_logs = pd.DataFrame(
        ligand_kinase_logs,
        columns=[
            "kinase",
            "ligand",
            "#kinases in kissim",
            "#kinases in karaman",
            "#kinases shared",
            "#active kinases shared",
        ],
    )
    ligand_kinase_logs = ligand_kinase_logs.set_index(["kinase", "ligand"])
    ligand_kinase_logs_selected = ligand_kinase_logs[
        (ligand_kinase_logs["#kinases shared"] >= min_n_shared_kinases)
        & (ligand_kinase_logs["#active kinases shared"] > min_n_shared_active_kinases)
    ]

    return ligand_kinase_logs_selected.index.to_list()