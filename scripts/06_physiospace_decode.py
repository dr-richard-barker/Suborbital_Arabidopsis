#!/usr/bin/env python3
"""scripts/06_physiospace_decode.py
Applies the PhysioSpace stress autodecoder framework (Hadizadeh Esfahani et al. 2021)
to the Blue Origin NS-26 suborbital Arabidopsis spaceflight dataset (Ferl et al. 2026).

Projects temporal differential expression profiles across 8 flight phases
(Leaves and Roots: EE, CS, RE, LN) and the Virgin Galactic Unity 22 benchmark
onto the canonical 20-axis Arabidopsis reference stress space (AT_Stress_Space).
"""

import os
import numpy as np
import pandas as pd
from scipy import stats

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data", "processed")

def benjamini_hochberg(p_values):
    """Benjamini-Hochberg FDR correction."""
    p_values = np.asarray(p_values)
    n = len(p_values)
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    fdr = np.zeros(n)
    cummin = 1.0
    for i in range(n - 1, -1, -1):
        rank = i + 1
        val = (sorted_p[i] * n) / rank
        cummin = min(cummin, val)
        fdr[i] = cummin
    # restore original order
    rev_indices = np.argsort(sorted_indices)
    return np.clip(fdr[rev_indices], 0.0, 1.0)

