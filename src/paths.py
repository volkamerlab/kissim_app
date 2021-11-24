"""
Defines paths.
"""

from pathlib import Path

PATH_DATA = Path(__file__).parent / "../data"

PATH_RESULTS = Path(__file__).parent / "../results"
if not PATH_RESULTS.exists():
    # If running on the CI, we won't have the results folder;
    # use the results_test folder instead
    print(f"Folder does not exist: {PATH_RESULTS}")
    PATH_RESULTS = Path(__file__).parent / "../test/results"
    print(f"Use test folder instead: {PATH_RESULTS}")

PATH_DATA_KLIFS_DOWNLOAD = PATH_DATA / "external/structures/20210902_KLIFS_HUMAN"
if not PATH_DATA_KLIFS_DOWNLOAD.exists():
    print(f"Folder does not exist: {PATH_DATA_KLIFS_DOWNLOAD}")
    PATH_DATA_KLIFS_DOWNLOAD = Path(__file__).parent / "../test/data/external/klifs_test"
    print(f"Use test folder instead: {PATH_DATA_KLIFS_DOWNLOAD}")
