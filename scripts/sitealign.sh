# Generate SiteAlign comparison data (SiteAlign version 4.0)

# 1. Download the MOL2 pocket files from KLIFS

# 2. Add a random empty TRIPOS tag to the MOL2 to comply with the SiteAlign expectations
for i in `ls pocket_*.mol2`; do echo "@<TRIPOS>RANDOM" >> $i;done

# 3. Create a list of all residues for each MOL2 file
for i in `ls pocket_*.mol2`; do chain=${i%.mol2}; chain=${chain##*chain} ; grep RESIDUE ${i}| awk '{print "'$chain' "substr($2,4,3)}' > ${i}.txt; done

# 4. Prepare the input file for SiteAlign
# Note that only the first entry will be compared to all other entries in this list
for i in `ls pocket_*.mol2`; do echo "${i} ${i}.txt"; done > screening_list

# 5. Run SiteAlign with the optimized settings for the KLIFS alignment
SiteAlign -i screening_list --nb_passes 1 --nrot 16 --ntrans 3 --itrans 1 --irot 0.785 -o screening_output