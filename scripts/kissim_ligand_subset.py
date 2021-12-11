"""
Generate KiSSim data for 
"""

from pathlib import Path
from kissim.api import subset, compare

from src.data.interacting_residues import residues_interacting_with_ligand
from src.paths import PATH_RESULTS

PATH_RESULTS_DFG_IN = PATH_RESULTS / "dfg_in"

def main(ligand_expo_id, path_fp_in=PATH_RESULTS_DFG_IN / "fingerprints_normalized.json"):
    """
    Generate KiSSim fingerprint distances for a subset version of the fingerprint that 
    is based only on residues that show interactions with co-crystallized structures
    (use KLIFS IFPS for this).

    Parameters
    ----------
    ligand_expo_id : str
        Ligand expo ID.
    path_fp_in : pathlib.Path
        Path to full-length fingerprint JSON file to be used for subsetting.
    """

    # Get interacting residues for query ligand
    print("Get interacting residues...")
    interacting_residues = residues_interacting_with_ligand(ligand_expo_id)

    # Create new output folder for subset results
    path_out = Path(f"{path_fp_in.parent}_{ligand_expo_id}")
    print(path_out)
    path_out.mkdir(parents=True, exist_ok=True)

    # Subset fingerprints
    print("Subset fingerprints...")
    fingerprint_generator = subset(
        fingerprints_path = path_fp_in,
        klifs_pocket_residue_subset_type=ligand_expo_id,
        fingerprints_subset_path = path_out / "fingerprints_normalized.json",
        klifs_pocket_residue_subset={ligand_expo_id: interacting_residues}
    )
    
    print("All-against-all comparison...")
    compare(
        fingerprint_generator=fingerprint_generator,
        output_path=path_out,
        feature_weights=None,
        n_cores=7
    )

if __name__ == "__main__":
    main("IRE")
    main("STI")
    main("DB8")
    main("B96")