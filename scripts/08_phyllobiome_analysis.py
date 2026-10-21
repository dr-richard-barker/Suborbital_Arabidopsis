#!/usr/bin/env python3
"""scripts/08_phyllobiome_analysis.py
Investigates evidence for phyllobiome / plant-microbe interactions in the NS-26
suborbital RNA-seq dataset and models how host-microbe dynamics change during
the suborbital flight profile.

Generates Figure 6:
  - Panel A: PhysioSpace Biotic & Biotic.Hormone trajectories (Leaves vs Roots)
  - Panel B: Heatmap of host phyllobiome-responsive defense genes (PR1, Defensins, WRKYs, PMEs)
  - Panel C: Metatranscriptomic unmapped-read mining architecture for suborbital RNA-seq
  - Panel D: Historical NASA OSDR seedling core microbiome distribution (OSD-37, 38, 120, 217, 522)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data", "processed")
FIG_DIR = os.path.join(ROOT_DIR, "figures")
DOCS_FIG_DIR = os.path.join(ROOT_DIR, "docs", "assets", "figures")
DOCS_DATA_DIR = os.path.join(ROOT_DIR, "docs", "assets", "data")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(DOCS_FIG_DIR, exist_ok=True)
os.makedirs(DOCS_DATA_DIR, exist_ok=True)

def main():
    print("=== Step 1: Loading NS-26 DEGs and PhysioScores ===")
    degs_path = os.path.join(DATA_DIR, "ns26_degs_master.csv")
    scores_path = os.path.join(DATA_DIR, "ns26_physiospace_scores.csv")
    pvals_path = os.path.join(DATA_DIR, "ns26_physiospace_pvalues.csv")

    degs = pd.read_csv(degs_path)
    df_scores = pd.read_csv(scores_path, index_col=0)
    df_pvals = pd.read_csv(pvals_path, index_col=0)

    # 1. Host phyllobiome-responsive genes
    keywords = ["defense", "pathogen", "biotic", "chitinase", "pr1", "wrky", "pectin", "defensin", "peroxidase", "glutathione"]
    hits = []
    for idx, row in degs.iterrows():
        sym = str(row.get("gene_symbol", ""))
        desc = str(row.get("gene_description", ""))
        text = (sym + " " + desc).lower()
        for kw in keywords:
            if kw in text:
                hits.append(row)
                break
    df_hits = pd.DataFrame(hits)

    # Filter top representative biotic/phyllobiome genes with non-null fold-changes
    key_gene_defs = [
        ("AT1G69940", "PPME1"),
        ("AT1G48020", "PMEI1"),
        ("AT2G47030", "PME4"),
        ("AT1G55010", "PDF1.5"),
        ("AT1G64195", "PDF-like 35"),
        ("AT1G68905", "PDF-like 262"),
        ("AT2G14610", "PR1"),
        ("AT1G80590", "WRKY66"),
        ("AT2G44745", "WRKY12"),
        ("AT4G22070", "WRKY31"),
        ("AT2G46400", "WRKY46"),
        ("AT2G40750", "WRKY54"),
        ("AT3G01080", "WRKY58"),
        ("AT1G02920", "GSTF7"),
        ("AT2G29470", "GSTU3"),
        ("AT2G41480", "PER25"),
        ("AT4G11290", "PER39"),
        ("AT1G68850", "PER11"),
        ("AT4G02520", "GSTF2"),
    ]
    key_gene_ids = [k[0] for k in key_gene_defs]
    gene_label_map = {k[0]: f"{k[1]} ({k[0]})" for k in key_gene_defs}
    sub_genes = degs[degs["gene_id"].isin(key_gene_ids)].copy()
    
    # Export phyllobiome genes table
    out_table = os.path.join(DATA_DIR, "ns26_phyllobiome_defense_genes.csv")
    sub_genes.to_csv(out_table, index=False)
    sub_genes.to_csv(os.path.join(DOCS_DATA_DIR, "ns26_phyllobiome_defense_genes.csv"), index=False)
    print(f"Extracted {len(sub_genes)} key host phyllobiome-responsive defense genes -> {out_table}")

    # Core historical spaceflight seedling microbiome taxa (from NASA OSDR / Barker et al.)
    microbiome_taxa = pd.DataFrame([
        {"Taxon": "Ralstonia pickettii", "Class": "Betaproteobacteria", "Role": "Endophyte / Biofilm former", "OSD_Prevalence": 5, "Niche": "Seed / Rhizosphere"},
        {"Taxon": "Pseudomonas fluorescens", "Class": "Gammaproteobacteria", "Role": "PGPB / Phyllosphere colonizer", "OSD_Prevalence": 4, "Niche": "Phyllosphere / Foliar"},
        {"Taxon": "Herbaspirillum huttiense", "Class": "Betaproteobacteria", "Role": "Nitrogen-fixing endophyte", "OSD_Prevalence": 4, "Niche": "Vascular / Apoplast"},
        {"Taxon": "Curvibacter gracilis", "Class": "Betaproteobacteria", "Role": "Aquatic / Epiphytic commensal", "OSD_Prevalence": 4, "Niche": "Leaf surface"},
        {"Taxon": "Cutibacterium acnes", "Class": "Actinobacteria", "Role": "Habitat / Hardware associate", "OSD_Prevalence": 5, "Niche": "Hardware / Foliar"},
        {"Taxon": "Acidovorax temperans", "Class": "Betaproteobacteria", "Role": "Motile biofilm endophyte", "OSD_Prevalence": 3, "Niche": "Seedling tissue"},
        {"Taxon": "Agrobacterium tumefaciens", "Class": "Alphaproteobacteria", "Role": "Wound-responsive colonizer", "OSD_Prevalence": 3, "Niche": "Rhizosphere / Wounds"},
        {"Taxon": "Bradyrhizobium viridifuturi", "Class": "Alphaproteobacteria", "Role": "Root / nodule-like endophyte", "OSD_Prevalence": 2, "Niche": "Root endosphere"},
        {"Taxon": "Cloacibacterium caeni", "Class": "Flavobacteriia", "Role": "Commensal biofilm bacterium", "OSD_Prevalence": 3, "Niche": "Moisture film"}
    ])

    print("=== Step 2: Plotting Multi-Panel Figure 6 ===")
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    fig = plt.figure(figsize=(15.5, 12.5), dpi=300)
    gs = gridspec.GridSpec(2, 2, height_ratios=[1.1, 1.0], hspace=0.35, wspace=0.35)

    # -------------------------------------------------------------
    # Panel A: PhysioSpace Biotic & Biotic.Hormone Trajectories
    # -------------------------------------------------------------
    ax_a = fig.add_subplot(gs[0, 0])
    phases = ["EE (~2.5m)", "CS (~4m)", "RE (~7.5m)", "LN (~10m)"]
    leaf_cols = ["EE Leaf", "CS Leaf", "RE Leaf", "LN Leaf"]
    root_cols = ["EE Root", "CS Root", "RE Root", "LN Root"]

    leaf_biotic = df_scores.loc["Biotic", leaf_cols].values
    leaf_bio_hormone = df_scores.loc["Biotic.Hormone", leaf_cols].values
    root_biotic = df_scores.loc["Biotic", root_cols].values
    root_bio_hormone = df_scores.loc["Biotic.Hormone", root_cols].values

    ax_a.axhline(0, color="#888888", linestyle="--", linewidth=1.2, alpha=0.7)
    ax_a.plot(phases, leaf_biotic, marker="o", linewidth=2.5, markersize=8, color="#1b5e20", label="Leaf: Biotic Pathogen Axis")
    ax_a.plot(phases, leaf_bio_hormone, marker="s", linewidth=2.5, markersize=8, color="#2e7d32", linestyle="-.", label="Leaf: Biotic.Hormone Axis (SA/JA)")
    ax_a.plot(phases, root_biotic, marker="^", linewidth=2.5, markersize=8, color="#8d6e63", label="Root: Biotic Pathogen Axis")
    ax_a.plot(phases, root_bio_hormone, marker="d", linewidth=2.5, markersize=8, color="#d84315", linestyle="-.", label="Root: Biotic.Hormone Axis (SA/JA)")

    # Highlight the CS divergence
    ax_a.axvspan(0.7, 1.3, color="#fff3e0", alpha=0.6, zorder=0)
    ax_a.text(1.0, 0.65, "CS: Microgravity Onset\nLeaf Immune Surge (+0.49***)\nvs Root Defense Suppression (-0.27*)",
              ha="center", fontsize=8.5, fontweight="bold", color="#e65100",
              bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffffff", edgecolor="#ffb74d", alpha=0.9))

    ax_a.set_ylabel("PhysioScore (Suppression [-1.0] <-> Induction [+1.0])", fontsize=10, fontweight="bold")
    ax_a.set_title("A: Host Immune & Biotic Hormone Dynamics Across Flight Phases", fontsize=11, fontweight="bold", pad=12)
    ax_a.legend(loc="lower left", fontsize=8.5, framealpha=0.9)
    ax_a.grid(True, linestyle=":", alpha=0.6)
    ax_a.set_ylim(-0.85, 0.85)

    # -------------------------------------------------------------
    # Panel B: Heatmap of Key Host Defense & Antimicrobial Genes
    # -------------------------------------------------------------
    ax_b = fig.add_subplot(gs[0, 1])
    gene_plot_cols = ["l2fc_ee_leaf", "l2fc_cs_leaf", "l2fc_re_leaf", "l2fc_ln_leaf", "l2fc_cs_root", "l2fc_re_root"]
    col_labels = ["EE Leaf", "CS Leaf", "RE Leaf", "LN Leaf", "CS Root", "RE Root"]

    sub_mat = sub_genes.set_index("gene_id")[gene_plot_cols].fillna(0.0)
    ylabels = [gene_label_map.get(gid, gid) for gid in sub_mat.index]

    cmap_b = sns.diverging_palette(240, 10, as_cmap=True)
    sns.heatmap(
        sub_mat,
        cmap=cmap_b,
        center=0.0,
        vmin=-4.0,
        vmax=4.0,
        annot=True,
        fmt=".1f",
        annot_kws={"size": 7.5, "weight": "bold"},
        xticklabels=col_labels,
        yticklabels=ylabels,
        linewidths=0.5,
        linecolor="#f0f0f0",
        cbar_kws={"label": "log2(Fold Change vs Ground)", "shrink": 0.85},
        ax=ax_b
    )
    ax_b.set_title("B: Host Phyllobiome Defense Genes Across Flight Phases", fontsize=11, fontweight="bold", pad=12)
    ax_b.set_ylabel("Host Defense / Cell-Wall Locus", fontsize=10, fontweight="bold")
    ax_b.tick_params(axis="x", rotation=30)

    # -------------------------------------------------------------
    # Panel C: Metatranscriptomic Unmapped-Read Mining Architecture (Flowchart)
    # -------------------------------------------------------------
    ax_c = fig.add_subplot(gs[1, 0])
    ax_c.set_xlim(0, 10)
    ax_c.set_ylim(0, 10)
    ax_c.axis("off")

    steps = [
        {"y": 8.6, "title": "1. Suborbital Plant Total RNA-Seq (KFTs)", "desc": "Sequential fixation at EE (~2.5m), CS (~4m), RE (~7.5m), LN (~10m)", "color": "#e8f5e9", "edge": "#4caf50"},
        {"y": 6.6, "title": "2. Host Decontamination (STAR / Araport11)", "desc": "85–95% reads map to Arabidopsis nuclear genome; 5–15% unmapped", "color": "#e3f2fd", "edge": "#2196f3"},
        {"y": 4.6, "title": "3. Metatranscriptome Assembly & Taxonomic Classification", "desc": "Kraken2/Bracken against RefSeq; unmapped non-host microbial contigs", "color": "#fff3e0", "edge": "#ff9800"},
        {"y": 2.6, "title": "4. Differential Phyllobiome Quantification", "desc": "Relative abundance & functional pathways (Pseudomonas, Ralstonia, etc.)", "color": "#f3e5f5", "edge": "#9c27b0"},
        {"y": 0.6, "title": "5. Host-Phyllobiome Holobiont Integration", "desc": "Cross-correlation of microbial shifts with host PR1, Defensins & WRKYs", "color": "#ffebee", "edge": "#f44336"}
    ]

    for s in steps:
        bbox_props = dict(boxstyle="round,pad=0.5", facecolor=s["color"], edgecolor=s["edge"], linewidth=1.5)
        ax_c.text(5.0, s["y"], f"{s['title']}\n{s['desc']}", ha="center", va="center",
                  fontsize=8.5, fontweight="bold", bbox=bbox_props)

    # Add connecting arrows
    for y_start in [7.7, 5.7, 3.7, 1.7]:
        ax_c.annotate("", xy=(5.0, y_start - 0.3), xytext=(5.0, y_start + 0.1),
                      arrowprops=dict(arrowstyle="->", color="#37474f", lw=2.0))

    ax_c.set_title("C: Metatranscriptomic Discovery Pipeline for Unmapped Reads", fontsize=11, fontweight="bold", pad=12)

    # -------------------------------------------------------------
    # Panel D: Historical NASA OSDR Seedling Core Microbiome
    # -------------------------------------------------------------
    ax_d = fig.add_subplot(gs[1, 1])
    y_pos = np.arange(len(microbiome_taxa))
    colors_d = ["#2b5c8f" if "Foliar" in n or "Leaf" in n or "Phyllosphere" in n else "#8f5c2b" for n in microbiome_taxa["Niche"]]

    bars = ax_d.barh(y_pos, microbiome_taxa["OSD_Prevalence"], color=colors_d, height=0.65, edgecolor="#333333", alpha=0.85)
    ax_d.set_yticks(y_pos)
    ax_d.set_yticklabels(microbiome_taxa["Taxon"], fontsize=9, fontstyle="italic")
    ax_d.invert_yaxis()
    ax_d.set_xlabel("Prevalence Across NASA OSDR Plant Seedling Studies (N=5)", fontsize=10, fontweight="bold")
    ax_d.set_title("D: Core Plant Endophyte & Phyllosphere Taxa in Spaceflight", fontsize=11, fontweight="bold", pad=12)
    ax_d.set_xlim(0, 5.6)
    ax_d.grid(True, axis="x", linestyle=":", alpha=0.6)

    # Bar value labels
    for bar in bars:
        w = bar.get_width()
        ax_d.text(w + 0.12, bar.get_y() + bar.get_height()/2, f"{int(w)} studies", va="center", fontsize=8.2, fontweight="bold")

    # Legend for niches
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#2b5c8f", label="Phyllosphere / Foliar / Surface"),
        Patch(facecolor="#8f5c2b", label="Endosphere / Rhizosphere / Seed")
    ]
    ax_d.legend(handles=legend_elements, loc="lower right", fontsize=8.5, framealpha=0.9)

    plt.suptitle("Figure 6: Phyllobiome Immune Surveillance & Host-Microbe Dynamics Across Suborbital Flight Phases",
                 fontsize=13, fontweight="bold", y=0.98)

    # Save to figures and docs/assets/figures
    out_png = os.path.join(FIG_DIR, "fig6_phyllobiome_dynamics.png")
    out_pdf = os.path.join(FIG_DIR, "fig6_phyllobiome_dynamics.pdf")
    docs_png = os.path.join(DOCS_FIG_DIR, "fig6_phyllobiome_dynamics.png")

    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    fig.savefig(docs_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved Figure 6: {out_png}")
    print(f"Saved Figure 6 (PDF): {out_pdf}")
    print(f"Saved Figure 6 (Docs asset): {docs_png}")

if __name__ == "__main__":
    main()
