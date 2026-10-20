#!/usr/bin/env python3
"""scripts/07_plot_physiospace_heatmap.py
Generates Figure 5: Diverging Heatmap of PhysioSpace Stress Pattern Activation
across Blue Origin NS-26 Suborbital Flight Phases.

Color palette: Strictly diverging (low) Blue -> White -> Red (high), centered at 0.0.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data", "processed")
FIG_DIR = os.path.join(ROOT_DIR, "figures")
DOCS_FIG_DIR = os.path.join(ROOT_DIR, "docs", "assets", "figures")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(DOCS_FIG_DIR, exist_ok=True)

def main():
    print("=== Step 1: Loading PhysioScore & P-value Matrices ===")
    scores_file = os.path.join(DATA_DIR, "ns26_physiospace_scores.csv")
    pvals_file = os.path.join(DATA_DIR, "ns26_physiospace_pvalues.csv")

    df_scores = pd.read_csv(scores_file, index_col=0)
    df_pvals = pd.read_csv(pvals_file, index_col=0)

    # Order of columns to present: Leaves chronologically, Roots chronologically, Unity 22 benchmark
    cols = [
        "EE Leaf", "CS Leaf", "RE Leaf", "LN Leaf",
        "EE Root", "CS Root", "RE Root", "LN Root",
        "Unity 22"
    ]
    df_scores = df_scores[cols]
    df_pvals = df_pvals[cols]

    # Order stress axes by biological theme
    axis_order = [
        "Heat", "Hypoxia", "Drought", "Osmotic", "Salt", "Cold", "Drought.Light",
        "Wounding", "Genotoxic", "Radiation", "UV", "Herbicide", "LowPH",
        "Biotic", "Biotic.Hormone", "Hormone",
        "Light", "FarRed", "Nitrogen", "FeDeficiency"
    ]
    existing_axes = [a for a in axis_order if a in df_scores.index]
    df_scores = df_scores.loc[existing_axes]
    df_pvals = df_pvals.loc[existing_axes]

    # Prepare formatted annotation strings with significance stars
    annot_matrix = np.empty(df_scores.shape, dtype=object)
    for i in range(df_scores.shape[0]):
        for j in range(df_scores.shape[1]):
            val = df_scores.iloc[i, j]
            pval = df_pvals.iloc[i, j]
            star = ""
            if pval < 0.001:
                star = "***"
            elif pval < 0.01:
                star = "**"
            elif pval < 0.05:
                star = "*"
            
            # Format value
            if abs(val) < 0.005:
                annot_matrix[i, j] = f"0.00{star}"
            else:
                annot_matrix[i, j] = f"{val:+.2f}{star}"

    print("=== Step 2: Rendering Publication Heatmap ===")
    # Custom Diverging Colormap: (low) Deep Blue -> Ice Blue -> White -> Coral -> Crimson Red (high)
    colors = ["#08519c", "#3182bd", "#6baed6", "#bdd7e7", "#ffffff", "#fcae91", "#fb6a4a", "#de2d26", "#a50f15"]
    cmap = mcolors.LinearSegmentedColormap.from_list("blue_white_red", colors, N=256)

    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    fig, ax = plt.subplots(figsize=(11.5, 12.5), dpi=300)

    # Plot heatmap centered strictly at 0.0
    sns.heatmap(
        df_scores,
        cmap=cmap,
        vmin=-0.85,
        vmax=0.85,
        center=0.0,
        annot=annot_matrix,
        fmt="",
        annot_kws={"size": 9.5, "weight": "bold"},
        linewidths=1.0,
        linecolor="#e0e0e0",
        cbar_kws={
            "label": "PhysioScore (Normalized Concordance: Suppressed [-1.0] <-> Induced [+1.0])",
            "shrink": 0.75,
            "pad": 0.04
        },
        ax=ax
    )

    # Vertical separators between Leaf, Root, and Unity 22
    ax.axvline(4, color="#2c3e50", linewidth=2.5)
    ax.axvline(8, color="#2c3e50", linewidth=2.5)

    # Add section header labels at the top
    ax.text(2.0, -0.85, "LEAVES (Blue Origin NS-26)", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#1b5e20",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#e8f5e9", edgecolor="#81c784", alpha=0.9))

    ax.text(6.0, -0.85, "ROOTS (Blue Origin NS-26)", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#8d6e63",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#efebe9", edgecolor="#bcaaa4", alpha=0.9))

    ax.text(8.5, -0.85, "COMPARATIVE", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#0d47a1",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#e3f2fd", edgecolor="#90caf9", alpha=0.9))

    # Subtitles for phases
    phase_labels = [
        "EE\nAscent (~2.5m)", "CS\nMicro-g (~4m)", "RE\nCoast (~7.5m)", "LN\nTouchdown (~10m)",
        "EE\nAscent (~2.5m)", "CS\nMicro-g (~4m)", "RE\nCoast (~7.5m)", "LN\nTouchdown (~10m)",
        "Virgin Galactic\nUnity 22"
    ]
    ax.set_xticklabels(phase_labels, fontsize=10, fontweight="bold", rotation=0)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=11, fontweight="medium", rotation=0)

    ax.set_title(
        "Figure 5: PhysioSpace Stress Pattern Autodecoding across the Suborbital Flight Profile\n"
        "Dynamic activation of 20 canonical Arabidopsis stress programs (* p<0.05, ** p<0.01, *** p<0.001)",
        fontsize=13,
        fontweight="bold",
        pad=42
    )

    # Note at bottom
    fig.text(
        0.5, 0.01,
        "Color scale: (Low) Deep Blue = Suppressed Program <-> White = Baseline <-> (High) Crimson Red = Induced Program.\n"
        "Projections performed against canonical AT_Stress_Space (20 axes x 22,729 genes; Hadizadeh Esfahani et al. 2021).",
        ha="center", fontsize=9.5, fontstyle="italic", color="#424242"
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])

    # Save to figures and docs/assets/figures
    out_png = os.path.join(FIG_DIR, "fig5_physiospace_stress_heatmap.png")
    out_pdf = os.path.join(FIG_DIR, "fig5_physiospace_stress_heatmap.pdf")
    docs_png = os.path.join(DOCS_FIG_DIR, "fig5_physiospace_stress_heatmap.png")

    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    fig.savefig(docs_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved figure: {out_png}")
    print(f"Saved figure: {out_pdf}")
    print(f"Saved docs asset: {docs_png}")

if __name__ == "__main__":
    main()
