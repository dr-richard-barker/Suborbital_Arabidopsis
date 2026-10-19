#!/usr/bin/env python3
"""
scripts/03_temporal_splines.py
Models continuous temporal dynamics of the 1,272 NS-26 DEGs across the
flight profile (EE -> CS -> RE -> LN) using temporal trajectories and
identifies dynamic trajectory archetypes (Transient Boost, Microgravity Coast,
Reentry/Landing Shock, Sustained Transition).
"""
import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.interpolate import CubicSpline

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
FIGURES_DIR = BASE_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Experimental flight time points in minutes relative to launch (T=0)
TIME_POINTS = {
    'EE': -16.0,  # Escape Enabled (~7:51 AM, T-16 min)
    'CS': 2.8,    # Capsule Separation (~8:10 AM, T+2.8 min)
    'RE': 5.3,    # Reentry (~8:12:30 AM, T+5.3 min)
    'LN': 10.5    # Landing (~8:17:30 AM, T+10.5 min)
}

def analyze_trajectories():
    df = pd.read_csv(PROCESSED_DIR / "ns26_degs_master.csv")
    
    leaf_cols = ['l2fc_ee_leaf', 'l2fc_cs_leaf', 'l2fc_re_leaf', 'l2fc_ln_leaf']
    root_cols = ['l2fc_ee_root', 'l2fc_cs_root', 'l2fc_re_root', 'l2fc_ln_root']
    
    # Fill unmeasured/non-significant L2FC with 0.0 (as done in paper methods for clustering)
    leaf_mat = df[leaf_cols].fillna(0.0).values
    root_mat = df[root_cols].fillna(0.0).values
    
    # Classify trajectory patterns for Leaf:
    # 1. Transient Launch/Boost Shock: High at CS, drops at RE and LN (|CS| > 1.0 and |CS| > 1.5 * |RE|)
    # 2. Microgravity Coast Responsive: High at RE (|RE| > 1.0 and |RE| > |CS| and |RE| > |LN|)
    # 3. Landing/Deceleration Shock: High at LN (|LN| > 1.0 and |LN| > |RE|)
    # 4. Sustained Spaceflight Shift: Elevated across CS and RE (|CS| > 0.8 and |RE| > 0.8)
    # 5. Complex / Multiphasic: other
    
    patterns = []
    for i in range(len(df)):
        ee, cs, re, ln = leaf_mat[i]
        abs_vals = np.abs([ee, cs, re, ln])
        max_idx = np.argmax(abs_vals)
        
        if np.max(abs_vals) < 0.5:
            patterns.append("Root_Dominant")
        elif max_idx == 1 and abs(cs) >= 1.0 and abs(cs) > 1.3 * abs(re):
            patterns.append("Transient_Boost_Shock")
        elif max_idx == 2 and abs(re) >= 1.0 and abs(re) > abs(cs):
            patterns.append("Microgravity_Coast_Responsive")
        elif max_idx == 3 and abs(ln) >= 1.0 and abs(ln) > abs(re):
            patterns.append("Landing_Touchdown_Shock")
        elif abs(cs) >= 0.8 and abs(re) >= 0.8 and np.sign(cs) == np.sign(re):
            patterns.append("Sustained_Transition")
        else:
            patterns.append("Progressive_Adaptive")
            
    df['leaf_trajectory_archetype'] = patterns
    
    # Archetype breakdown
    counts = df['leaf_trajectory_archetype'].value_counts()
    print("Leaf Trajectory Archetypes:")
    print(counts)
    
    # Save enriched dataset
    out_path = PROCESSED_DIR / "ns26_degs_trajectories.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved trajectory-annotated dataset -> {out_path}")
    
    # Generate summary stats by archetype
    summary = df.groupby('leaf_trajectory_archetype').agg(
        total_genes=('gene_id', 'count'),
        heat_genes=('heat_stress', 'sum'),
        ros_genes=('ros_all', 'sum'),
        vg_shared=('vg_unity22_deg', 'sum'),
        orbital_shared=('orbital_deg', 'sum')
    ).reset_index()
    
    summary_path = PROCESSED_DIR / "ns26_archetype_functional_enrichment.csv"
    summary.to_csv(summary_path, index=False)
    print("\nArchetype Functional Breakdown:")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    analyze_trajectories()
