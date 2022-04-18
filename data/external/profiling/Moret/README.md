# Moret dataset

### Download

Data downloaded from https://www.smallmoleculesuite.org/ as publised in [Moret et al. 2019](https://doi.org/10.1016/j.chembiol.2019.02.018) using the following parameters:

1. Use targets from example gene list "Kinome".
2. Select selectivity "Most selective" and "Semi-selective" (see Comments for details on selectivity scores).
3. Select approval phase "Approved".
4. Include compounds from chemicalprobes.org (4.0 star rating only).
5. View table per target ("Display per entry").
6. Select maximum "Minimum affinity for query target" and minimum "Minimum number of affinity measures".
7. Download the library as CSV.


### Comments

Selectivity is defined as follows in the [paper by Moret et al. 2019](https://doi.org/10.1016/j.chembiol.2019.02.018):

> Selectivity score is a continuous variable; however, for convenience we also assigned descriptive labels to different classes of compound-target interaction. 

> **Most selective (MS)** interactions meet four criteria: 
(1) the difference in q1 values computed for the distributions of on- and off-target data is not less than 100-fold, 
(2) the distributions of on-target and off-target binding affinities differ with p value below 0.1 
(3) the compound has at least 4-fold more off-target than on-target affinity measurement (so that data bias is below 20%), 
(4) at least two published reports establish that the affinity for drug-target interaction is less than 100 nM. 

> **Semi-selective (SS)** interactions have slightly less stringent criteria: 
(1) the difference in q1 values is not less than 10-fold, 
(2) the p value for on and off-target binding affinities is below 0.1, 
(3) at least four publications report affinity less than 1 μM (because the affinity cutoff is less stringent than for interactions meeting MS criteria, more data-points are needed to establish confidence in binding). 

> **Poly-selective (PS)** interactions are those for which: 
(1) q1 values for on- and off-target binding are similar, 
(2) on-target q1 is under 9 μM, 
(3) data bias is under 20%. 

> **Unknown (UN)** interactions are those for which the compound has not been sufficiently probed for off-target binding but fulfills the PS requirements with respect potency and affinity for the nominal target.