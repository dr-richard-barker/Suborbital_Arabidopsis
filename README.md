# Suborbital *Arabidopsis* Omics (Blue Origin NS-26)

Re-analysis and multi-mission comparative omics of the Blue Origin New Shepard NS-26 human-tended spaceflight experiment:
> **Reference:** Ferl, R.J., Strickland, H.F., Callaham, J.B. et al. *Suborbital spaceflight reveals rapid changes in gene expression accompanying the transition to and from space.* **npj Microgravity** 12, 86 (2026). [doi:10.1038/s41526-026-00645-6](https://doi.org/10.1038/s41526-026-00645-6).

Integrated into the **CoSE (Collaborative Science Environment)** data presentation and GitHub Pages system.

---

## 1. Study Overview & Flight Profile

* **Vehicle:** Blue Origin New Shepard **NS-26** (launched August 29, 2024 from Launch Site One, West Texas).
* **Organism:** *Arabidopsis thaliana* (Col-0, 8-day-old seedlings grown on phytagel mesh coupons).
* **Hardware:** Kennedy Space Center Fixation Tubes (KFTs) pre-loaded with RNAlater fixative.
* **Sampling Phases (Paired Real-Time Flight vs. Ground Controls):**
  1. `EE` (Escape Enabled): Pre-launch baseline on tower (~T-16 min, 7:51 AM).
  2. `CS` (Capsule Separation): Post-boost / microgravity onset (~T+2.8 min, 8:10 AM).
  3. `RE` (Reentry): End of ~3.5 min microgravity coast (~T+5.3 min, 8:12 AM).
  4. `LN` (Landing): Touchdown (~T+10.5 min, 8:17 AM).
* **Sequencing:** Illumina NovaSeq X, $2 \times 150$ bp, ~60M reads/sample across dissected Leaves and Roots.

---

## 2. Repository & Public Data Status

* **NASA OSDR:** Cited under **`OSD-948`**. (Currently pending public indexing on OSDR portal).
* **NCBI GEO:** Deposited under **`GSE312580`**. (Currently in private / embargoed status).
* **Supplementary Peer-Reviewed Data:** Fully ingested from Springer Nature CDN (`MOESM1` & `MOESM2`).
* **Automated Poller:** `scripts/01_poll_repositories.py` polls OSDR and GEO APIs to notify and trigger raw data download the moment the embargo lifts.

---

## 3. Directory Layout

```
Suborbital_Arabidopsis/
├── data/
│   ├── raw/                      # Downloaded MOESM1, MOESM2, OSD-624 metadata
│   └── processed/                # Tidy master DEGs, phase summaries, trajectories
├── scripts/
│   ├── 00_download_data.py       # Ingests published supplements and OSDR comparator
│   ├── 01_poll_repositories.py   # Watcher for OSD-948 and GSE312580
│   ├── 02_comparative_degs.py    # DEG cleaning and cross-mission metrics
│   ├── 03_temporal_splines.py    # Continuous trajectory modeling & archetypes
│   └── 04_generate_figures.py    # Publication-ready CoSE visualizations
├── figures/                      # High-resolution PNGs (300 DPI)
├── docs/                         # CoSE-styled GitHub Pages presentation portal
│   ├── assets/
│   │   ├── style.css             # CoSE brand styles and dark-mode tokens
│   │   └── figures/              # Web-optimized figures
│   ├── .nojekyll
│   └── index.html                # Interactive portal and data explorer
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 4. Key Re-Analysis Findings

1. **Strong Organ Divergence:**
   * Leaves mount a 4× stronger response than roots (617 leaf DEGs vs. 119 root DEGs at Reentry).
   * Only 71 genes are shared between leaves and roots at microgravity coast (RE).
2. **Microgravity Coast Peak for Proteotoxic Stress:**
   * Dynamic trajectory modeling revealed that **505 DEGs** peak specifically during the microgravity coast phase (`RE`).
   * This coast cohort harbors **72% of all heat stress chaperones (70/97)** and **59% of reactive oxygen species genes (178/303)**.
   * Thermal dataloggers verified maximum temperatures $<30^\circ\text{C}$ in-flight, proving the heat shock response is an acute non-thermal reaction triggered by entering microgravity.
3. **Cross-Mission Suborbital Concordance:**
   * 207 DEGs replicate between Blue Origin NS-26 (vertical rocket ascent) and Virgin Galactic Unity 22 (`OSD-624`, horizontal air-launch).
   * 83 DEGs are shared with long-term orbital spaceflight on the ISS (`APEX`).

---

## 5. Usage

```bash
# Activate environment
source .venv/bin/activate

# Check repository status (OSD-948 / GSE312580)
python3 scripts/01_poll_repositories.py

# Run continuous background watcher (hourly)
python3 scripts/01_poll_repositories.py --watch 3600

# Re-run trajectory analysis and figures
python3 scripts/03_temporal_splines.py
python3 scripts/04_generate_figures.py

# Preview the CoSE GitHub Pages presentation portal locally
python3 -m http.server 8080 --directory docs
```
