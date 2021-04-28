"""
Load kinase datasets.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)

KINMAP_URL = (
    "https://raw.githubusercontent.com/openkinome/kinodata/master/data/KinHubKinaseList.csv"
)


def kinmap(kinmap_url=KINMAP_URL):
    """
    Load KinMap kinase dataset.

    Parameters
    ----------
    kinmap_url : str
        KinMap URL for kinase dataset.

    Returns
    -------
    pandas.DataFrame
        KinMap kinases (rows) with their KinMap kinase name ("xName"), "Manning Name", "HGNC Name",
        full kinase name ("Kinase Name"), kinase group, family and subfamily ("Group", "Family",
        "SubFamily") and "UniProtID".
    """

    kinmap_df = pd.read_csv(kinmap_url)
    return kinmap_df


def _kinmap_kinase_names(kinase_names):
    """
    Cast given ligand names to the PKIDB ligand IDs.

    Parameters
    ----------
    kinase_names : list of str
        List of kinase names.

    Returns
    -------
    list of str
        List of KinMap kinase names.
    """

    kinmap_df = kinmap()
    kinmap_kinase_names = [
        _kinmap_kinase_name(kinase_name, kinmap_df) for kinase_name in kinase_names
    ]

    change_log = pd.DataFrame({"kinase.input": kinase_names, "kinase.kinmap": kinmap_kinase_names})
    change_log = change_log[change_log["kinase.input"] != change_log["kinase.kinmap"]]
    if change_log.shape[0] > 0:
        logger.warning(f"Changed kinase names (unknown names may be discarded):\n{change_log}")

    return kinmap_kinase_names


def _kinmap_kinase_name(kinase_name, kinmap_df):
    """
    Cast a given kinase name to the KinMap kinase name.

    Parameters
    ----------
    kinase_name : str
        Kinase name.
    kinmap_df : pandas.DataFrame
        Kinase data (columns) for all KinMap kinases (rows) from `kinases.kinmap()`.

    Returns
    -------
    str
        KinMap kinase name. If input kinase name unknown or ambiguous return "unknown (why?)".
    """

    kinase_name = kinase_name.replace("-", "_")
    if kinmap_df["xName"].isin([kinase_name]).any():
        return kinase_name
    else:
        kinase_name_kinmap = kinmap_df[
            (kinmap_df["Manning\xa0Name"] == kinase_name)
            | (kinmap_df["HGNC\xa0Name"] == kinase_name)
        ]
        if len(kinase_name_kinmap) == 0:
            return "unknown (not in KinMap)"
        elif len(kinase_name_kinmap) == 1:
            return kinase_name_kinmap.squeeze()["xName"]
        else:
            return "unknown (ambiguous kinase name)"