"""
Calculate enrichment values. TODO Add clear definitions!
"""


def enrichment_factor(ranks, ligand_kinase_method, kinase_kinase_method, cutoff_percentage=10):

    ratio_active_kinases_identified, ratio_ranked_data = enrichment(
        ranks, ligand_kinase_method, kinase_kinase_method, cutoff_percentage
    )
    ef = ratio_active_kinases_identified * ratio_ranked_data

    return ef


def enrichment(ranks, ligand_kinase_method, kinase_kinase_method, cutoff_percentage=10):

    kinases_total = ranks.dropna(subset=[f"{kinase_kinase_method}.rank2"]).sort_values(
        f"{kinase_kinase_method}.measure"
    )[1:]
    n_kinases_total = kinases_total.shape[0]

    n_kinases_top_x = int(n_kinases_total * cutoff_percentage / 100.0)
    kinases_top_x = kinases_total.head(n_kinases_top_x)

    n_active_kinases_total = kinases_total[f"{ligand_kinase_method}.active"].sum()
    n_active_kinases_top_x = kinases_top_x[f"{ligand_kinase_method}.active"].sum()

    ratio_active_kinases_identified = n_active_kinases_top_x / n_active_kinases_total
    ratio_ranked_data = n_kinases_top_x / n_kinases_total

    return ratio_active_kinases_identified, ratio_ranked_data


def enrichment_optimal(ranks, ligand_kinase_method, kinase_kinase_method):

    n_kinases = ranks.dropna(subset=[f"{kinase_kinase_method}.rank2"]).shape[0]
    n_active_kinases = ranks.dropna(subset=[f"{kinase_kinase_method}.rank2"])[
        f"{ligand_kinase_method}.active"
    ].sum()

    return n_active_kinases / n_kinases
