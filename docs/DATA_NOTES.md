# Data source and reproducibility notes

All six data files were supplied from the user's historical IPL group assignment. The newly supplied group presentation cites the Kaggle dataset `ramjidoolla/ipl-data-set`, but the exact file versions and redistribution license have **not** been independently verified. **Before uploading them to a public GitHub repository, check your right to redistribute them**; if this cannot be confirmed, publish the code, README, and figures only, remove `data/*` from the repository, and explain how to obtain the dataset through an authorized source.

- `deliveries.csv`: ball-level historical match events (179,078 rows; 21 columns). There is **no Season** column; without `matches.csv` do not infer yearly trends from match IDs.
- `Players.xlsx`: 566 player records (5 columns). Missing DOB/country fields exist; DOB is not necessary for the reproducible charts.
- `Player_Consistency_Stats.csv`: 516 derived batting metric rows. The script filters to players with at least 10 matches when plotting average runs vs. strike rate.
- `Players_with_clusters.csv`: 516 players, including 34 rows without a valid cluster label; group labels were created in the original project.
- `teamwise_home_and_away.csv`: 14 team rows; percentages were supplied, not reconstructed from original match records.
- `teams.csv`: 1-column reference team list.

## Missing original inputs

The original group code references `matches.csv` and `most_runs_average_strikerate.csv`, but those files were not among the uploads. They are not fabricated in this package. The new `src/ipl_analysis.py` is deliberately designed to run without either file.

## Accuracy and reuse

The included model scripts in `archive/` are historical coursework artifacts. They contain static user-specific filesystem paths, do not represent a maintained package, and may contain modeling limitations. Do not describe their numeric predictions as validated future IPL outcomes.
