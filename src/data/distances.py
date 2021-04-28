"""
Load kinase distances matrices.
"""

import logging
from pathlib import Path

import pandas as pd
from kissim.comparison import FingerprintDistanceGenerator

from . import kinases

logger = logging.getLogger(__name__)

RESULTS_PATH = Path(__file__).parent / "../../results"
KISSIM_PATH = RESULTS_PATH / "fingerprint_distances.json"


def kissim(
    structure_kinase_mapping_by="minimum", kinmap_kinases=False, distances_path=KISSIM_PATH
):
    """
    Get kinase distance matrix from `kissim` using a user-defined structure-kinase mapping method.

    Parameters
    ----------
    structure_kinase_mapping_by : str
        Structure-kinase mapping method (default: minimum).
    kinmap_kinases : bool
        Map kinase names to KinMap kinase names (default: False).
    distances_path : str or pathlib.Path
        Path to fingerprint distances JSON `kissim` file.
    """

    fingerprint_distance_generator = FingerprintDistanceGenerator.from_json(distances_path)
    kissim_df = fingerprint_distance_generator.kinase_distance_matrix(structure_kinase_mapping_by)

    if kinmap_kinases:
        kinase_names_new = kinases._kinmap_kinase_names(kissim_df.columns)
        # Cast column name for all unknown kinases to "unknown" and drop these columns
        kinase_names_new = [
            "unknown" if column_name.startswith("unknown") else column_name
            for column_name in kinase_names_new
        ]
        # Rename kinases
        kissim_df.columns = kinase_names_new
        kissim_df.index = kinase_names_new
        # Remove kinases that could not be mapped to KinMap
        kissim_df = kissim_df.drop("unknown", axis=0).drop("unknown", axis=1)
        kissim_df

    return kissim_df
