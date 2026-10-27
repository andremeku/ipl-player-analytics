"""Reproducible IPL visual analysis based only on datasets supplied with this repo.

Usage (from repository root):
    python src/ipl_analysis.py
    python src/ipl_analysis.py --data-dir data --output-dir figures

This module is a cleaned portfolio adaptation of a historical group project.
It does NOT claim to forecast future IPL player outcomes.
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BG = "#FAFCFF"
INK = "#17263C"
BLUE = "#2263C7"
TEAL = "#009A9A"
ORANGE = "#EA884D"


def load_data(data_dir: Path) -> dict[str, pd.DataFrame]:
    required = {
        "deliveries": "deliveries.csv",
        "players": "Players.xlsx",
        "clusters": "Players_with_clusters.csv",
        "consistency": "Player_Consistency_Stats.csv",
        "home_away": "teamwise_home_and_away.csv",
    }
    absent = [filename for filename in required.values() if not (data_dir / filename).is_file()]
    if absent:
        raise FileNotFoundError("Missing input file(s) in " + str(data_dir) + ": " + ", ".join(absent))
    loaded = {}
    for key, filename in required.items():
        if filename.endswith(".xlsx"):
            loaded[key] = pd.read_excel(data_dir / filename)
        else:
            loaded[key] = pd.read_csv(data_dir / filename)
    return loaded


def chart_style():
    sns.set_theme(style="whitegrid", font_scale=1.05)
    plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG,
                         "axes.labelcolor": INK, "text.color": INK,
                         "axes.titleweight": "bold", "savefig.facecolor": BG})


def finish(path: Path):
    plt.tight_layout(pad=1.8)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def create_figures(d: dict[str, pd.DataFrame], out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    chart_style()
    deliveries=d["deliveries"].copy()
    deliveries["batsman_runs"] = pd.to_numeric(deliveries["batsman_runs"], errors="coerce").fillna(0)

    top = deliveries.groupby("batsman", observed=True)["batsman_runs"].sum().nlargest(10).sort_values()
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    bars=ax.barh(top.index,top.values,color=BLUE)
    ax.bar_label(bars,padding=5,fontsize=9,fmt="%d")
    ax.set_xlim(0,top.max()*1.17)
    ax.set_xlabel("Batter runs in supplied delivery records")
    ax.set_title("Highest run totals · Provided IPL dataset",loc="left",pad=16,fontsize=17)
    ax.grid(axis="x",alpha=.18);ax.grid(axis="y",visible=False)
    finish(out/'top_batters.png')

    players=d["players"]
    country=players["Country"].fillna("Not recorded").value_counts().head(10).sort_values()
    fig,ax=plt.subplots(figsize=(9.7,5.5))
    bars=ax.barh(country.index,country.values,color=TEAL)
    ax.bar_label(bars,padding=4,fontsize=9)
    ax.set_xlim(0,country.max()*1.16)
    ax.set_title("Player nationality distribution",loc="left",pad=16,fontsize=17)
    ax.set_xlabel("Players in supplied Players.xlsx")
    ax.grid(axis="x",alpha=.18);ax.grid(axis="y",visible=False)
    finish(out/'player_nationalities.png')

    con=d['consistency'].copy()
    for c in ['total_runs','average_runs','strike_rate','total_matches']:
        con[c]=pd.to_numeric(con[c],errors='coerce')
    con=con.loc[con['total_matches']>=10].dropna(subset=['average_runs','strike_rate','total_runs'])
    fig,ax=plt.subplots(figsize=(9.6,5.6))
    sizes=(con['total_runs'].clip(upper=6000).fillna(0)/30).clip(lower=15)
    ax.scatter(con['strike_rate'],con['average_runs'],s=sizes,alpha=.46,c=BLUE,edgecolors='none')
    ax.set_xlabel('Batting strike rate (source summary)')
    ax.set_ylabel('Average runs per match (source summary)')
    ax.set_title('Batting output vs. strike rate',loc='left',pad=16,fontsize=17)
    ax.text(.99,.03,'Players with ≥10 recorded matches · bubble size ≈ total runs',
            transform=ax.transAxes,ha='right',va='bottom',fontsize=9,color='#5E7186')
    ax.grid(alpha=.16)
    finish(out/'runs_vs_strike_rate.png')

    ha=d['home_away'].copy()
    for c in ['home_win_percentage','away_win_percentage','home_matches','away_matches']:
        ha[c]=pd.to_numeric(ha[c],errors='coerce')
    ha=ha.sort_values('home_win_percentage',ascending=True).tail(12)
    fig,ax=plt.subplots(figsize=(10.3,6))
    import numpy as np
    y=np.arange(len(ha)); h=.37
    ax.barh(y-h/2,ha['home_win_percentage'],height=h,color=BLUE,label='Home')
    ax.barh(y+h/2,ha['away_win_percentage'],height=h,color=ORANGE,label='Away')
    ax.set_yticks(y,ha['team'],fontsize=9)
    ax.set_xlim(0,100);ax.set_xlabel('Win percentage (%)')
    ax.set_title('Home vs. away team win rates',loc='left',pad=16,fontsize=17)
    ax.legend(loc='lower right',frameon=False)
    ax.grid(axis='x',alpha=.16);ax.grid(axis='y',visible=False)
    finish(out/'home_away_performance.png')

    clustered=d['clusters'].copy()
    clustered=clustered.dropna(subset=['cluster','total_runs','strikerate']).copy()
    clustered['cluster']=clustered['cluster'].astype(int)
    fig,ax=plt.subplots(figsize=(9.6,5.6))
    sc=ax.scatter(clustered['strikerate'],clustered['total_runs'],c=clustered['cluster'],cmap='viridis',
                  alpha=.64,s=37,edgecolors='none')
    ax.set_xlabel('Strike rate (source metrics)');ax.set_ylabel('Total runs (source metrics)')
    ax.set_title('Historical K-means player groups',loc='left',pad=16,fontsize=17)
    cbar=fig.colorbar(sc,ax=ax,pad=.03,ticks=sorted(clustered['cluster'].unique()))
    cbar.set_label('Original cluster label')
    ax.grid(alpha=.16)
    finish(out/'player_clusters.png')

    metrics={
        'ball_by_ball_records':int(len(deliveries)),
        'unique_matches':int(deliveries['match_id'].nunique()),
        'unique_batters':int(deliveries['batsman'].nunique()),
        'player_demographic_rows':int(len(players)),
        'players_in_consistency_summary':int(len(d['consistency'])),
        'players_with_cluster_label':int(clustered.shape[0]),
        'teams_in_home_away_summary':int(len(d['home_away'])),
        'leading_batter':str(top.index[-1]),
        'leading_batter_runs':int(top.iloc[-1]),
    }
    (out/'summary_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf-8')
    return metrics


def main():
    root=Path(__file__).resolve().parents[1]
    parser=argparse.ArgumentParser(description='Generate exploratory IPL figures from bundled files')
    parser.add_argument('--data-dir',type=Path,default=root/'data')
    parser.add_argument('--output-dir',type=Path,default=root/'figures')
    args=parser.parse_args()
    d=load_data(args.data_dir)
    summary=create_figures(d,args.output_dir)
    print('Saved five charts and summary_metrics.json to',args.output_dir)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
