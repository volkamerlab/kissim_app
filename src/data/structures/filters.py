"""
Defines filters for the KLIFS dataset.
"""

from functools import wraps
import datetime
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def log_step(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        time_taken = str(start_time - end_time)
        logger.info(f"{func.__name__:<30}{result.shape[0]:>7} structures ({time_taken}s)")
        return result

    return wrapper


@log_step
def make_copy(dataframe):
    """
    Make a copy of the input DataFrame.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    pandas.DataFrame
        Copy of input DataFrame.
    """
    return dataframe.copy()


@log_step
def select_species(structures, species):
    """
    Filter structures based on selected species.

    Parameters
    ----------
    structures : pandas.DataFrame
        Structures DataFrame from opencadd.databases.klifs module.
    species : str or list of str
        Species.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame.
    """
    if not isinstance(species, list):
        species = [species]
    return structures[structures["species.klifs"].isin(species)]


@log_step
def select_dfg(structures, dfg_conformation):
    """
    Filter structures based on selected DFG conformation(s).

    Parameters
    ----------
    structures : pandas.DataFrame
        Structures DataFrame from opencadd.databases.klifs module.
    dfg_conformation : str of list of str
        DFG conformation(s).

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame.
    """
    if not isinstance(dfg_conformation, list):
        dfg_conformation = [dfg_conformation]
    return structures[structures["structure.dfg"].isin(dfg_conformation)]


@log_step
def select_resolution(structures, resolution_max):
    """
    Filter structures for structure with a resolution equal or lower than a given value.

    Parameters
    ----------
    structures : pandas.DataFrame
        Structures DataFrame from opencadd.databases.klifs module.
    resolution_max : int or float
        Maximum resolution value.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame.
    """
    return structures[structures["structure.resolution"] <= resolution_max]


@log_step
def select_qualityscore(structures, qualityscore_min):
    """
    Filter structures for structures with a quality score equal or greater than a given value.

    Parameters
    ----------
    structures : pandas.DataFrame
        Structures DataFrame from opencadd.databases.klifs module.
    qualityscore_min : int or float
        Minimum KLIFS quality score value.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame.
    """
    return structures[structures["structure.qualityscore"] >= qualityscore_min]


@log_step
def select_maximum_n_mutations(structures, n_mutations):
    """
    Filter structures for structures with a maximum of N mutations in the KLIFS pocket.

    Parameters
    ----------
    structures : pandas.DataFrame
        Structures DataFrame from opencadd.databases.klifs module; must include "structure.pocket"
        and "kinase.pocket" columns.
    n_mutations : int
        Number of mutations allowed.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame.
    """

    def has_more_than_n_mutations(structure_seq, kinase_seq, n_mutations):
        """
        Check if input KLIFS structures has a mutation by comparing the KLIFS structure pocket
        sequence to the KLIFS kinase pocket sequence. "_" and "-" residues are omitted, any other
        positional mismatches are reported as mutation.

        Parameters
        ----------
        structure_seq : str
            KLIFS structure pocket sequence. Same length as `kinase_seq`.
        kinase_seq : str
            KLIFS kinase pocket sequence. Same length as `structure_seq`.
        n_mutations : int
            Number of mutations allowed.

        Returns
        -------
        bool
            Structure has a mutation (True) or not (False).
        """

        sequences = pd.DataFrame(
            [list(structure_seq), list(kinase_seq)], index=["structure", "kinase"]
        ).transpose()
        sequences.index = sequences.index + 1
        # Remove gaps in KLIFS structure, which are denoted with "_"
        sequences = sequences[sequences.apply(lambda x: x["structure"] != "_", axis=1)]
        # Remove gaps in KLIFS kinase, which are denoted with "-"
        sequences = sequences[sequences.apply(lambda x: x["kinase"] != "-", axis=1)]

        # Get mutations by detecting positional mismatches
        mutations = sequences[sequences.apply(lambda x: x["structure"] != x["kinase"], axis=1)]

        if mutations.shape[0] > n_mutations:
            return True
        else:
            return False

    # Keep only structures without any mutations
    structures = structures[
        structures.apply(
            lambda x: not has_more_than_n_mutations(
                x["structure.pocket"], x["kinase.pocket"], n_mutations
            ),
            axis=1,
        )
    ]
    return structures


@log_step
def select_maximum_n_missing_residues(structures, n_missing_residues):
    """
    Filter structures for structures with a maximum of N missing residues in the KLIFS pocket.

    Parameters
    ----------
    structures : pandas.DataFrame
        Structures DataFrame from opencadd.databases.klifs module; must include "structure.pocket".
    n_missing_residues : int
        Number of missing residues allowed.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame.
    """
    return structures[structures["structure.pocket"].str.count("_") <= n_missing_residues]


@log_step
def select_best_pdb_kinase_pairs(structures):
    """
    Pick only the best structure among all structures per kinase-PDB pair.
    The best structures per kinase-PDB pair is defined as having the least missing residues,
    the least missing atoms, and the lowest alternate model identifier (in that order).

    Parameters
    ----------
    structures : pandas.DataFrame
        Structures DataFrame from opencadd.databases.klifs module.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame.

    Notes
    -----

    Example A

    | # missing residues | # missing atoms | alternate model | chain | picked |
    ---------------------------------------------------------------------------
    | 0                  | 0               | A               | A     | x      |
    | 1                  | 0               | A               | A     |        |

    Example B

    | # missing residues | # missing atoms | alternate model | chain | picked |
    ---------------------------------------------------------------------------
    | 1                  | 0               | A               | A     | x      |
    | 1                  | 9               | A               | A     |        |

    Example C

    | # missing residues | # missing atoms | alternate model | chain | picked |
    ---------------------------------------------------------------------------
    | 1                  | 0               | B               | A     |        |
    | 1                  | 0               | A               | A     | x      |

    Example D

    | # missing residues | # missing atoms | alternate model | chain | picked |
    ---------------------------------------------------------------------------
    | 1                  | 0               | A               | B     |        |
    | 1                  | 0               | A               | A     | x      |

    """
    # Sort structures by kinase, PDB and descending qualityscore
    structures.sort_values(
        by=[
            "kinase.klifs_name",
            "structure.pdb_id",
            "structure.missing_residues",  # Least missing residues
            "structure.missing_atoms",  # Least missing atoms
            "structure.alternate_model",  # Prioritize model with lowest ID
            "structure.chain",  # Prioritize chain with lowest ID
        ],
        ascending=[True, True, True, True, True, True],
        inplace=True,
    )
    # Drop duplicate kinase-PDB pairs, keep only the first entry (sorting done before!)
    structures.drop_duplicates(
        subset=["kinase.klifs_name", "structure.pdb_id"], keep="first", inplace=True
    )
    return structures


@log_step
def select_unflagged_structures_only(structures):
    """
    Remove structures that are flagged in KLIFS.

    Parameters
    ----------
    structures : pandas.DataFrame
        Structures DataFrame from opencadd.databases.klifs module.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame.
    """
    # TODO: This bit will be part of opencadd at some point
    from bravado.client import SwaggerClient

    KLIFS_API_DEFINITIONS = "https://klifs.net/swagger_v2/swagger.json"
    KLIFS_CLIENT = SwaggerClient.from_url(
        KLIFS_API_DEFINITIONS, config={"validate_responses": False}
    )
    structures_list = (
        KLIFS_CLIENT.Structures.get_structure_list(
            structure_ID=structures["structure.klifs_id"].to_list()
        )
        .response()
        .result
    )

    flagged_structure_klifs_ids = []
    for structure in structures_list:
        if structure.curation_flag:
            flagged_structure_klifs_ids.append(structure.structure_ID)

    # Remove flagged structures from kissim dataset
    structures = structures[~structures["structure.klifs_id"].isin(flagged_structure_klifs_ids)]

    return structures
