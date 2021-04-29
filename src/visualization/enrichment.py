"""
Visualize enrichment.
"""

from collections import defaultdict
import math

import pandas as pd
import matplotlib.pyplot as plt

from ..evaluation import kinase_ranks, enrichment


def enrichment_plots(
    ligand_kinase_pairs,
    ligand_kinase_matrix,
    kinase_kinase_matrix,
    ligand_kinase_method,
    kinase_kinase_method,
    kinase_activity_cutoff,
    kinase_activity_max=True,
):
    """
    Create enrichment plots per ligand for different ligand targets (multiplot).

    Parameters
    ----------
    Please check `src.evaluation.kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data` docstring.
    """

    data_dict = _enrichment_plots_data(
        ligand_kinase_pairs,
        ligand_kinase_matrix,
        kinase_kinase_matrix,
        ligand_kinase_method,
        kinase_kinase_method,
        kinase_activity_cutoff,
        kinase_activity_max,
    )

    n_cols = 4
    n_rows = math.ceil(len(data_dict) / n_cols)
    fig, axes = plt.subplots(figsize=(n_cols * 5, n_rows * 5), nrows=n_rows, ncols=n_cols)
    axes = axes.reshape(-1)

    for i, (ligand_name, (experiment_df, optimum, n_kinases, n_active_kinases)) in enumerate(
        data_dict.items()
    ):
        # Experimental curves
        experiment_df.plot(
            title=f"{ligand_name.upper()} (in total {n_kinases} kinases, {n_active_kinases} active kinases)",
            ylim=(0, 101),
            xlim=(-1, 100),
            ax=axes[i],
        )
        # Optimal curve for ligand
        axes[i].plot([0, optimum, 100], [0, 100, 100], "--", color="k")
        # Cosmetics
        axes[i].set_aspect(1.0 / axes[i].get_data_ratio(), adjustable="box")
        axes[i].set_xlabel("% ranked kissim dataset")
        axes[i].set_ylabel("% true active kinases identified")

    # Make empty plots blank
    n_plots = len(data_dict)
    n_axes = len(axes)
    for i in range(n_plots, n_axes):
        axes[i].axis("off")


def _enrichment_plots_data(
    ligand_kinase_pairs,
    ligand_kinase_matrix,
    kinase_kinase_matrix,
    ligand_kinase_method,
    kinase_kinase_method,
    kinase_activity_cutoff,
    kinase_activity_max=True,
):
    """
    Create EF plots per ligand for different ligand targets (multiplot).

    Parameters
    ----------
    Please check `src.evaluation.kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data` docstring.
    """

    experiment_dict = defaultdict(list)
    optimum_dict = {}
    n_kinases = {}
    n_active_kinases = {}

    for ligand_name, kinase_name in ligand_kinase_pairs:
        ranks, _ = kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data(
            ligand_name,
            kinase_name,
            ligand_kinase_matrix,
            kinase_kinase_matrix,
            ligand_kinase_method,
            kinase_kinase_method,
            kinase_activity_cutoff,
            kinase_activity_max,
        )
        # Experimental enrichment (`experiment` : DataFrame)
        experiment = [
            enrichment.enrichment_top_x(ranks, ligand_kinase_method, kinase_kinase_method, i)
            for i in range(0, 101, 1)
        ]
        experiment = pd.DataFrame(experiment, columns=["x", kinase_name]).set_index("x")

        # Optimal enrichment (`optimum` : float)
        # Technically needs only to be calculated; loop structure will calculate this mutiple times
        optimum = enrichment.enrichment_optimal(ranks, ligand_kinase_method)

        experiment_dict[ligand_name].append(experiment)
        optimum_dict[ligand_name] = optimum
        n_kinases[ligand_name] = ranks.shape[0]
        n_active_kinases[ligand_name] = ranks[f"{ligand_kinase_method}.active"].sum()

    data_dict = {
        ligand_name: (
            pd.concat(experiment, axis=1).reset_index(drop=True),
            optimum,
            n_kinases,
            n_active_kinases,
        )
        for (ligand_name, experiment), (_, optimum), (_, n_kinases), (_, n_active_kinases) in zip(
            experiment_dict.items(),
            optimum_dict.items(),
            n_kinases.items(),
            n_active_kinases.items(),
        )
    }

    return data_dict


def enrichment_factor_plots(
    ligand_kinase_pairs,
    ligand_kinase_matrix,
    kinase_kinase_matrix,
    ligand_kinase_method,
    kinase_kinase_method,
    kinase_activity_cutoff,
    kinase_activity_max=True,
):
    """
    Prepares data in `enrichment_plots` function.

    Parameters
    ----------
    Please check `src.evaluation.kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data` docstring.

    Returns
    -------
    dict
        Enrichment plot data for ligands (keys): Experimental enrichment plot x/y values, optimal
        x value, number of kinases, and number of active kinases.
    """

    data_dict = _enrichment_factor_plots_data(
        ligand_kinase_pairs,
        ligand_kinase_matrix,
        kinase_kinase_matrix,
        ligand_kinase_method,
        kinase_kinase_method,
        kinase_activity_cutoff,
        kinase_activity_max,
    )

    n_cols = 4
    n_rows = math.ceil(len(data_dict) / n_cols)
    fig, axes = plt.subplots(figsize=(n_cols * 5, n_rows * 5), nrows=n_rows, ncols=n_cols)
    axes = axes.reshape(-1)

    for i, (ligand_name, ef_df) in enumerate(data_dict.items()):
        # Experimental curves
        ef_df.plot(
            title=ligand_name.upper(),
            ax=axes[i],
        )
        # Cosmetics
        axes[i].set_xlabel("${x\%}$")
        axes[i].set_ylabel("$EF_{x\%}$")

    # Make empty plots blank
    n_plots = len(data_dict)
    n_axes = len(axes)
    for i in range(n_plots, n_axes):
        axes[i].axis("off")


def _enrichment_factor_plots_data(
    ligand_kinase_pairs,
    ligand_kinase_matrix,
    kinase_kinase_matrix,
    ligand_kinase_method,
    kinase_kinase_method,
    kinase_activity_cutoff,
    kinase_activity_max=True,
):
    """
    Prepares data in `enrichment_factor_plots` function.

    Parameters
    ----------
    Please check `src.evaluation.kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data` docstring.

    Returns
    -------
    dict
        Enrichment plot data for ligands (keys): EF_x% values.
    """

    data_dict = defaultdict(list)
    for ligand_name, kinase_name in ligand_kinase_pairs:
        ranks, _ = kinase_ranks.kinase_ranks_by_ligand_vs_kinase_data(
            ligand_name,
            kinase_name,
            ligand_kinase_matrix,
            kinase_kinase_matrix,
            ligand_kinase_method,
            kinase_kinase_method,
            kinase_activity_cutoff,
            kinase_activity_max,
        )
        top_x_list = [1, 5, 10, 20, 25, 50]
        data = [
            enrichment.enrichment_factor_top_x(
                ranks, ligand_kinase_method, kinase_kinase_method, top_x
            )
            for top_x in top_x_list
        ]
        data = pd.Series(data, index=top_x_list)
        data.name = kinase_name
        data_dict[ligand_name].append(data)
    data_dict = {ligand_name: pd.concat(data, axis=1) for ligand_name, data in data_dict.items()}

    return data_dict