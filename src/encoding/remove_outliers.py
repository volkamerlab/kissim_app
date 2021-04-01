"""
Removes outlier fingerprints (if distances are too large).

Run python script:
python remove_outliers.py
"""

from pathlib import Path
from kissim.encoding import FingerprintGenerator

RESULTS = Path("../../results/")

DISTANCE_CUTOFFS = {
    "hinge_region": (1, 34),
    "dfg_region": (1, 34),
    "front_pocket": (1, 34),
    "center": (1, 34),
}


def main(fingerprint_generator_path, distance_cutoffs):

    print("Read fingerprints...")
    fingerprint_generator = FingerprintGenerator.from_json(fingerprint_generator_path)
    print(f"Number of fingerprints: {len(fingerprint_generator.data)}")

    print(
        f"Use the following distance minimum/maximum cutoffs"
        f" to identify outlier structures: {distance_cutoffs}"
    )
    remove_structure_ids = []
    for structure_id, fp in fingerprint_generator.data.items():
        if (fp.distances > 34).any().any():
            remove_structure_ids.append(structure_id)
    print(f"Structure IDs to be removed: {remove_structure_ids}")

    print("Remove fingerprints with distance outliers...")
    for structure_id in remove_structure_ids:
        del fingerprint_generator.data[structure_id]
    print(f"Number of fingerprints: {len(fingerprint_generator.data)}")

    fingerprint_generator_clean_path = (
        fingerprint_generator_path.parent / f"{fingerprint_generator_path.stem}_clean.json"
    )
    print(f"Save cleaned fingerprints to {fingerprint_generator_clean_path}...")
    fingerprint_generator.to_json(fingerprint_generator_clean_path)


main(RESULTS / "fingerprints.json", DISTANCE_CUTOFFS)