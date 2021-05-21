"""
Data container for ligand-kinase data.
"""

import logging

import pandas as pd

from src.evaluation.data.base_data import BaseData


logger = logging.getLogger(__name__)


class LigandVsKinaseData(BaseData):
    """
    TODO

    Attributes
    ----------
    ligand_query : str
        Ligand name (kinases are extracted from `ligand_kinase_matrix` by this ligand).
    kinase_query : str
        Kinase name (kinases are extracted from `kinase_kinase_matrix` by this kinase).
    ligand_kinase_method : str
        Name for ligand profiling method to be used as identifier.
    kinase_kinase_method : str
        Name for kinase distances method to be used as identifier.
    TODO
    """

    def __init__(
        self,
        ligand_query,
        kinase_query,
        ligand_kinase_method,
        kinase_kinase_method,
        ligand_kinase_matrix,
        kinase_kinase_matrix,
        kinase_activity_cutoff,
        kinase_activity_max,
    ):
        """
        TODO

        Parameters
        ----------
        ligand_query : str
            Ligand name (kinases are extracted from `ligand_kinase_matrix` by this ligand).
        kinase_query : str
            Kinase name (kinases are extracted from `kinase_kinase_matrix` by this kinase).
        ligand_kinase_method : str
            Name for ligand profiling method to be used as identifier.
        kinase_kinase_method : str
            Name for kinase distances method to be used as identifier.
        ligand_kinase_matrix : TODO
            TODO
        kinase_kinase_matrix : TODO
            TODO
        kinase_activity_cutoff : float
            Cutoff value to be used to determine activity. By default this cutoff is the maximum value.
            Set `kinase_activity_max=False` if cutoff is the minimum value.
        kinase_activity_max : bool
            If `True` (default), the `kinase_activity_cutoff` is used as the maximum cutoff, else as
            the minimum cutoff.
        """

        self.ligand_query = ligand_query
        self.kinase_query = kinase_query
        self.ligand_kinase_method = ligand_kinase_method
        self.kinase_kinase_method = kinase_kinase_method
        self.data = None
        self.n_kinases_by_kinase = None
        self.n_kinases_by_ligand = None
        self.n_kinases_shared = None
        self.n_active_kinases_shared = None
        (
            self.data,
            self.n_kinases_by_kinase,
            self.n_kinases_by_ligand,
            self.n_kinases_shared,
            self.n_active_kinases_shared,
        ) = self._merge_datasets(
            ligand_kinase_matrix,
            kinase_kinase_matrix,
            kinase_activity_cutoff,
            kinase_activity_max,
        )

    def _merge_datasets(
        self,
        ligand_kinase_matrix,
        kinase_kinase_matrix,
        kinase_activity_cutoff,
        kinase_activity_max,
    ):
        """
        Compare kinase ranks between a ligand profiling dataset and a kinase distances dataset.
        The profiling dataset contains kinases for the query ligand extracted from the ligand-kinase
        matrix. The distances dataset contains kinases for the query kinase extracted from the
        kinase-kinase matrix.

        Returns
        -------
        kinase_data : pandas.DataFrame
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
        n_kinases_by_kinase : int
            Number of kinases in kinase-kinase method
        n_kinases_by_ligand : int
            Number of kinases in ligand-kinase method
        n_kinases_shared : int
            Number of shared kinases
        n_active_kinases_shared : int
            Number of shared active kinases
        """

        # Load kinase data from kinase-kinase matrix (by query kinase)
        kinase_data_by_kinase = self._kinase_data_by_query_kinase(
            self.kinase_query, kinase_kinase_matrix
        )

        # Load kinase data from ligand-kinase matrix (by query ligand)
        ranks_by_ligand = self._kinase_data_by_query_ligand(
            self.ligand_query, ligand_kinase_matrix
        )
        if kinase_activity_max:
            ranks_by_ligand[f"active_{self.ligand_kinase_method}"] = (
                ranks_by_ligand[f"measure"] <= kinase_activity_cutoff
            )
        else:
            ranks_by_ligand[f"active_{self.ligand_kinase_method}"] = (
                ranks_by_ligand[f"measure"] >= kinase_activity_cutoff
            )

        # Merge two datasets while keeping only common kinases
        kinase_data = pd.merge(
            kinase_data_by_kinase,
            ranks_by_ligand,
            how="inner",
            on="kinase",
            suffixes=(f"_{self.kinase_kinase_method}", f"_{self.ligand_kinase_method}"),
        )
        kinase_data = kinase_data.set_index("kinase")

        # Now rank kinases again based only on the shared kinases
        kinase_data[f"rank2_{self.kinase_kinase_method}"] = kinase_data[
            f"measure_{self.kinase_kinase_method}"
        ].rank()
        kinase_data[f"rank2_{self.ligand_kinase_method}"] = kinase_data[
            f"measure_{self.ligand_kinase_method}"
        ].rank()

        # Rearange columns
        kinase_data = kinase_data[
            [
                f"measure_{self.ligand_kinase_method}",
                f"active_{self.ligand_kinase_method}",
                f"rank1_{self.ligand_kinase_method}",
                f"rank2_{self.ligand_kinase_method}",
                f"measure_{self.kinase_kinase_method}",
                f"rank1_{self.kinase_kinase_method}",
                f"rank2_{self.kinase_kinase_method}",
            ]
        ]
        kinase_data.columns = [f"{i.split('_')[1]}.{i.split('_')[0]}" for i in kinase_data.columns]

        # Log number of kinases for different criteria
        n_kinases_by_kinase = kinase_data_by_kinase.shape[0]
        n_kinases_by_ligand = ranks_by_ligand.shape[0]
        n_kinases_shared = kinase_data.shape[0]
        n_active_kinases_shared = kinase_data[
            kinase_data[f"{self.ligand_kinase_method}.active"]
        ].shape[0]

        # Sort rows by kinase-kinase method (DO NOT CHANGE!)
        kinase_data = kinase_data.sort_values(f"{self.kinase_kinase_method}.measure")

        return (
            kinase_data,
            n_kinases_by_kinase,
            n_kinases_by_ligand,
            n_kinases_shared,
            n_active_kinases_shared,
        )

    def _kinase_data_by_query_ligand(self, ligand_query, ligand_kinase_matrix):
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
            kinase_data = ligand_kinase_matrix[ligand_query]
            kinase_data = self._add_rank(kinase_data)
            return kinase_data
        except KeyError:
            logging.info(f"Query ligand {ligand_query} is not part of dataset.")
            raise KeyError(f"Query ligand {ligand_query} is not part of dataset.")
