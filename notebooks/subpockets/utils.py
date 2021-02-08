import pandas as pd
from IPython.display import display, Markdown
from opencadd.structure.pocket import PocketKlifs

def random_pockets(structures, n_structures, seed, anchor_residues, subpocket_names, subpocket_colors, klifs_session):
    
    random_structures = structures.sample(n=n_structures, random_state=seed)
    subpockets = {
        "anchor_residue.klifs_ids": anchor_residues,
        "subpocket.name": subpocket_names,
        "subpocket.color": subpocket_colors
    }
    display(Markdown(pd.DataFrame(
        {"name": subpocket_names, "anchors": anchor_residues, "color": subpocket_colors}
    ).to_markdown()))
    pockets = []
    for structure_klifs_id in random_structures["structure.klifs_id"]:
        print(f"Structure KLIFS ID: {structure_klifs_id}")
        pocket = PocketKlifs.from_structure_klifs_id(structure_klifs_id, subpockets, klifs_session=klifs_session)
        pockets.append(pocket)
        
    return pockets