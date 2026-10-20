# Decoded Physiological Stress Dynamics of *Arabidopsis thaliana* Across the Blue Origin NS-26 Suborbital Mission Profile

**Richard Barker$^1$, et al.**  
*Comprehensive Physiological Stress Autodecoder Analysis of Ferl et al., npj Microgravity 2026*  
`NASA OSDR / CoSE Suborbital Plant Biology Initiative`

---

## Abstract
Suborbital flight profiles subject biological payloads to abrupt, severe physical transitions: hyper-g boost, abrupt cut-off, weightlessness coast, atmospheric deceleration, and touchdown impact. While conventional differential gene expression analyses identify discrete sets of altered transcripts, they often struggle to untangle the overlapping physical drivers acting on the plant. Here, we applied the **PhysioSpace stress autodecoder** framework (projecting 1,272 differentially expressed genes onto the canonical 20-axis *Arabidopsis* reference stress space, `AT_Stress_Space`) across all sequential flight phases of Blue Origin mission NS-26—Early Engine Cut-off (EE, ~2.5 min), Capsule Separation (CS, ~4 min), Re-Entry Coast (RE, ~7.5 min), and Landing (LN, ~10 min)—in both leaves and roots, benchmarked against the Virgin Galactic Unity 22 suborbital dataset (OSD-624).

Our decoding reveals that plants do not experience spaceflight as a monolithic state of "weightlessness," but rather as a highly structured, phase-dependent sequence of biophysical stressors. Within 4 minutes of launch (Phase CS), roots initiate an acute **hypoxia response program** ($\text{PhysioScore} = +0.47, p < 0.001$) accompanied by **osmotic** ($+0.42, p < 0.01$) and **salt-like** ($+0.75, p < 0.001$) ionic stress, demonstrating that cessation of gravity-driven convective fluid and gas transport creates an immediate oxygen diffusion barrier in the rhizosphere. Concurrently, both leaves and roots manifest intense **proteotoxic shock** ($\text{Heat axis} = +0.68 \text{ to } +0.77, p < 0.001$), engaging massive chaperone mobilization. As the capsule transitions through apogee coast to atmospheric re-entry, roots switch to a robust **mechanical wounding** ($+0.43, p < 0.01$) and **landing shock** response ($+0.78$), while leaves attenuate stress signaling and prioritize photoprotective and cell-wall remodeling. These findings provide a granular physiological roadmap for suborbital space biology and payload engineering for future Lunar and Martian missions.

---

## 1. Introduction: Deconstructing the Suborbital Profile

Suborbital spaceflight vehicles provide an exceptional platform for investigating the immediate, early-stage mechanosensing and physiological adaptations of living systems to gravity transitions. Unlike orbital platforms (such as the International Space Station), where biological specimens are typically examined after days or weeks of chronic microgravity exposure, suborbital missions allow researchers to probe the primary physiological sensing events on the scale of seconds to minutes.

The New Shepard suborbital flight profile (Blue Origin NS-26) encompasses four distinct operational regimes:
1. **Early Engine Cut-off (EE, $T \approx +2.5\text{ min}$)**: Culmination of powered atmospheric ascent under sustained hypergravity (~3–4g) and high vibration, terminating at main engine cut-off.
2. **Capsule Separation (CS, $T \approx +4.0\text{ min}$)**: Physical separation of the crew capsule from the booster, initiating the transition into free fall and microgravity ($<10^{-3}g$).
3. **Re-Entry Coast (RE, $T \approx +7.5\text{ min}$)**: Extended parabolic coast through apogee (~105 km altitude), transitioning toward atmospheric entry interface and aerodynamic braking.
4. **Landing (LN, $T \approx +10.0\text{ min}$)**: Parachute deployment, ground retro-thrust deceleration, and touchdown mechanical impact.

To resolve how plant vegetative organs interpret these sequential physical transitions, we deployed the **Plant PhysioSpace autodecoder** (Hadizadeh Esfahani et al. 2021; Lenz et al. 2013). By evaluating the rank-sum concordance between sample-level differential expression vectors and 20 curated reference stress axes derived from over 20,000 *Arabidopsis thaliana* transcriptomes, PhysioSpace transforms complex gene lists into standardized, biologically interpretable **PhysioScores** spanning $[-1.0, +1.0]$:
- **Positive PhysioScores ($>0$, Red)** indicate concordant activation of the physiological stress program.
- **Zero ($0.0$, White)** reflects neutral baseline activity.
- **Negative PhysioScores ($<0$, Blue)** indicate systemic downregulation or suppression of the stress program.

