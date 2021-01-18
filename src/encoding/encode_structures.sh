#!/bin/bash

# Generate kissim fingerprints for a set of KLIFS structures

kissim encode -i "../../data/processed/structure_klifs_ids.txt" -o "../../results/fingerprints.json" -c 7 -l "../../data/external/20210114_KLIFS_HUMAN"
#kissim encode -i "../../data/processed/structure_klifs_ids_test.txt" -o "../../results/fingerprints.json" -c 7 -l "../../data/external/20210114_KLIFS_HUMAN"
#kissim encode -i 109 118 110 113 111 116 112 114 115 117 -o "../../results/fingerprints.json" -c 7 -l "../../data/external/20201223_KLIFS_ABL2_HUMAN"
