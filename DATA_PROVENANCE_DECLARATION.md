# Data Provenance & FAIR Open Science Declaration

**Project:** Suborbital *Arabidopsis* Multi-Mission Transcriptomics (Blue Origin NS-26)  
**Maintained by:** Collaborative Science Environment Inc. (CoSE) · Madison, Wisconsin  
**Author:** Dr. Richard Barker (`dr.richard.barker@gmail.com`)  
**Date:** October 19, 2026  

---

## 1. Primary Study Citation & Data Ingestion

The biological data analyzed in this repository originate from the peer-reviewed study:
> **Citation:** Ferl, R.J., Strickland, H.F., Callaham, J.B., Aknadibossian, V., Marr, O., Adhikari, P., & Paul, A.-L. (2026). *Suborbital spaceflight reveals rapid changes in gene expression accompanying the transition to and from space.* **npj Microgravity**, 12(1), Article 86.  
> **DOI:** [10.1038/s41526-026-00645-6](https://doi.org/10.1038/s41526-026-00645-6)  
> **Published:** August 4, 2026 (Version of Record: October 15, 2026).

### Ingested Datasets
1. **Supplementary Data 01 (`41526_2026_645_MOESM1_ESM.xlsx`):**
   * Full DEG heatmap matrix for 1,272 *Arabidopsis thaliana* (Col-0) genes across 4 flight phases (`EE`, `CS`, `RE`, `LN`) in Leaves and Roots.
   * Includes $\log_2(\text{Fold Change})$ values vs. time-matched ground controls, FDR-adjusted $p$-values, hierarchical clustering values (1-Cos Avg, 1-Cos S, 1-Cos C), and cross-study reference flags.
2. **Supplementary Data 02 (`41526_2026_645_MOESM2_ESM.xlsx`):**
   * Curated Gene Lists: ROS Wheel Core Groups I–VIII, Heat shock chaperones/factors, Cell wall biosynthesis, Housekeeping negative controls, and Flowering controls.

---

## 2. Public Repository Audit & Status (Checked Live 2026-10-18)

| Repository | Identifier | Declared Status in Paper | Audited Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **NASA GeneLab / OSDR** | **`OSD-948`** | Deposited | 🟡 Pending Indexing (0 hits) | Endpoint polled automatically via `scripts/01_poll_repositories.py`. |
| **NCBI GEO** | **`GSE312580`** | Deposited (BioProject) | 🟡 Private / Embargoed | Scheduled for release following Version of Record publication. |
| **NASA OSDR Benchmark** | **`OSD-624`** | Public Reference | 🟢 Available | Virgin Galactic Unity 22 suborbital dataset (Ferl et al., 2023). |
| **NASA OSDR Benchmark** | **`OSD-406`** | Public Reference | 🟢 Available | Autonomous suborbital flights (Blue Origin NS-12 & VG VP-03). |

---

## 3. FAIR Science Principles

* **Findable:** Standard AGI locus identifiers (`ATxGxxxxx`), NCBI taxonomy ID 3702, and explicit DOI citations.
* **Accessible:** Openly downloadable CSV/Parquet tables in `data/processed/` and live interactive presentation portal via GitHub Pages.
* **Interoperable:** Tidy data structures matching Bioconductor and Python data science ecosystems.
* **Reusable:** Permissively licensed under MIT License, with version-locked `requirements.txt` and fully reproducible scripts (`00` through `05`).
