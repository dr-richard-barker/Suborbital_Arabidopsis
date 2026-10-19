#!/usr/bin/env python3
"""
scripts/05_network_hubs.py
Performs transcription factor (TF) and chaperone network hub identification,
extracts key regulatory families (bHLH, HSF, BAG, WRKY, NAC, MYB, PMEI),
generates Figure 4, and builds a standalone interactive 3D Plotly visualization
(docs/assets/interactive_3d_clusters.html) mirroring Strickland et al. (2025).
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.manifold import TSNE
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
FIG_DIR = BASE_DIR / "figures"
DOCS_ASSETS = BASE_DIR / "docs" / "assets"
DOCS_FIG_DIR = DOCS_ASSETS / "figures"

# Official CoSE Brand Palette
COSE_NAVY = "#2F5985"
COSE_BLUE = "#3B6EA5"
COSE_TEAL = "#3FB6A8"
COSE_MINT = "#54C9BA"
COSE_CORAL = "#D55E00"
COSE_CARD = "#F7F7F8"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 11,
    "axes.edgecolor": "#CCCCCC",
    "axes.linewidth": 1.0,
    "figure.autolayout": True,
    "savefig.dpi": 300
})

TF_FAMILIES = {
    'HSF': ['HSF', 'HEAT SHOCK FACTOR'],
    'sHSP/Chaperone': ['HSP', 'HEAT SHOCK PROTEIN', 'CHAPERONE', 'DNAJ'],
    'bHLH': ['BHLH', 'BASIC HELIX-LOOP-HELIX'],
    'BAG Chaperone': ['BAG'],
    'WRKY': ['WRKY'],
    'MYB': ['MYB'],
    'NAC': ['NAC'],
    'ERF/AP2': ['ERF', 'AP2'],
    'PMEI/Cell Wall': ['PMEI', 'PECTIN METHYLESTERASE'],
    'GST/Redox': ['GLUTATHIONE S-TRANSFERASE', 'GST'],
    'Auxin/IAA': ['AUXIN', 'IAA', 'SAUR']
}

def annotate_families(df):
    def get_family(row):
        text = f"{row['gene_symbol']} {row['gene_description']}".upper()
        for fam, keywords in TF_FAMILIES.items():
            if any(kw in text for kw in keywords):
                return fam
        return 'Other'
    
    df['functional_family'] = df.apply(get_family, axis=1)
    return df

def generate_hub_analysis():
    df = pd.read_csv(PROCESSED_DIR / "ns26_degs_trajectories.csv")
    df = annotate_families(df)
    
    fam_counts = df[df['functional_family'] != 'Other']['functional_family'].value_counts()
    print("Top Functional Regulatory Families:")
    print(fam_counts)
    
    # Figure 4: Regulatory Families Breakdown & Phase Dynamics
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
    
    # Left: Family Counts
    fam_counts_sorted = fam_counts.sort_values(ascending=True)
    colors = [COSE_CORAL if 'HSF' in f or 'sHSP' in f or 'BAG' in f else COSE_TEAL for f in fam_counts_sorted.index]
    bars = ax1.barh(fam_counts_sorted.index, fam_counts_sorted.values, color=colors, height=0.65)
    ax1.set_title("Key Regulatory Families in NS-26", fontsize=12, fontweight='bold', color=COSE_NAVY)
    ax1.set_xlabel("Number of Genes", fontsize=10)
    ax1.grid(axis='x', linestyle='--', alpha=0.5)
    for b in bars:
        w = b.get_width()
        ax1.text(w + 0.8, b.get_y() + b.get_height()/2, f"{int(w)}", va='center', fontsize=9.5, fontweight='bold')
    ax1.set_xlim(0, max(fam_counts_sorted.values) + 8)
    
    # Right: Expression dynamics of HSF / sHSP / bHLH / GST across flight phases (Leaves)
    fams_to_plot = ['sHSP/Chaperone', 'HSF', 'bHLH', 'GST/Redox']
    phases = ['EE', 'CS', 'RE', 'LN']
    cols = ['l2fc_ee_leaf', 'l2fc_cs_leaf', 'l2fc_re_leaf', 'l2fc_ln_leaf']
    
    palette = [COSE_CORAL, COSE_NAVY, COSE_TEAL, COSE_BLUE]
    for fam, color in zip(fams_to_plot, palette):
        sub = df[df['functional_family'] == fam]
        means = sub[cols].fillna(0.0).mean().values
        ax2.plot(phases, means, marker='o', linewidth=2.5, label=f"{fam} (n={len(sub)})", color=color)
        
    ax2.axhline(0, color='#888888', linestyle=':', linewidth=0.8)
    ax2.set_title("Leaf Mean Trajectory by Regulatory Family", fontsize=12, fontweight='bold', color=COSE_NAVY)
    ax2.set_ylabel("Mean log2(Fold Change) vs Ground", fontsize=10)
    ax2.set_xlabel("Suborbital Flight Phase", fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(frameon=True, facecolor=COSE_CARD, fontsize=9.5)
    
    fig.suptitle("Transcriptional Regulation & Chaperone Dynamics in Human-Tended Suborbital Spaceflight",
                 fontsize=13, fontweight='bold', color=COSE_NAVY, y=0.99)
                 
    for p in [FIG_DIR / "fig4_hub_transcription_factors.png", DOCS_FIG_DIR / "fig4_hub_transcription_factors.png"]:
        fig.savefig(p, bbox_inches='tight')
    plt.close(fig)
    print("Saved Figure 4.")
    
    # Build 3D t-SNE projection with random initialization
    feature_cols = [
        'l2fc_ee_leaf', 'l2fc_cs_leaf', 'l2fc_re_leaf', 'l2fc_ln_leaf',
        'l2fc_ee_root', 'l2fc_cs_root', 'l2fc_re_root', 'l2fc_ln_root'
    ]
    mat = df[feature_cols].fillna(0.0).values
    
    print("Computing 3D t-SNE manifold (init='random', perplexity=30)...")
    tsne = TSNE(n_components=3, perplexity=30, init='random', random_state=42, max_iter=1000)
    embedding = tsne.fit_transform(mat)
    
    df['tsne_x'] = embedding[:, 0]
    df['tsne_y'] = embedding[:, 1]
    df['tsne_z'] = embedding[:, 2]
    
    # Save fully annotated dataset with 3D coordinates
    df.to_csv(PROCESSED_DIR / "ns26_degs_trajectories.csv", index=False)
    print("Saved updated dataset with 3D coordinates -> ns26_degs_trajectories.csv")
    
    # Create interactive 3D scatter using Plotly
    color_map = {
        'Microgravity_Coast_Responsive': COSE_TEAL,
        'Transient_Boost_Shock': COSE_CORAL,
        'Landing_Touchdown_Shock': COSE_NAVY,
        'Sustained_Transition': COSE_BLUE,
        'Root_Dominant': '#E76F51',
        'Progressive_Adaptive': '#8E9AAF'
    }
    
    fig3d = px.scatter_3d(
        df,
        x='tsne_x', y='tsne_y', z='tsne_z',
        color='leaf_trajectory_archetype',
        color_discrete_map=color_map,
        hover_name='gene_id',
        hover_data={
            'gene_symbol': True,
            'functional_family': True,
            'l2fc_re_leaf': ':.2f',
            'l2fc_cs_leaf': ':.2f',
            'vg_unity22_deg': True,
            'orbital_deg': True,
            'tsne_x': False, 'tsne_y': False, 'tsne_z': False
        },
        title="3D Manifold of NS-26 Arabidopsis Suborbital Transcriptome (t-SNE & DBSCAN Archetypes)",
        labels={'leaf_trajectory_archetype': 'Dynamic Archetype'}
    )
    
    fig3d.update_traces(marker=dict(size=4, opacity=0.85))
    fig3d.update_layout(
        template="plotly_white",
        scene=dict(
            xaxis=dict(title="t-SNE 1", showbackground=False),
            yaxis=dict(title="t-SNE 2", showbackground=False),
            zaxis=dict(title="t-SNE 3", showbackground=False)
        ),
        font=dict(family="sans-serif", color=COSE_NAVY),
        legend=dict(
            yanchor="top", y=0.9, xanchor="left", x=0.05,
            bgcolor="rgba(247, 247, 248, 0.9)"
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    html_out = DOCS_ASSETS / "interactive_3d_clusters.html"
    fig3d.write_html(str(html_out), include_plotlyjs="cdn")
    print(f"Saved interactive 3D WebGL viewer -> {html_out}")

if __name__ == "__main__":
    generate_hub_analysis()