def main():
    print("=== Step 1: Loading NS-26 Master DEGs & Crosswalk ===")
    degs_path = os.path.join(DATA_DIR, "ns26_degs_master.csv")
    cw_path = os.path.join(DATA_DIR, "tair_to_entrez.csv")
    space_path = os.path.join(DATA_DIR, "at_stress_space_matrix.csv")

    degs = pd.read_csv(degs_path)
    cw = pd.read_csv(cw_path)
    space = pd.read_csv(space_path, index_col=0)
    space.index = space.index.astype(str)

    cw["entrez_id"] = cw["entrez_id"].astype(str)
    cw["tair_id"] = cw["tair_id"].astype(str)

    # Merge NS-26 DEGs with Entrez crosswalk
    merged = degs.merge(cw, left_on="gene_id", right_on="tair_id")
    merged["entrez_id"] = merged["entrez_id"].astype(str)
    merged = merged[merged["entrez_id"].isin(space.index)].copy()

    print(f"Total DEGs: {len(degs)} | Mapped in AT_Stress_Space: {merged['gene_id'].nunique()} genes ({len(merged)} records)")

    # Define conditions to project
    conditions = [
        {"name": "EE Leaf", "col": "l2fc_ee_leaf", "organ": "Leaf", "phase": "EE", "type": "NS-26"},
        {"name": "CS Leaf", "col": "l2fc_cs_leaf", "organ": "Leaf", "phase": "CS", "type": "NS-26"},
        {"name": "RE Leaf", "col": "l2fc_re_leaf", "organ": "Leaf", "phase": "RE", "type": "NS-26"},
        {"name": "LN Leaf", "col": "l2fc_ln_leaf", "organ": "Leaf", "phase": "LN", "type": "NS-26"},
        {"name": "EE Root", "col": "l2fc_ee_root", "organ": "Root", "phase": "EE", "type": "NS-26"},
        {"name": "CS Root", "col": "l2fc_cs_root", "organ": "Root", "phase": "CS", "type": "NS-26"},
        {"name": "RE Root", "col": "l2fc_re_root", "organ": "Root", "phase": "RE", "type": "NS-26"},
        {"name": "LN Root", "col": "l2fc_ln_root", "organ": "Root", "phase": "LN", "type": "NS-26"},
        {"name": "Unity 22", "col": "vg_unity22_deg", "organ": "Comparative", "phase": "All", "type": "Virgin Galactic"}
    ]

    long_rows = []
    matrix_scores = {}
    matrix_pvals = {}

    print("\n=== Step 2: Running PhysioSpace Projections across 20 Stress Axes ===")
    for cond in conditions:
        cond_name = cond["name"]
        col = cond["col"]

        if col == "vg_unity22_deg":
            sub = merged[merged["vg_unity22_deg"] == True].copy()
            # In Unity 22, we have gene membership; rank by mean fold change across leaf/root active phases
            sub["score_val"] = sub[["l2fc_cs_leaf", "l2fc_re_leaf", "l2fc_cs_root", "l2fc_re_root"]].mean(axis=1).fillna(1.0)
            sub_grp = sub.groupby("entrez_id")["score_val"].mean()
        else:
            sub = merged.dropna(subset=[col]).copy()
            sub_grp = sub.groupby("entrez_id")[col].mean()

        pos_genes = [g for g in sub_grp[sub_grp > 0].index if g in space.index]
        neg_genes = [g for g in sub_grp[sub_grp < 0].index if g in space.index]
        n_pos = len(pos_genes)
        n_neg = len(neg_genes)

        print(f"Condition: {cond_name:12s} | Mapped Genes: {len(sub_grp):3d} (Up: {n_pos:3d}, Down: {n_neg:3d})")

        s_dict = {}
        p_dict = {}

        for axis in space.columns:
            if n_pos >= 2 and n_neg >= 2:
                u_stat, pval = stats.mannwhitneyu(
                    space.loc[pos_genes, axis],
                    space.loc[neg_genes, axis],
                    alternative="two-sided"
                )
                stat_norm = 2.0 * ((u_stat / (n_pos * n_neg)) - 0.5)
            elif len(sub_grp) >= 2:
                # Fallback one-sample t-test against reference baseline
                t_stat, pval = stats.ttest_1samp(space.loc[sub_grp.index, axis], 0.0)
                stat_norm = float(np.clip(t_stat / 4.0, -1.0, 1.0))
            else:
                # Single gene (e.g. EE Root)
                val = float(space.loc[sub_grp.index, axis].values[0]) if len(sub_grp) == 1 else 0.0
                stat_norm = float(np.clip(val, -1.0, 1.0))
                pval = 0.5

            s_dict[axis] = stat_norm
            p_dict[axis] = pval

            long_rows.append({
                "condition": cond_name,
                "organ": cond["organ"],
                "phase": cond["phase"],
                "type": cond["type"],
                "stress_axis": axis,
                "physioscore": stat_norm,
                "p_value": pval,
                "n_genes_up": n_pos,
                "n_genes_down": n_neg
            })

        matrix_scores[cond_name] = s_dict
        matrix_pvals[cond_name] = p_dict

    # Compute FDR within each condition
    df_long = pd.DataFrame(long_rows)
    all_fdrs = []
    for cond_name, grp in df_long.groupby("condition"):
        fdr_vals = benjamini_hochberg(grp["p_value"].values)
        all_fdrs.extend(list(zip(grp.index, fdr_vals)))
    
    fdr_series = pd.Series(dict(all_fdrs))
    df_long["fdr"] = fdr_series
    df_long["sig_symbol"] = df_long["p_value"].apply(
        lambda p: "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else ""))
    )

    # Build matrices
    df_scores = pd.DataFrame(matrix_scores)
    df_pvals = pd.DataFrame(matrix_pvals)

    print("\n=== Step 3: Saving Output Files ===")
    out_scores = os.path.join(DATA_DIR, "ns26_physiospace_scores.csv")
    out_pvals = os.path.join(DATA_DIR, "ns26_physiospace_pvalues.csv")
    out_long = os.path.join(DATA_DIR, "ns26_physiospace_long.csv")

    df_scores.to_csv(out_scores)
    df_pvals.to_csv(out_pvals)
    df_long.to_csv(out_long, index=False)

    print(f"Saved: {out_scores} ({df_scores.shape})")
    print(f"Saved: {out_pvals} ({df_pvals.shape})")
    print(f"Saved: {out_long} ({df_long.shape})")

    print("\n=== Summary of Decoded PhysioScores ===")
    print(df_scores.round(3))

if __name__ == "__main__":
    main()
