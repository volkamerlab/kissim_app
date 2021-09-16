"""
Defines paths.
"""

from pathlib import Path

PATH_DATA = Path(__file__).parent / "../data"
PATH_RESULTS = Path(__file__).parent / "../results"

PATH_DATA_KLIFS_DOWNLOAD = PATH_DATA / "external/structures/20210902_KLIFS_HUMAN"
PATH_DATA_KLIFS_DOWNLOAD_TEST = PATH_DATA / "external/structures/klifs_test"
