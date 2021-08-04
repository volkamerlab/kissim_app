"""
Script to normalize fingerprints.

Usage
-----
normalize_fp.py /path/to/fingerprints.json /path/to/fingerprints_normalized.json
"""

import argparse
from pathlib import Path

from kissim.encoding import FingerprintGenerator

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to fingerprints JSON file.")
parser.add_argument("output", type=str, help="Path to normalized fingerprints JSON file.")
args = parser.parse_args()

path = Path(args.input)
fingerprint_generator = FingerprintGenerator.from_json(path)
fps_normalized_dict = fingerprint_generator._normalize_fingerprints()
fingerprint_generator.data = fps_normalized_dict

path_normalized = Path(args.output)
fingerprint_generator.to_json(path_normalized)