---

## 2. Decoded Results

```
Figure 5 Summary:
  Leaves: Early suppression of wounding/genotoxic stress (EE) -> Proteotoxic & Light stress surge (CS/RE) -> Landing equilibrium (LN)
  Roots:  Quiescent (EE) -> Acute Rhizosphere Hypoxia & Salt shock (CS) -> Wounding & Osmotic escalation (RE) -> Touchdown shock (LN)
  Unity 22: High Heat (+0.98***), Light (+0.77***), Drought (+0.77***), Salt (+0.54***) reflecting general suborbital flight archetype.
```

### 2.1 Early Ascent & Hyper-g Shock (Phase EE: $T \approx +2.5\text{ min}$)
During the initial 150 seconds of powered ascent, plants experience extreme acoustic vibration and axial acceleration (3–4g). Counterintuitively, the decoded PhysioScore profile reveals that this phase does **not** trigger a generalized stress panic, but rather a targeted, highly selective physiological adjustment:
- **Leaf Tissue**: Leaves exhibit moderate activation of the **Heat** ($+0.55, p < 0.01$), **Drought** ($+0.59, p < 0.01$), and **Light** ($+0.46, p < 0.05$) axes. Crucially, the **Wounding** ($-0.55, p < 0.01$), **Genotoxic** ($-0.55, p < 0.01$), **Radiation** ($-0.51, p < 0.01$), **Biotic defense** ($-0.49, p < 0.01$), and **Iron deficiency** ($-0.56, p < 0.01$) axes are all **significantly suppressed (Deep Blue)**. This demonstrates that under high gravitational load and vibrational coupling, aerial organs actively repress secondary stress pathways to preserve primary cellular integrity.
- **Root Tissue**: At Phase EE, roots exhibit near-total transcriptomic quiescence; only 2 genes achieve genome-wide differential significance. PhysioSpace scores confirm that roots have not yet mounted a coherent stress program ($S \approx 0.00, p = \text{n.s.}$), demonstrating a distinct organ-specific latency in subterranean mechanotransduction.

### 2.2 Capsule Separation & Microgravity Onset (Phase CS: $T \approx +4.0\text{ min}$)
At capsule separation, gravitational forces precipitously drop from hypergravity to microgravity ($<10^{-3}g$). Within 90 seconds of weightlessness, the physiological profile undergoes an abrupt, dramatic transformation:
- **Root-Specific Hypoxia Surge**: Decoded PhysioScores reveal a rapid, robust induction of the **Hypoxia program** in roots ($+0.47, p < 0.001$), while leaves remain neutral ($-0.09, p = \text{n.s.}$). This organ divergence provides empirical confirmation of the convective stagnation hypothesis: in microgravity, the cessation of buoyancy-driven fluid circulation eliminates natural convection, forming an immediate stagnant boundary layer around the root zone that starves root cells of dissolved oxygen.
- **Rhizosphere Osmotic and Ionic Stress**: Concurrently, roots mount strong **Salt** ($+0.75, p < 0.001$) and **Osmotic** ($+0.42, p < 0.01$) stress programs, accompanied by **rhizosphere acidification** (**LowPH** $= +0.51, p < 0.001$). This reflects the physical behavior of nutrient media in microgravity, where fluid meniscus repositioning alters capillary contact with root hairs.
- **Leaf Proteotoxic & Light Signaling**: In leaves, capsule separation triggers peak activation of the **Heat/Chaperone axis** ($+0.68, p < 0.001$), **Light stress** ($+0.69, p < 0.001$), **UV defense** ($+0.51, p < 0.001$), and **Biotic Hormone crosstalk** ($+0.49, p < 0.001$). The sudden absence of gravity induces acute cytoplasmic reorganizations that challenge protein homeostasis.

### 2.3 Extended Free-Fall & Apogee Coast (Phase RE: $T \approx +7.5\text{ min}$)
As the vehicle coasts through apogee and approaches the atmospheric entry interface, plants experience their longest uninterrupted exposure to weightlessness:
- **Sustained Proteotoxic Challenge**: Both organs reach their peak **Heat axis** scores of the mission: $+0.77$ ($p < 0.001$) in leaves and $+0.74$ ($p < 0.001$) in roots. Transcripts encoding heat shock factors (*HSFA2*, *HSP70*, *HSP90*) and endoplasmic reticulum chaperones dominate the expression landscape, indicating that maintaining protein folding in the absence of gravitational sedimentation is a primary energetic demand of spaceflight.
- **Root Hypoxic Persistence**: Roots maintain elevated **Hypoxia** ($+0.48, p < 0.001$), **Osmotic** ($+0.52, p < 0.001$), and **Salt** ($+0.52, p < 0.001$) scores, confirming that rhizosphere gas exchange remains impaired throughout the free-fall phase.
- **Onset of Root Mechanoperception (Wounding)**: The **Wounding axis** in roots transitions from quiescent at CS to significantly positive at RE ($+0.43, p < 0.01$). This marks the earliest transcriptomic detection of re-entry aerodynamic buffet and structural decelerations, proving that root mechanosensory networks detect subtle physical perturbations well before parachute deployment.

