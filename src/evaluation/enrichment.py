"""
Calculate enrichment values. TODO Add clear definitions!
"""


def enrichment_plot_data(ranks, ligand_kinase_method, kinase_kinase_method):
    """
    Calcuate y values for x values ranging from 0 to 100 (step size 1) for enrichment plot.

    Parameters
    ----------
    ranks : pandas.DataFrame
        Must use `src.evaluation.kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data`. See this
        return value description in this function's docstring.
    ligand_kinase_method : str
        Name for ligand profiling method to be used as identifier in `ranks`.
    kinase_kinase_method : str
        Name for kinase distances method to be used as identifier in `ranks`.

    Returns
    -------
    list of tuple
        List of x/y values (y values for x values ranging from 0 to 100 (step size 1)).

    Notes
    -----
    N   : Number of kinases in totoal
    N_s : Number of kinases in top x% of ranked kinases
    n   : Number of active kinases in total
    n_s : Number of active kinases in top x% of ranked kinases

    For the enrichment plot, the x and y values are calculated as follows:
    x = N_s / N
    y = n_s / n
    """
    enrichment_data = [
        enrichment_top_x(ranks, ligand_kinase_method, kinase_kinase_method, i)
        for i in range(0, 101, 1)
    ]
    return enrichment_data


def enrichment_top_x(ranks, ligand_kinase_method, kinase_kinase_method, top_x):
    """
    Calculate the enrichment in the top x% (`top_x`) of ranked kinases.

    Parameters
    ----------
    ranks : pandas.DataFrame
        Must use `src.evaluation.kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data`. See this
        return value description in this function's docstring.
    ligand_kinase_method : str
        Name for ligand profiling method to be used as identifier in `ranks`.
    kinase_kinase_method : str
        Name for kinase distances method to be used as identifier in `ranks`.
    top_x : float
        The top x% of ranked kinases.

    Returns
    -------
    ratio_ranked_data : float
        Percentage of ranked data in `top_x` (x value in enrichment plot).
    ratio_active_kinases_identified : float
        Percentage of active kinases in `top_x` (y value in enrichment plot).

    Notes
    -----
    See notes in `enrichment_plot_data`.
    """

    # Get number of kinases in top x% and in total
    kinases_total = ranks
    n_kinases_total = kinases_total.shape[0]
    n_kinases_top_x = int(n_kinases_total * top_x / 100.0)
    kinases_top_x = kinases_total.head(n_kinases_top_x)

    # Get number of active kinases in top x% and in total
    n_active_kinases_total = kinases_total[f"{ligand_kinase_method}.active"].sum()
    n_active_kinases_top_x = kinases_top_x[f"{ligand_kinase_method}.active"].sum()

    # Calculate important ratios
    ratio_ranked_data = n_kinases_top_x / n_kinases_total * 100
    ratio_active_kinases_identified = n_active_kinases_top_x / n_active_kinases_total * 100

    return ratio_ranked_data, ratio_active_kinases_identified


def enrichment_optimal(ranks, ligand_kinase_method):
    """
    Calculate the optimal enrichment, i.e. the ratio of ranked kinases, in which optimally all
    active kinases have been found.

    Parameters
    ----------
    ranks : pandas.DataFrame
        Must use `src.evaluation.kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data`. See this
        return value description in this function's docstring.
    ligand_kinase_method : str
        Name for ligand profiling method to be used as identifier in `ranks`.

    Returns
    -------
    float
        Percentage of ranked kinases that will optimally contain _all_ active kinases.

    Notes
    -----
    N   : Number of kinases in totoal
    N_s : Number of kinases in top x% of ranked kinases
    n   : Number of active kinases in total
    n_s : Number of active kinases in top x% of ranked kinases

    For the enrichment plot, the x values are calculated as follows:
    x = N_s / N
    In the optimal case, N_s = n, hence:
    x_optimal = n / N
    """

    n_kinases = ranks.shape[0]
    n_active_kinases = ranks[f"{ligand_kinase_method}.active"].sum()
    ratio_active_kinases_identified_optimal = n_active_kinases / n_kinases * 100

    return ratio_active_kinases_identified_optimal


def enrichment_factor_top_x(ranks, ligand_kinase_method, kinase_kinase_method, top_x):
    """
    Calculate the enrichment factor for the top x% (`top_x`) of ranked kinases.

    Parameters
    ----------
    ranks : pandas.DataFrame
        Must use `src.evaluation.kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data`. See this
        return value description in this function's docstring.
    ligand_kinase_method : str
        Name for ligand profiling method to be used as identifier in `ranks`.
    kinase_kinase_method : str
        Name for kinase distances method to be used as identifier in `ranks`.
    top_x : float
        The top x% of ranked kinases.

    Returns
    -------
    float
        Enrichment factor.

    Notes
    -----
    N   : Number of kinases in totoal
    N_s : Number of kinases in top x% of ranked kinases
    n   : Number of active kinases in total
    n_s : Number of active kinases in top x% of ranked kinases

    The enrichment factor is defined as:
    EFx% = (n_s / n) / (N_s / N)
    """

    ratio_active_kinases_identified, ratio_ranked_data = enrichment_top_x(
        ranks, ligand_kinase_method, kinase_kinase_method, top_x
    )
    if ratio_ranked_data > 0:
        ef = ratio_active_kinases_identified / ratio_ranked_data
    else:
        ef = 0

    return ef