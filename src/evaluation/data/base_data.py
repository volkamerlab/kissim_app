"""
Basic data container; parent class for kinase-kinase and ligand-kinase data.
"""


import logging

logger = logging.getLogger(__name__)


class BaseData:
    """
    Handles basic data properties.
    """

    def __init__(self):
        pass

    def _kinase_data_by_query_kinase(self, kinase_query, kinase_kinase_matrix):
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
            kinase_data = kinase_kinase_matrix[kinase_query]
            kinase_data = self._add_rank(kinase_data)
            return kinase_data
        except KeyError:
            raise KeyError(f"Query kinase {kinase_query} is not part of dataset.")

    @staticmethod
    def _add_rank(kinase_data):
        """
        Add ranks to kinase data.
        """

        kinase_data = kinase_data.reset_index()
        kinase_data.columns = ["kinase", "measure"]
        kinase_data = kinase_data.dropna(subset=["measure"])
        kinase_data["rank1"] = kinase_data["measure"].rank()

        return kinase_data
