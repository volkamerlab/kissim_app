# Manual curation of kinase inhibitor on-targets

We will assign main on-targets manually based on the following table including
- Main on-targets reported in literature, starting point are DrugBank and PKIDB 
- Use KinMap kinase names (since we are using the Karaman dataset provided by KinMap)
- For multitargeted ligands define multiple targets

| Approved kinase inhibitor                            | Intended kinase target |
|------------------------------------------------------|---------------------------------------------------------|
| [Erlotinib](https://go.drugbank.com/drugs/DB00530)   | EGFR |
| [Gefitinib](https://go.drugbank.com/drugs/DB00317)   | EGFR |
| [Lapatinib](https://go.drugbank.com/drugs/DB01259)   | EGFR, ERBB2 |
| [Tofacitinib](https://go.drugbank.com/drugs/DB08895) | JAK1, JAK2, JAK3 |
| [Vandetanib](https://go.drugbank.com/drugs/DB05294)  | VEGFR2, EGFR, RET; [see paper](https://www.ema.europa.eu/en/documents/assessment-report/caprelsa-epar-public-assessment-report_en.pdf) |
| [Imatinib](https://go.drugbank.com/drugs/DB00619)    | multitargeted inhibitor - TK: ABL1, KIT, PDGFRa; [see paper](https://www.hindawi.com/journals/cherp/2014/357027/) |
| [Sunitinib](https://go.drugbank.com/drugs/DB01268)   | multitargeted inhibitor - TK: VEGFR1/2, PDFGRa/b, KIT, FLT2, RET, CSF1R; [see paper](https://link.springer.com/article/10.2165/11318860-000000000-00000) |
| [Dasatinib](https://go.drugbank.com/drugs/DB01254)   | multitargeted inhibitor - TK: ABL1 (BCRABL), SRC, Eph\_ (Ephrins), \_GFR (GFR); see DrugBank Identification > Description |
| [Sorafenib](https://go.drugbank.com/drugs/DB00398)   | multitargeted inhibitor - TK/TKL (Raf/Mek/Erk pathways): RAF\_ (Raf) \[TKL\], PDFGR\_ (PDFG), VEGF2/3, KIT; see DrugBank Identification > Description |