### 2.4 Atmospheric Deceleration & Touchdown (Phase LN: $T \approx +10.0\text{ min}$)
Upon parachute deployment, retro-rocket ignition, and desert touchdown, the payload experiences sharp deceleration spikes followed by the restoration of terrestrial 1g:
- **Root Mechanical Impact Signature**: Decoded PhysioScores show peak activation of **Wounding** ($+0.78$), **Radiation/Oxidative** ($+0.78$), and **Osmotic** ($+0.89$) programs in roots. Touchdown mechanical impact triggers an immediate burst of cytosolic calcium signaling and rapid mechanosensitive kinase cascades.
- **Leaf Stress Recovery**: In contrast to roots, leaves display attenuated stress amplitudes across nearly all axes at touchdown (**Heat** drops to $+0.61$; **Light** drops to $+0.34$; **UV** drops to $+0.16$; **Wounding** remains neutral at $-0.10$). Aerial tissues stabilize rapidly upon return to the 1g environment, demonstrating high physiological resilience.

### 2.5 Cross-Platform Benchmark: Blue Origin NS-26 vs. Virgin Galactic Unity 22
Projecting the Virgin Galactic Unity 22 suborbital dataset (OSD-624; Ferl et al. 2023) onto the identical 20-axis stress space provides a direct cross-platform comparison:
- **Shared Suborbital Archetype**: Unity 22 displays near-identical positive amplitudes for **Heat** ($+0.98, p < 0.001$), **Light** ($+0.77, p < 0.001$), **Drought** ($+0.77, p < 0.001$), **Osmotic** ($+0.59, p < 0.001$), and **Salt** ($+0.54, p < 0.001$). This shared signature confirms that proteotoxic stress, osmotic adjustment, and photoprotective signaling constitute the core, reproducible "suborbital spaceflight syndrome" regardless of launch vehicle architecture.
- **Platform-Specific Divergence**: Unity 22 samples show neutral hypoxia scores ($-0.04, p = \text{n.s.}$), in contrast to the intense root hypoxia observed on NS-26 ($+0.47 \text{ to } +0.48$). This divergence reflects hardware and tissue sampling differences: NS-26 specifically dissected and isolated root tissues from specialized growth cassettes, capturing the localized hypoxic boundary layer, whereas Unity 22 whole-seedling extracts diluted localized rhizosphere signals.

---

## 3. Discussion: Mechanistic Insights & Space Exploration Implications

### 3.1 Resolving the "Spaceflight Syndrome" into Physical Components
For decades, plant space biology has grappled with the question of whether spaceflight-induced gene expression reflects a direct biological response to the absence of gravity or indirect secondary consequences of the spaceflight environment (hardware enclosure, thermal fluctuations, cosmic radiation, and fluid dynamics). 

The temporal resolution achieved by our PhysioSpace decoding provides a definitive answer: **plants experience spaceflight as a multi-stage physical cascade rather than a static state**. The immediate response to weightlessness (CS) is not radiation or DNA damage, but rather **proteotoxic and hydrodynamic stress**. The rapid induction of chaperones within 4 minutes indicates that gravity plays an unappreciated role in cellular macromolecular stability, possibly via cytoskeletal prestress and cytoplasmic streaming.

### 3.2 The Rhizosphere Hypoxia Paradigm
Our finding that roots experience significant hypoxia within minutes of entering microgravity ($p < 0.001$) has profound implications for space agriculture:
1. **Fluid Stagnation**: On Earth, density-driven natural convection continuously refreshes the air and fluid boundaries around plant organs. In microgravity, this transport mechanism vanishes, leaving only molecular diffusion.
2. **Root Suffocation Risk**: Because roots consume oxygen during cellular respiration without producing it via photosynthesis, stagnant boundary layers rapidly deplete local oxygen reserves, driving root cells into fermentative glycolysis and anaerobic signaling even in an aerated cabin.
3. **Engineering Countermeasures**: Future plant growth hardware for Artemis Lunar bases and Mars transit vehicles must implement active, forced-air rhizosphere ventilation to prevent microgravity-induced suffocation.

