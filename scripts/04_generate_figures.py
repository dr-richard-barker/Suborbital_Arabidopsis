#!/usr/bin/env python3
"""
scripts/04_generate_figures.py
Generates publication-quality figures styled in the CoSE color palette
for the NS-26 suborbital Arabidopsis re-analysis, saved to figures/ and docs/assets/figures/.
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
FIG_DIR = BASE_DIR / "figures"
DOCS_FIG_DIR = BASE_DIR / "docs" / "assets" / "figures"

FIG_DIR.mkdir(parents=True, exist_ok=True)
DOCS_FIG_DIR.mkdir(parents=True, exist_ok=True)

# Official CoSE Brand Palette
COSE_NAVY = "#2F5985"
COSE_BLUE = "#3B6EA5"
COSE_TEAL = "#3FB6A8"
COSE_MINT = "#54C9BA"
COSE_CORAL = "#D55E00"
COSE_DARK = "#171A20"
COSE_CARD = "#F7F7F8"
COSE_MUTED = "#5A5A5A"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 11,
    "axes.edgecolor": "#CCCCCC",
    "axes.linewidth": 1.0,
    "figure.autolayout": True,
    "savefig.dpi": 300
})

def plot_fig1_phase_degs():
    df = pd.read_csv(PROCESSED_DIR / "ns26_phase_summary.csv")
    
    phases = ['EE', 'CS', 'RE', 'LN']
    leaf_up = [df[(df['organ']=='Leaf') & (df['phase']==p)]['upregulated'].values[0] for p in phases]
    leaf_down = [df[(df['organ']=='Leaf') & (df['phase']==p)]['downregulated'].values[0] for p in phases]
    root_up = [df[(df['organ']=='Root') & (df['phase']==p)]['upregulated'].values[0] for p in phases]
    root_down = [df[(df['organ']=='Root') & (df['phase']==p)]['downregulated'].values[0] for p in phases]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
    
    x = np.arange(len(phases))
    width = 0.38
    
    # Leaves
    ax1.bar(x - width/2, leaf_up, width, label='Upregulated', color=COSE_TEAL, edgecolor='none')
    ax1.bar(x + width/2, leaf_down, width, label='Downregulated', color=COSE_CORAL, edgecolor='none')
    ax1.set_xticks(x)
    ax1.set_xticklabels(['EE\n(Pre-launch)', 'CS\n(Post-boost)', 'RE\n(Microgravity)', 'LN\n(Touchdown)'])
    ax1.set_title("Leaf Transcriptome Response", fontsize=13, fontweight='bold', color=COSE_NAVY)
    ax1.set_ylabel("Differentially Expressed Genes (Count)", fontsize=11)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(frameon=True, facecolor=COSE_CARD, edgecolor='none')
    
    # Annotate totals
    for i, p in enumerate(phases):
        tot = leaf_up[i] + leaf_down[i]
        ax1.text(i, max(leaf_up[i], leaf_down[i]) + 20, f"Total: {tot}", ha='center', fontsize=9, fontweight='bold')
    
    # Roots
    ax2.bar(x - width/2, root_up, width, label='Upregulated', color=COSE_TEAL, edgecolor='none')
    ax2.bar(x + width/2, root_down, width, label='Downregulated', color=COSE_CORAL, edgecolor='none')
    ax2.set_xticks(x)
    ax2.set_xticklabels(['EE\n(Pre-launch)', 'CS\n(Post-boost)', 'RE\n(Microgravity)', 'LN\n(Touchdown)'])
    ax2.set_title("Root Transcriptome Response", fontsize=13, fontweight='bold', color=COSE_NAVY)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    for i, p in enumerate(phases):
        tot = root_up[i] + root_down[i]
        ax2.text(i, max(root_up[i], root_down[i]) + 20, f"Total: {tot}", ha='center', fontsize=9, fontweight='bold')
        
    fig.suptitle("NS-26 Suborbital Spaceflight: Organ-Specific Phasic Transcriptome Response", 
                 fontsize=14, fontweight='bold', color=COSE_NAVY, y=1.03)
    
    for path in [FIG_DIR / "fig1_phase_degs.png", DOCS_FIG_DIR / "fig1_phase_degs.png"]:
        fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print("Saved Figure 1.")

def plot_fig2_trajectories():
    df = pd.read_csv(PROCESSED_DIR / "ns26_degs_trajectories.csv")
    archetypes = [
        ("Microgravity_Coast_Responsive", "Microgravity Coast Peak (RE)", COSE_TEAL),
        ("Transient_Boost_Shock", "Transient Boost Shock (CS)", COSE_CORAL),
        ("Landing_Touchdown_Shock", "Landing Shock (LN)", COSE_NAVY),
        ("Sustained_Transition", "Sustained Microgravity Shift", COSE_BLUE)
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(11, 8.5), sharex=True, sharey=True)
    axes = axes.flatten()
    
    time_points = [-16.0, 2.8, 5.3, 10.5]
    time_labels = ['EE\n(T-16m)', 'CS\n(T+2.8m)', 'RE\n(T+5.3m)', 'LN\n(T+10.5m)']
    
    for idx, (arch_key, arch_title, color) in enumerate(archetypes):
        ax = axes[idx]
        sub = df[df['leaf_trajectory_archetype'] == arch_key]
        n_genes = len(sub)
        
        # Plot individual trajectories as transparent lines
        leaf_mat = sub[['l2fc_ee_leaf', 'l2fc_cs_leaf', 'l2fc_re_leaf', 'l2fc_ln_leaf']].fillna(0.0).values
        for row in leaf_mat[:100]:  # sample up to 100 for visual clarity
            ax.plot(time_points, row, color=color, alpha=0.08, linewidth=1)
            
        # Mean trajectory
        mean_traj = np.mean(leaf_mat, axis=0)
        ax.plot(time_points, mean_traj, color=color, linewidth=3.5, label='Mean Trajectory')
        
        # Shaded microgravity period (T+2.5 to T+5.5 min)
        ax.axvspan(2.8, 5.3, color='#EBF5FB', alpha=0.5, label='Microgravity Coast')
        ax.axhline(0, color='#888888', linestyle=':', linewidth=0.8)
        
        ax.set_title(f"{arch_title} (n = {n_genes})", fontsize=12, fontweight='bold', color=COSE_NAVY)
        ax.set_ylabel("Expression log2(Fold Change)", fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.4)
        if idx == 0:
            ax.legend(loc='upper left', frameon=True, facecolor=COSE_CARD, fontsize=9)
            
    for ax in axes[2:]:
        ax.set_xticks(time_points)
        ax.set_xticklabels(time_labels)
        ax.set_xlabel("Flight Phase Timeline (Minutes relative to launch)", fontsize=10)
        
    fig.suptitle("Temporal Trajectory Archetypes of Arabidopsis Response to Suborbital Spaceflight", 
                 fontsize=14, fontweight='bold', color=COSE_NAVY, y=0.99)
    
    for path in [FIG_DIR / "fig2_temporal_archetypes.png", DOCS_FIG_DIR / "fig2_temporal_archetypes.png"]:
        fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print("Saved Figure 2.")

def plot_fig3_functional_breakdown():
    df = pd.read_csv(PROCESSED_DIR / "ns26_functional_categories.csv")
    df = df[df['Category'] != 'Total_NS26_DEGs'].copy()
    
    # Clean label strings
    label_map = {
        'Shared_with_VG_Unity22': 'Virgin Galactic Unity 22 Suborbital',
        'Shared_with_Orbital_APEX': 'Orbital Spaceflight (APEX)',
        'Heat_Stress_Associated': 'Heat Stress / Chaperones',
        'ROS_All_Associated': 'Reactive Oxygen Species (All)',
        'ROS_Core_III': 'ROS Core III (Peroxisomal/Light)',
        'ROS_Core_IV': 'ROS Core IV (Mitochondrial)',
        'Cell_Wall_Associated': 'Cell Wall Biosynthesis',
        'Housekeeping_Negative_Control': 'Housekeeping (Control)',
        'Flowering_Negative_Control': 'Flowering (Control)'
    }
    df['Label'] = df['Category'].map(label_map).fillna(df['Category'])
    df = df.sort_values(by='Gene_Count', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    colors = [COSE_CORAL if 'Control' in l else COSE_BLUE if 'Suborbital' in l or 'Orbital' in l else COSE_TEAL for l in df['Label']]
    bars = ax.barh(df['Label'], df['Gene_Count'], color=colors, edgecolor='none', height=0.65)
    
    ax.set_xlabel("Number of NS-26 DEGs Belonging to Category", fontsize=11)
    ax.set_title("Cross-Mission and Functional Category Enrichment in Blue Origin NS-26", 
                 fontsize=13, fontweight='bold', color=COSE_NAVY)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    for bar in bars:
        w = bar.get_width()
        pct = (w / 1272) * 100
        ax.text(w + 5, bar.get_y() + bar.get_height()/2, f"{int(w)} ({pct:.1f}%)", 
                va='center', fontsize=9.5, fontweight='bold', color='#333333')
        
    ax.set_xlim(0, 360)
    
    for path in [FIG_DIR / "fig3_functional_enrichment.png", DOCS_FIG_DIR / "fig3_functional_enrichment.png"]:
        fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print("Saved Figure 3.")

if __name__ == "__main__":
    plot_fig1_phase_degs()
    plot_fig2_trajectories()
    plot_fig3_functional_breakdown()
