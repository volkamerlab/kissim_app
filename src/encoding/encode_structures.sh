#!/bin/bash

# Generate kissim fingerprints for a set of KLIFS structures

kissim encode -i "../../data/processed/structure_klifs_ids.txt" -o "../../results/fingerprints.json" -c 7 -l "../../data/external/20210114_KLIFS_HUMAN"
