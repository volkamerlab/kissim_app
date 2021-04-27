"""
Ranks kinases based on different measures.
"""

import logging

import pandas as pd

from ..data import distances

logger = logging.getLogger(__name__)


def profiling_vs_similarity_dataset(
    kinase_query,
    kinase_kinase_matrix,
    kinase_kinase_method,
    ligand_query,
    ligand_kinase_matrix,
    ligand_kinase_method,
    kinase_activity_cutoff=100.0,
):

    logging.warning(f"Input kinase/ligand: {kinase_query}/{ligand_query}")

    # Load datasets
    ranks_by_kinase = _ranked_kinases_by_query_kinase(kinase_query, kinase_kinase_matrix)
    logger.warning(
        f"Number of kinases in {kinase_kinase_method} dataset: {ranks_by_kinase.shape[0]}"
    )
    ranks_by_ligand = _ranked_kinases_by_query_ligand(ligand_query, ligand_kinase_matrix)
    ranks_by_ligand[f"active_{ligand_kinase_method}"] = (
        ranks_by_ligand[f"measure"] <= kinase_activity_cutoff
    )
    logger.warning(
        f"Number of kinases in {ligand_kinase_method} dataset: {ranks_by_ligand.shape[0]}"
    )

    # Merge two datasets while keeping only common kinases
    ranks = pd.merge(
        ranks_by_kinase,
        ranks_by_ligand,
        how="inner",
        on="kinase",
        suffixes=(f"_{kinase_kinase_method}", f"_{ligand_kinase_method}"),
    )
    ranks = ranks.set_index("kinase")
    logger.warning(f"Number of shared kinases in both datasets: {ranks.shape[0]}")

    # Now rank kinases again based only on the shared kinases
    ranks[f"rank2_{kinase_kinase_method}"] = ranks[f"measure_{kinase_kinase_method}"].rank()
    ranks[f"rank2_{ligand_kinase_method}"] = ranks[f"measure_{ligand_kinase_method}"].rank()

    # Rearange columns
    ranks = ranks[
        [
            f"measure_{kinase_kinase_method}",
            f"rank1_{kinase_kinase_method}",
            f"rank2_{kinase_kinase_method}",
            f"measure_{ligand_kinase_method}",
            f"active_{ligand_kinase_method}",
            f"rank1_{ligand_kinase_method}",
            f"rank2_{ligand_kinase_method}",
        ]
    ]
    ranks.columns = [f"{i.split('_')[1]}.{i.split('_')[0]}" for i in ranks.columns]

    ranks = ranks.sort_values(f"{ligand_kinase_method}.measure")

    return ranks


def similarity_vs_similarity_dataset(
    kinase_query,
    kinase_kinase_matrix1,
    kinase_kinase_method1,
    kinase_kinase_matrix2,
    kinase_kinase_method2,
):
    pass


def _ranked_kinases_by_query_kinase(query_kinase, kinase_kinase_matrix):

    ranks = kinase_kinase_matrix[query_kinase]
    ranks = _ranked_kinases(ranks)

    return ranks


def _ranked_kinases_by_query_ligand(query_ligand, ligand_kinase_matrix):

    ranks = ligand_kinase_matrix[query_ligand]
    ranks = _ranked_kinases(ranks)

    return ranks


def _ranked_kinases(ranks):

    ranks = ranks.reset_index()
    ranks.columns = ["kinase", "measure"]
    ranks = ranks.dropna(subset=["measure"])
    ranks["rank1"] = ranks["measure"].rank()

    return ranks
