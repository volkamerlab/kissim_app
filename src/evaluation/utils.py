"""
Calculate enrichment values.
"""

from sklearn import metrics


def roc_fpr_tpr_auc(ligand_vs_kinase_data):
    """
    Get the following ROC curve data for a ligand-kinase pair:
    FPR, TPR, AUC, number of shared kinases, number of shared active kinases.

    Parameters
    ----------
    Please check `src.evaluation.kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data` docstring.

    Returns
    -------
    list
        FPR, TPR, AUC, number of shared kinases, number of shared active kinases.Visualize ROC curves.

    References
    ----------
    - ROC AUC: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html#sklearn.metrics.roc_auc_score  # noqa: E501
    - ROC curve: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html#sklearn.metrics.roc_curve)  # noqa: E501
    """

    data = ligand_vs_kinase_data.data
    # data[f"{ligand_vs_kinase_data.kinase_kinase_method}.measure"] = range(0, len(data))

    # Get labels
    y_true = data[f"{ligand_vs_kinase_data.ligand_kinase_method}.active"].to_list()
    # Get scores
    y_score = data[f"{ligand_vs_kinase_data.kinase_kinase_method}.measure"]
    # TPR and FPR values are calculated based on different threshold values that will
    # cast the `y_score` values to True or False, if `y_score` >= `threshold`
    # Our score describes distances; if we want our score to be True if >= `threshold`,
    # we will need to convert distances to similarities
    # In short: `y_score` needs descending values!
    y_score = (1 - y_score / y_score.max()).to_list()
    pos_label = True

    # `roc_curve` returns `(fpr, tpr, thresholds)`; number of thresholds and their values seem
    # to be set based on the input data
    fpr, tpr, _ = metrics.roc_curve(y_true, y_score, pos_label=pos_label)
    auc = metrics.roc_auc_score(y_true, y_score)
    n_kinases_shared = ligand_vs_kinase_data.n_kinases_shared
    n_active_kinases_shared = ligand_vs_kinase_data.n_active_kinases_shared

    return fpr, tpr, auc, n_kinases_shared, n_active_kinases_shared


def enrichment_plot_data(ligand_vs_kinase_data):
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

    enrichment_data = [enrichment_top_x(ligand_vs_kinase_data, i) for i in range(0, 101, 1)]
    return enrichment_data


def enrichment_top_x(ligand_vs_kinase_data, top_x):
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
    kinases_total = ligand_vs_kinase_data.data
    n_kinases_total = kinases_total.shape[0]
    n_kinases_top_x = int(n_kinases_total * top_x / 100.0)
    kinases_top_x = kinases_total.head(n_kinases_top_x)

    # Get number of active kinases in top x% and in total
    n_active_kinases_total = kinases_total[
        f"{ligand_vs_kinase_data.ligand_kinase_method}.active"
    ].sum()
    n_active_kinases_top_x = kinases_top_x[
        f"{ligand_vs_kinase_data.ligand_kinase_method}.active"
    ].sum()

    # Calculate important ratios
    ratio_ranked_data = n_kinases_top_x / n_kinases_total * 100
    ratio_active_kinases_identified = n_active_kinases_top_x / n_active_kinases_total * 100

    return ratio_ranked_data, ratio_active_kinases_identified


def enrichment_optimal(ligand_vs_kinase_data):
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

    ranks = ligand_vs_kinase_data.data
    n_kinases = ranks.shape[0]
    n_active_kinases = ranks[f"{ligand_vs_kinase_data.ligand_kinase_method}.active"].sum()
    ratio_active_kinases_identified_optimal = n_active_kinases / n_kinases * 100

    return ratio_active_kinases_identified_optimal


def enrichment_factor_top_x(ligand_vs_kinase_data, top_x):
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
        ligand_vs_kinase_data, top_x
    )
    if ratio_ranked_data > 0:
        ef = ratio_active_kinases_identified / ratio_ranked_data
    else:
        ef = 0

    return ef


def calculate_tanimoto(int_list1, int_list2):
    """
    Calculate Tanimoto coefficient for two binary integer lists with values [0, 1].
    If all integers in both lists are set to 0, return 0.

    Parameters
    ----------
    int_list1: list of int
        List of integers [0, 1]. Must have same length as int_list2.
    int_list2: list of int
        List of integers [0, 1]. Must have same length as int_list1.

    Returns
    -------
    float
        Tanimoto coefficient (similarity between input).

    Notes
    -----
    For binary values [0, 1], the Tanimoto coefficient is defined as follows:

    $$T_{c}(A,B) = \frac{c}{a+b-c}$$

    a: Number of features present (i.e. being 1) in A <br>
    b: Number of features present (i.e. being 1) in B <br>
    c: Number of features present in both A and B (i.e. both being 1)
    """

    # Input must have same length
    if len(int_list1) != len(int_list2):
        raise ValueError("Input is not of same length.")

    a = sum(int_list1)
    b = sum(int_list2)
    c = sum([1 for i, j in zip(int_list1, int_list2) if i + j == 2])

    # If all integers in both lists are set to 0, return 0
    if a + b == 0:
        return 0.0
    # Else calculate Tanimoto coefficient
    else:
        return round(float(c) / (a + b - c), 2)