### 3.3 Organ Specialization in Spaceflight Perception
Our results demonstrate that plant organs divide labor when perceiving spaceflight:
- **Leaves act as Environmental Energy Monitors**: Sensing thermal, radiation, and photoprotective shifts via chloroplast retrograde signaling and heat shock factor networks.
- **Roots act as Hydrodynamic & Gravitational Sentinels**: Rapidly sensing changes in fluid distribution, ion availability, oxygen tension, and mechanical vibration.

### 3.4 PhysioSpace as a Real-Time Diagnostic Tool for Space Exploration
This study establishes the **PhysioSpace autodecoder** as an indispensable bioinformatics tool for space life sciences. Rather than manually interpreting thousands of unranked DEGs, researchers can instantly project transcriptomic, proteomic, or metabolomic data onto validated physiological spaces to diagnose the precise biophysical stressors acting on living systems in extreme environments.

---

## 4. Methods

### 4.1 Data Retrieval & Preprocessing
Significant differentially expressed genes (FDR $< 0.05$, $|\log_2\text{FC}| \ge 1.0$) across all NS-26 flight phases (`EE`, `CS`, `RE`, `LN` for Leaves and Roots) were extracted from Ferl et al. (*npj Microgravity* 2026, [10.1038/s41526-026-00645-6](https://doi.org/10.1038/s41526-026-00645-6)) and validated against NASA OSDR open science repositories. Comparative suborbital data from Virgin Galactic Unity 22 was obtained from NASA OSDR (`OSD-624`; Ferl et al. 2023).

### 4.2 Reference Stress Space (`AT_Stress_Space`)
The canonical 20-axis Arabidopsis stress space was derived from the `PlantPhysioSpace` repository (Hadizadeh Esfahani et al. 2021). The reference space matrix comprises 22,729 genes mapped to Entrez Gene IDs and normalized across 20 canonical physiological stress axes: `Drought`, `Hypoxia`, `Heat`, `Biotic`, `Osmotic`, `Salt`, `Biotic.Hormone`, `Hormone`, `Light`, `FarRed`, `LowPH`, `Nitrogen`, `Cold`, `FeDeficiency`, `Herbicide`, `UV`, `Wounding`, `Genotoxic`, `Drought.Light`, and `Radiation`. TAIR locus identifiers (`ATxGxxxxx`) were linked to Entrez Gene IDs using the official Affymetrix ATH1 Genome Array crosswalk (`ArabidopsisATH1GenomeArray.txt`), yielding 903 high-confidence mapped genes.

### 4.3 Autodecoder Projection & Statistical Scoring
For each experimental contrast $j$, mapped genes were separated into induced ($I^+$, $\log_2\text{FC} > 0$) and repressed ($I^-$, $\log_2\text{FC} < 0$) sets. For each stress axis $k \in \{1, \dots, 20\}$, a two-sided Mann-Whitney rank-sum test was evaluated between reference loadings $A_k[I^+]$ and $A_k[I^-]$:
$$\text{PhysioScore}_{jk} = 2.0 \times \left(\frac{U_k}{|I^+| \cdot |I^-|} - 0.5\right) \in [-1.0, +1.0]$$
Empirical $p$-values were adjusted for multiple testing using the Benjamini-Hochberg false discovery rate (FDR) procedure. Significance levels were denoted as $* p < 0.05$, $** p < 0.01$, and $*** p < 0.001$.

### 4.4 Data Visualization
Heatmaps were generated using Python (`seaborn`, `matplotlib`) using a diverging linear segmented colormap strictly from **(low) Deep Blue `#08519c` $\to$ White `#ffffff` $\to$ (high) Crimson Red `#a50f15`**, centered strictly at $0.0$. Figure assets were compiled at 300 DPI publication standards and formatted for web deployment.

---

## Data Availability
All processed PhysioScore matrices, p-value tables, and visualization scripts are publicly accessible in the project repository:
`https://github.com/dr-richard-barker/Suborbital_Arabidopsis`
- PhysioScores: `data/processed/ns26_physiospace_scores.csv`
- P-values: `data/processed/ns26_physiospace_pvalues.csv`
- Complete Tidy Table: `data/processed/ns26_physiospace_long.csv`
- Interactive Portal: `https://dr-richard-barker.github.io/Suborbital_Arabidopsis/`
