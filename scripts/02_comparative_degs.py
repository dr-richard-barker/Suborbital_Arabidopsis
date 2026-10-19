#!/usr/bin/env python3
"""
scripts/02_comparative_degs.py
Processes MOESM1 and MOESM2 to generate harmonized, tidy DEG tables,
cross-mission comparisons (NS-26 vs VG Unity 22 vs Orbital APEX),
and functional category statistics.
"""
import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

MOESM1_PATH = RAW_DIR / "41526_2026_645_MOESM1_ESM.xlsx"
MOESM2_PATH = RAW_DIR / "41526_2026_645_MOESM2_ESM.xlsx"

def process_degs():
    print("Loading MOESM1 Full Heatmap...")
    df = pd.read_excel(MOESM1_PATH, sheet_name="Full Heatmap", skiprows=1)
    
    # Standardize column names
    col_map = {
        'Gene_ID': 'gene_id',
        'Gene_symbol': 'gene_symbol',
        'Gene_def': 'gene_description',
        'EE Leaf': 'l2fc_ee_leaf',
        'CS Leaf': 'l2fc_cs_leaf',
        'RE Leaf': 'l2fc_re_leaf',
        'LN Leaf': 'l2fc_ln_leaf',
        'EE Root': 'l2fc_ee_root',
        'CS Root': 'l2fc_cs_root',
        'RE Root': 'l2fc_re_root',
        'LN Root': 'l2fc_ln_root',
        'VG ': 'vg_unity22_deg',
        'Orbital': 'orbital_deg',
        'Heat': 'heat_stress',
        'ROS ALL': 'ros_all',
        'RC I': 'rc_1',
        'RC II': 'rc_2',
        'RC III': 'rc_3',
        'RC IV': 'rc_4',
        'RC V': 'rc_5',
        'RC VI': 'rc_6',
        'RC VII': 'rc_7',
        'RC VIII': 'rc_8',
        'Cell Wall': 'cell_wall',
        'Housekeeping': 'housekeeping',
        'Flowering': 'flowering',
        '1-Cos C': 'cluster_id'
    }
    
    # Keep and rename present columns
    keep_cols = [c for c in col_map.keys() if c in df.columns]
    clean_df = df[keep_cols].rename(columns=col_map).copy()
    
    # Clean string columns
    clean_df['gene_id'] = clean_df['gene_id'].astype(str).str.strip().str.upper()
    clean_df['gene_symbol'] = clean_df['gene_symbol'].astype(str).str.strip().replace({'nan': '', '': ''})
    clean_df['gene_description'] = clean_df['gene_description'].astype(str).str.strip().replace({'nan': ''})
    
    # Convert flags to boolean
    flag_cols = ['vg_unity22_deg', 'orbital_deg', 'heat_stress', 'ros_all',
                 'rc_1', 'rc_2', 'rc_3', 'rc_4', 'rc_5', 'rc_6', 'rc_7', 'rc_8',
                 'cell_wall', 'housekeeping', 'flowering']
    for fc in flag_cols:
        if fc in clean_df.columns:
            clean_df[fc] = clean_df[fc].notna() & (clean_df[fc].astype(str).str.strip() != '') & (clean_df[fc] != 0)
    
    # Save master tidy matrix
    out_master = PROCESSED_DIR / "ns26_degs_master.csv"
    clean_df.to_csv(out_master, index=False)
    print(f"Saved master DEG table ({len(clean_df)} genes) -> {out_master}")
    
    # Generate phase counts breakdown
    phase_cols = [
        ('EE Leaf', 'l2fc_ee_leaf', 'Leaf', 'EE'),
        ('CS Leaf', 'l2fc_cs_leaf', 'Leaf', 'CS'),
        ('RE Leaf', 'l2fc_re_leaf', 'Leaf', 'RE'),
        ('LN Leaf', 'l2fc_ln_leaf', 'Leaf', 'LN'),
        ('EE Root', 'l2fc_ee_root', 'Root', 'EE'),
        ('CS Root', 'l2fc_cs_root', 'Root', 'CS'),
        ('RE Root', 'l2fc_re_root', 'Root', 'RE'),
        ('LN Root', 'l2fc_ln_root', 'Root', 'LN'),
    ]
    
    summary_rows = []
    for label, col, organ, phase in phase_cols:
        series = clean_df[col].dropna()
        n_up = (series > 0).sum()
        n_down = (series < 0).sum()
        n_total = len(series)
        summary_rows.append({
            'condition': label,
            'organ': organ,
            'phase': phase,
            'total_degs': n_total,
            'upregulated': n_up,
            'downregulated': n_down
        })
    
    sum_df = pd.DataFrame(summary_rows)
    out_sum = PROCESSED_DIR / "ns26_phase_summary.csv"
    sum_df.to_csv(out_sum, index=False)
    print("Phase Summary:")
    print(sum_df.to_string(index=False))
    
    # Cross-mission overlap stats
    overlap_stats = {
        "Total_NS26_DEGs": len(clean_df),
        "Shared_with_VG_Unity22": int(clean_df['vg_unity22_deg'].sum()),
        "Shared_with_Orbital_APEX": int(clean_df['orbital_deg'].sum()),
        "Heat_Stress_Associated": int(clean_df['heat_stress'].sum()),
        "ROS_All_Associated": int(clean_df['ros_all'].sum()),
        "ROS_Core_III": int(clean_df['rc_3'].sum()),
        "ROS_Core_IV": int(clean_df['rc_4'].sum()),
        "Cell_Wall_Associated": int(clean_df['cell_wall'].sum()),
        "Housekeeping_Negative_Control": int(clean_df['housekeeping'].sum()),
        "Flowering_Negative_Control": int(clean_df['flowering'].sum()),
    }
    
    overlap_df = pd.DataFrame(list(overlap_stats.items()), columns=['Category', 'Gene_Count'])
    overlap_df['Percentage_of_NS26'] = (overlap_df['Gene_Count'] / len(clean_df) * 100).round(2)
    out_overlap = PROCESSED_DIR / "ns26_functional_categories.csv"
    overlap_df.to_csv(out_overlap, index=False)
    print("\nFunctional Overlap:")
    print(overlap_df.to_string(index=False))

if __name__ == "__main__":
    process_degs()
