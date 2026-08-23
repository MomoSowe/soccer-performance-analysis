# Top 5 European Leagues Player Performance Analysis (2025-2026)

A data analysis project exploring player performance across Europe's top 5 leagues — the Premier League, La Liga, Serie A, Bundesliga, and Ligue 1 — using the 2025-2026 season dataset (2,839 players).

## Overview

This project answers 10 self-directed analytical questions about scoring output, shooting efficiency, squad performance, age curves, league discipline, and goalkeeping, using pandas for data processing and matplotlib/seaborn for visualization.

## Tools & Technologies

- **Python**
- **Pandas** — data cleaning, filtering, and groupby aggregations
- **NumPy** — numerical operations
- **Matplotlib** — chart rendering
- **Seaborn** — statistical visualization, regression plots, and heatmaps

## Questions Answered

1. Who are the top 10 goal contributors (Goals + Assists) this season, broken down by goals vs. assists?
2. Which position group converts shots into goals most efficiently?
3. Does more playing time correlate with a higher goal-contribution rate per 90 minutes?
4. Which club has the highest combined goal output across the top 5 leagues?
5. At what age do players tend to peak in goal contribution output?
6. How does shooting accuracy (shots on target %) differ across the 5 leagues?
7. Which league is the most disciplined, by cards per 90 minutes?
8. Who are the top 10 goalkeepers by save percentage?
9. Do squads with more combined defensive actions (tackles won + interceptions) concede fewer goals?
10. Which numeric performance metrics are most strongly correlated with one another? (Full correlation heatmap across 21 metrics)

## Methodology Notes

- Analysis is restricted to players with at least 5 full-match equivalents (90s) played, to avoid small-sample distortions (e.g., a player with 1 shot and 1 goal showing a 100% conversion rate).
- A custom `scaled_barh()` helper function dynamically pads chart axes based on the value range, keeping close-value bar comparisons readable rather than compressed against a fixed-scale axis.
- All 10 charts are automatically exported to the `outputs/` folder when the script runs.

## Project Structure

```
soccer-performance-analysis/
├── data/
│   ├── players_data_light-2025_2026.csv
│   └── players_data-2025_2026.csv
├── outputs/
│   ├── 01_top_goal_contributors.png
│   ├── 02_conversion_by_position.png
│   ├── 03_minutes_vs_contribution_rate.png
│   ├── 04_top_clubs_by_goals.png
│   ├── 05_age_vs_performance.png
│   ├── 06_accuracy_by_league.png
│   ├── 07_discipline_by_league.png
│   ├── 08_top_goalkeepers.png
│   ├── 09_defense_vs_goals_conceded.png
│   └── 10_correlation_heatmap.png
├── analysis.py
├── requirements.txt
└── README.md
```

## How to Run

```bash
pip install -r requirements.txt
python analysis.py
```

All charts and printed findings are generated automatically and saved to `outputs/`.

## Key Findings

- **Harry Kane (Bayern Munich)** led all players in combined goal contributions (41 G+A), followed closely by **Erling Haaland** (35) and **Michael Olise** (34).
- **Forwards convert shots into goals at nearly double the rate of defenders** (14.7% vs. 7.6%), confirming expected positional scoring efficiency.
- **Minutes played showed virtually no correlation with per-90 goal contribution rate** (r = -0.01), suggesting that high-output players perform consistently whether used as starters or in shorter stints — output per 90 is largely independent of total workload.
- **Bayern Munich led all clubs in total goals scored** (119), well ahead of Barcelona (94) and Inter (85).
- **Bundesliga players posted the highest shot accuracy** (32.6% shots on target), while **La Liga was the least disciplined league** by cards per 90.
- Squad-level defensive actions (tackles + interceptions) showed a **moderate positive correlation with goals conceded** (r = 0.26) — likely reflecting that teams under more defensive pressure generate more tackles/interceptions simply by facing more attacking play, rather than defensive activity causing goals against.

## Data Source

Player statistics dataset for the 2025-2026 season, Top 5 European Leagues (sourced via Kaggle, originally FBref-derived data).

## Author

Muhammad Sowe — Information Systems student at UMBC, seeking Data Analyst / SQL Developer opportunities.
[GitHub](https://github.com/MomoSowe) | sowem2765@gmail.com
