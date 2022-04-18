"""
Evaluate method performance based on ligand-kinase data.
"""

from collections import defaultdict
import logging
import math

import pandas as pd
import matplotlib.pyplot as plt

from src import data
from src.evaluation import utils
from src.evaluation.data.ligand_vs_kinase_data import LigandVsKinaseData

logger = logging.getLogger(__name__)
plt.style.use("seaborn")


class LigandVsKinaseEvaluator:
    """
    Evaluator for performance for profiling vs. kinase similarity datasets.

    Attributes
    ----------
    ligand_kinase_method : str
        Name for ligand profiling method to be used as identifier.
    kinase_kinase_method : str
        Name for kinase distances method to be used as identifier.
    ligand_kinase_pairs : list of list of str
        List of ligand-kinase pairs (input).
    ligand_kinase_pairs_curated : list of list of str
        List of ligand-kinase pairs (curated); potentially less than input because some pairs do
        not have enough coverage (see class arguments e.g. `min_n_shared_kinases` and
        `min_n_shared_active_kinases`).
    data_dict : dict of dict of LigandVsKinaseData
        For each ligand (key 1) and each kinase (key 2) store respective dataset.
    """

    def __init__(
        self,
        ligand_kinase_pairs,
        ligand_kinase_method,
        kinase_kinase_method,
        kinase_activity_cutoff,
        kinase_activity_max,
        min_n_shared_kinases=10,
        min_n_shared_active_kinases=3,
        pkidb_ligands=True,
        fda_approved=False,
        kinmap_kinases=True,
        kinase_kinase_path=None,
    ):
        """
        Initialize LigandVsKinaseEvaluator.

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
        kinase_activity_cutoff : float
            Cutoff value to be used to determine activity. By default this cutoff is the maximum
            value. Set `kinase_activity_max=False` if cutoff is the minimum value.
        kinase_activity_max : bool
            If `True` (default), the `kinase_activity_cutoff` is used as the maximum cutoff, else
            as the minimum cutoff.
        pkidb_ligands : bool
            Keep only PKIDB ligands (will rename ligands to their names in PKIDB). Default is True.
        fda_approved : bool
            Has only effect if `pkidb_ligands` is True. Keep only FDA-approved PKIDB ligands.
            Default is False.
        kinmap_kinases : bool
            Map kinase names to KinMap kinase names. Default is False.
        kinase_kinase_path : str or pathlib.Path or None
            Set path to user-defined dataset file. If None, use default path for respective
            dataset.
        """

        self.ligand_kinase_method = ligand_kinase_method
        self.kinase_kinase_method = kinase_kinase_method
        self.ligand_kinase_pairs = ligand_kinase_pairs
        self.ligand_kinase_pairs_curated = None
        self.data_dict = None

        # Get ligand-kinase and kinase-kinase matrices
        ligand_kinase_matrix, kinase_kinase_matrix = self._load_datasets(
            ligand_kinase_method,
            kinase_kinase_method,
            pkidb_ligands,
            fda_approved,
            kinmap_kinases,
            kinase_kinase_path,
        )

        # Get merged dataset for each ligand-kinase pair
        data_dict = defaultdict(dict)
        for ligand_name, kinase_name in self.ligand_kinase_pairs:
            try:
                data = LigandVsKinaseData(
                    ligand_name,
                    kinase_name,
                    self.ligand_kinase_method,
                    self.kinase_kinase_method,
                    ligand_kinase_matrix,
                    kinase_kinase_matrix,
                    kinase_activity_cutoff,
                    kinase_activity_max,
                )
                data_dict[ligand_name][kinase_name] = data
            except KeyError as e:
                logging.error(e)
        self.data_dict = data_dict

        # Curate input ligand kinase pairs
        self.ligand_kinase_pairs_curated = self._curate_ligand_kinase_pairs(
            min_n_shared_kinases, min_n_shared_active_kinases
        )

    def _load_datasets(
        self,
        ligand_kinase_method,
        kinase_kinase_method,
        pkidb_ligands,
        fda_approved,
        kinmap_kinases,
        kinase_kinase_path,
    ):
        """
        Load ligand-kinase and kinase-kinase dataset.

        Parameters
        ----------
        Check `__init__` docstring.

        Returns
        -------
        ligand_kinase_matrix : pd.DataFrame
            Ligand-kinase data.
        kinase_kinase_matrix : pd.DataFrame
            Kinase-kinase data.
        """

        ligand_kinase_matrix = data.profiling.load(
            ligand_kinase_method,
            pkidb_ligands=pkidb_ligands,
            fda_approved=fda_approved,
            kinmap_kinases=kinmap_kinases,
        )

        kinase_kinase_matrix = data.distances.load(
            kinase_kinase_method,
            kinmap_kinases=kinmap_kinases,
            distances_path=kinase_kinase_path,
        )

        return ligand_kinase_matrix, kinase_kinase_matrix

    def _curate_ligand_kinase_pairs(self, min_n_shared_kinases, min_n_shared_active_kinases):
        """
        Curate input ligand-kinase pairs. Keep only pair that
        - have a minimum of `min_n_shared_kinases` shared kinases
        - have a minimum of `min_n_shared_active_kinases` shared active kinases, while activity is
        defined as <=/=> `min_n_shared_kinases` with `kinase_activity_max=True/False`, respectively

        Parameters
        ----------
        min_n_shared_kinases : int
            Datasets must share at least `min_n_shared_kinases` kinases.
        min_n_shared_active_kinases : int
            Datasets must share at least `min_n_shared_active_kinases` active kinases.

        Returns
        -------
        list of tuple
            Curate list of ligand and kinase name pairs.
        """

        logging.info(
            f"Number of ligand-kinase pairs (full dataset): {len(self.ligand_kinase_pairs)}"
        )

        ligand_kinase_pairs_curated = []
        for ligand_name, ligand_dict in self.data_dict.items():
            for kinase_name, ligand_kinase_data in ligand_dict.items():
                # Conditions
                n_kinases_shared = ligand_kinase_data.n_kinases_shared
                n_active_kinases_shared = ligand_kinase_data.n_active_kinases_shared
                cond1 = n_kinases_shared >= min_n_shared_kinases
                cond2 = n_active_kinases_shared > min_n_shared_active_kinases
                cond3 = n_kinases_shared > n_active_kinases_shared
                if cond1 & cond2 & cond3:
                    ligand_kinase_pairs_curated.append([ligand_name, kinase_name])

        logging.info(
            f"Number of ligand-kinase pairs (filtered dataset): {len(ligand_kinase_pairs_curated)}"
        )

        return ligand_kinase_pairs_curated

    def plot_enrichment(self):
        """
        Create enrichment plots per ligand for different ligand targets (multiplot).
        """

        enrichment_plots_data_dict = self._enrichment_plots_data()

        n_cols = 4
        n_rows = math.ceil(len(enrichment_plots_data_dict) / n_cols)
        n_rows = max(n_rows, 1)
        _, axes = plt.subplots(figsize=(n_cols * 5, n_rows * 5), nrows=n_rows, ncols=n_cols)
        axes = axes.reshape(-1)

        for i, (ligand_name, (experiment_df, optimum, n_kinases, n_active_kinases)) in enumerate(
            enrichment_plots_data_dict.items()
        ):
            # Experimental curves
            experiment_df.plot(
                title=(
                    f"{ligand_name.upper()} (in total {n_kinases} kinases, "
                    f"{n_active_kinases} active kinases)"
                ),
                ylim=(0, 101),
                xlim=(-1, 100),
                ax=axes[i],
            )
            # Optimal curve
            axes[i].plot(
                [0, optimum, 100], [0, 100, 100], label="Optimum", linestyle="--", color="k"
            )
            # Random curve
            axes[i].plot([0, 100], [0, 100], label="Random", linestyle="--", color="grey")
            axes[i].legend()
            # Cosmetics
            axes[i].set_aspect(1.0 / axes[i].get_data_ratio(), adjustable="box")
            axes[i].set_xlabel("% ranked kissim dataset")
            axes[i].set_ylabel("% true active kinases identified")

        # Make empty plots blank
        n_plots = len(enrichment_plots_data_dict)
        n_axes = len(axes)
        for i in range(n_plots, n_axes):
            axes[i].axis("off")

    def _enrichment_plots_data(self):
        """
        Get data for EF plots per ligand for different ligand targets (multiplot).

        Returns
        -------
        dict of pd.DataFrame
            Per ligand (key) get corresponding data needed for enrichment plot.
        """

        experiment_dict = defaultdict(list)
        optimum_dict = {}
        n_kinases = {}
        n_active_kinases = {}

        for ligand_name, kinase_name in self.ligand_kinase_pairs_curated:

            # Get data for current ligand-kinase pair
            ligand_vs_kinase_data = self.data_dict[ligand_name][kinase_name]
            # Experimental enrichment (`experiment` : DataFrame)
            experiment = [
                utils.enrichment_top_x(
                    ligand_vs_kinase_data,
                    i,
                )
                for i in range(0, 101, 1)
            ]
            experiment = pd.DataFrame(experiment, columns=["x", kinase_name]).set_index("x")

            # Optimal enrichment (`optimum` : float)
            # Technically needs only to be calculated
            # Loop structure will calculate this mutiple times
            optimum = utils.enrichment_optimal(ligand_vs_kinase_data)

            experiment_dict[ligand_name].append(experiment)
            optimum_dict[ligand_name] = optimum
            n_kinases[ligand_name] = ligand_vs_kinase_data.data.shape[0]
            n_active_kinases[ligand_name] = ligand_vs_kinase_data.data[
                f"{self.ligand_kinase_method}.active"
            ].sum()

        data_dict = {
            ligand_name: (
                pd.concat(experiment, axis=1).reset_index(drop=True),
                optimum,
                n_kinases,
                n_active_kinases,
            )
            for (ligand_name, experiment), (_, optimum), (_, n_kinases), (
                _,
                n_active_kinases,
            ) in zip(
                experiment_dict.items(),
                optimum_dict.items(),
                n_kinases.items(),
                n_active_kinases.items(),
            )
        }

        return data_dict

    def plot_enrichment_factors(self):
        """
        Create enrichment factor plots per ligand for different ligand targets (multiplot).
        """

        data_dict = self._enrichment_factor_plots_data()

        n_cols = 4
        n_rows = math.ceil(len(data_dict) / n_cols)
        n_rows = max(n_rows, 1)
        _, axes = plt.subplots(figsize=(n_cols * 5, n_rows * 5), nrows=n_rows, ncols=n_cols)
        axes = axes.reshape(-1)

        for i, (ligand_name, ef_df) in enumerate(data_dict.items()):
            # Experimental curves
            ef_df.plot(
                title=ligand_name.upper(),
                ax=axes[i],
            )
            # Cosmetics
            axes[i].set_xlabel("${x\%}$")  # noqa: W605
            axes[i].set_ylabel("$EF_{x\%}$")  # noqa: W605

        # Make empty plots blank
        n_plots = len(data_dict)
        n_axes = len(axes)
        for i in range(n_plots, n_axes):
            axes[i].axis("off")

    def _enrichment_factor_plots_data(self):
        """
        Prepares data in `plot_enrichment_factors` function.

        Returns
        -------
        dict
            Enrichment plot data for ligands (keys): EF_x% values.
        """

        data_dict = defaultdict(list)
        for ligand_name, kinase_name in self.ligand_kinase_pairs_curated:

            # Get data for current ligand-kinase pair
            ligand_vs_kinase_data = self.data_dict[ligand_name][kinase_name]
            top_x_list = [1, 5, 10, 20, 25, 50]
            data = [
                utils.enrichment_factor_top_x(ligand_vs_kinase_data, top_x) for top_x in top_x_list
            ]
            data = pd.Series(data, index=top_x_list)
            data.name = kinase_name
            data_dict[ligand_name].append(data)
        data_dict = {
            ligand_name: pd.concat(data, axis=1) for ligand_name, data in data_dict.items()
        }

        return data_dict

    def plot_roc_curves(self, output_file=None):
        """
        Create ROC curve plots per ligand for different ligand targets (multiplot).

        Parameters
        ----------
        output_file : str
            Path to output figure PNG file.

        Returns
        -------
        dict
            AUCs for all ligand-kinase pairs. Example:
            {"ligand_name-kinase_name": 1.0, "ligand_name-kinase_name": 0.8}
        """

        data_dict = self._roc_curves_data()

        n_cols = 4
        n_rows = math.ceil(len(data_dict) / n_cols)
        n_rows = max(n_rows, 1)
        _, axes = plt.subplots(figsize=(n_cols * 5, n_rows * 5), nrows=n_rows, ncols=n_cols)
        axes = axes.reshape(-1)

        auc_dict = {}

        for i, (ligand_name, kinases_data) in enumerate(data_dict.items()):
            for kinase_data in kinases_data:
                kinase_name, fpr, tpr, auc, n_kinases, n_active_kinases = kinase_data
                # Experimental curves
                axes[i].plot(fpr, tpr, label=f"{kinase_name} (AUC={round(auc, 3)})")
                auc_dict[f"{ligand_name}-{kinase_name}"] = auc
            # Random curve
            axes[i].plot([0, 1], [0, 1], label="Random", linestyle="--", color="grey")
            axes[i].legend(title="On-targets")
            # Cosmetics
            axes[i].set_aspect(1.0 / axes[i].get_data_ratio(), adjustable="box")
            axes[i].set_xlabel("FPR")
            axes[i].set_ylabel("TPR")
            axes[i].set_title(
                f"{ligand_name.upper()} (in total {n_kinases} kinases, "
                f"{n_active_kinases} active kinases)",
            )

        # Make empty plots blank
        n_plots = len(data_dict)
        n_axes = len(axes)
        for i in range(n_plots, n_axes):
            axes[i].axis("off")

        if output_file:
            if output_file.suffix == ".png":
                plt.savefig(output_file, bbox_inches="tight", dpi=300)
            else:
                plt.savefig(output_file, bbox_inches="tight")

        return auc_dict

    def _roc_curves_data(self):
        """
        Get data for ROC curve plots per ligand for different ligand targets (multiplot).


        Returns
        -------
        dict of pd.DataFrame
            Per ligand (key) get corresponding data needed for ROC plot.
        """

        data_dict = defaultdict(list)

        for ligand_name, kinase_name in self.ligand_kinase_pairs_curated:

            # Get data for current ligand-kinase pair
            ligand_vs_kinase_data = self.data_dict[ligand_name][kinase_name]

            fpr, tpr, auc, n_kinases, n_active_kinases = utils.roc_fpr_tpr_auc(
                ligand_vs_kinase_data
            )

            data_dict[ligand_name].append(
                [kinase_name, fpr, tpr, auc, n_kinases, n_active_kinases]
            )

        return data_dict
