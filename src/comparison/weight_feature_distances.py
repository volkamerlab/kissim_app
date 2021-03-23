"""
Generates fingerprint distances for different feature weighting schemes.

Run python script:
python weight_feature_distances.py
"""

from pathlib import Path

import pandas as pd

from kissim.comparison import FeatureDistancesGenerator, FingerprintDistanceGenerator
from kissim.api.compare import weight_feature_distances

RESULTS = Path("../../results/")

FEATURE_WEIGHTS_DICT = {
    "15": None,
    "100": [1.0 / 8] * 8 + [0] * 4 + [0] * 3,
    "010": [0] * 8 + [1.0 / 4] * 4 + [0] * 3,
    "001": [0] * 8 + [0] * 4 + [1.0 / 3] * 3,
    "110": [0.5 / 8] * 8 + [0.5 / 4] * 4 + [0] * 3,
    "101": [0.5 / 8] * 8 + [0] * 4 + [0.5 / 3] * 3,
    "011": [0] * 8 + [0.5 / 4] * 4 + [0.5 / 3] * 3,
    "111": [1.0 / 3 / 8] * 8 + [1.0 / 3 / 4] * 4 + [1.0 / 3 / 3] * 3,
}

print("Read feature distances...")
feature_distances_generator = FeatureDistancesGenerator.from_json(
    RESULTS / "feature_distances.json"
)

print("Generate fingerprint distances for different feature weights...")
for feature_weights_name, feature_weights in FEATURE_WEIGHTS_DICT.items():
    print(f"Feature weights: {feature_weights}")
    fingerprint_distance_generator = FingerprintDistanceGenerator.from_feature_distances_generator(
        feature_distances_generator, feature_weights
    )
    feature_weights_tag = "-".join(
        [str(int(i * 1000)) for i in fingerprint_distance_generator.feature_weights]
    )
    fingerprint_distance_json_filepath = (
        RESULTS / f"fingerprint_distances_{feature_weights_tag}.json"
    )
    print(f"To file {fingerprint_distance_json_filepath}")
    fingerprint_distance_generator.to_json(fingerprint_distance_json_filepath)