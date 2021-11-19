# Run this script in the CI to generate dummy kissim data!
#
# Dummy data:
# - Structure KLIFS ID: 111; ABL2 kinase
# - Structure KLIFS ID: 113; ABL2 kinase
# - Structure KLIFS ID: 1641; CHK1 kinase
# - Structure KLIFS ID: 9122; ADCK3 kinase

NCORES=1
KLIFS_DOWNLOAD=klifs_test

# Generate dummy kissim data for "all" conformations
results=results/all
mkdir $results
kissim encode -i data/processed/structure_klifs_ids_test.txt -o $results/fingerprints.json -c $NCORES -l data/external/structures/$KLIFS_DOWNLOAD
kissim outliers -i $results/fingerprints.json -d 34 -o $results/fingerprints_clean.json
kissim normalize -i $results/fingerprints_clean.json -o $results/fingerprints_normalized.json -f
kissim compare -i $results/fingerprints_normalized.json -o $results -c $NCORES
kissim weights -i $results/feature_distances.csv -o $results/fingerprint_distances_100.csv -w 0.125 0.125 0.125 0.125 0.125 0.125 0.125 0.125 0 0 0 0 0 0 0 
kissim weights -i $results/feature_distances.csv -o $results/fingerprint_distances_010.csv -w 0 0 0 0 0 0 0 0 0.25 0.25 0.25 0.25 0 0 0
kissim weights -i $results/feature_distances.csv -o $results/fingerprint_distances_001.csv -w 0 0 0 0 0 0 0 0 0 0 0 0 0.333 0.333 0.333
kissim weights -i $results/feature_distances.csv -o $results/fingerprint_distances_110.csv -w 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.125 0.125 0.125 0.125 0 0 0
kissim weights -i $results/feature_distances.csv -o $results/fingerprint_distances_101.csv -w 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0.062 0 0 0 0 0.166 0.166 0.166
kissim weights -i $results/feature_distances.csv -o $results/fingerprint_distances_011.csv -w 0 0 0 0 0 0 0 0 0.125 0.125 0.125 0.125 0.166 0.166 0.166
kissim weights -i $results/feature_distances.csv -o $results/fingerprint_distances_111.csv -w 0.041 0.041 0.041 0.041 0.041 0.041 0.041 0.041 0.083 0.083 0.083 0.083 0.111 0.111 0.111

# Copy dummy kissim data for "dfg_in" and "dfg_out" conformations
# We are simply copying the dataset here, since we only need to set up the correct folder structures
# the data content is irrelevent
mkdir results/dfg_in
cp results/all/* results/dfg_in/
mkdir results/dfg_out
cp results/all/* results/dfg_out/