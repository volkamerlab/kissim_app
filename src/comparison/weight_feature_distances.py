"""
Generates fingerprint distances for different feature weighting schemes.

Run python script:
python weight_feature_distances.py
"""

import argparse
from pathlib import Path

import pandas as pd

from kissim.comparison import FeatureDistancesGenerator, FingerprintDistanceGenerator
from kissim.api.compare import weight_feature_distances

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


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, help="Path to feature distances.", required=True
    )
    parser.add_argument("-c", "--ncores", type=int, help="Number of cores.", required=True)
    args = parser.parse_args()

    return args


def calculate_fingerprint_distances(
    feature_distances_generator_path, feature_weights_dict, n_cores
):

    print("Read feature distances...")
    feature_distances_generator_path = Path(feature_distances_generator_path)
    feature_distances_generator = FeatureDistancesGenerator.from_json(
        feature_distances_generator_path
    )

    print("Generate fingerprint distances for different feature weights...")
    for _, feature_weights in feature_weights_dict.items():
        print(f"Feature weights: {feature_weights}")
        fingerprint_distance_generator = (
            FingerprintDistanceGenerator.from_feature_distances_generator(
                feature_distances_generator, feature_weights, n_cores=n_cores
            )
        )
        feature_weights_tag = "-".join(
            [str(int(i * 1000)) for i in fingerprint_distance_generator.feature_weights]
        )
        fingerprint_distance_json_filepath = (
            feature_distances_generator_path.parent
            / f"fingerprint_distances_{feature_weights_tag}.json"
        )
        print(f"To file {fingerprint_distance_json_filepath}")
        fingerprint_distance_generator.to_json(fingerprint_distance_json_filepath)


def main():
    args = parse_arguments()
    calculate_fingerprint_distances(args.input, FEATURE_WEIGHTS_DICT, args.ncores)


if __name__ == "__main__":
    main()