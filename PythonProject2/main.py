"""
Top 5 European Leagues Player Performance Analysis (2025-2026 Season)
=======================================================================

Analyzes player statistics across the Premier League, La Liga, Serie A,
Bundesliga, and Ligue 1 to answer a series of structured questions about
scoring output, efficiency, discipline, and squad performance.

Data source: FBref-derived player stats, 2025-2026 season (2,839 players).

Author: Muhammad Sowe
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_fig(fig, filename):
    """Save a figure to the outputs directory and close it."""
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


def scaled_barh(ax, labels, values, color, value_fmt="{:.1f}"):
    """
    Custom helper that draws a horizontal bar chart and dynamically pads
    the x-axis so close-value comparisons remain readable, then labels
    each bar with its exact value.
    """
    bars = ax.barh(labels, values, color=color)
    max_val = max(values)
    min_val = min(values)
    padding = (max_val - min_val) * 0.15 if max_val != min_val else max_val * 0.1
    ax.set_xlim(0, max_val + padding)
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_width() + padding * 0.05,
            bar.get_y() + bar.get_height() / 2,
            value_fmt.format(val),
            va="center",
            fontsize=9,
        )
    ax.invert_yaxis()
    return ax


# ----------------------------------------------------------------------
# Load & clean data
# ----------------------------------------------------------------------
df = pd.read_csv("data/players_data_light-2025_2026.csv")

# Keep only outfield players with a meaningful sample size (avoid small-
# sample-size distortions, e.g. a player with 1 shot and 1 goal showing a
# 100% conversion rate).
MIN_90S = 5
outfield = df[(df["Pos"] != "GK") & (df["90s"] >= MIN_90S)].copy()
keepers = df[(df["Pos"] == "GK") & (df["90s"] >= MIN_90S)].copy()

# Clean league names (strip country-code prefix, e.g. "es La Liga" -> "La Liga")
outfield["League"] = outfield["Comp"].str.split(" ", n=1).str[1]
keepers["League"] = keepers["Comp"].str.split(" ", n=1).str[1]
df["League"] = df["Comp"].str.split(" ", n=1).str[1]

# Simplify position into primary position group
outfield["PosGroup"] = outfield["Pos"].str.split(",").str[0]

# Per-90 goal contribution metric
outfield["G+A_per90"] = outfield["G+A"] / outfield["90s"]

print(f"Total players: {len(df)}")
print(f"Outfield players (min {MIN_90S} 90s played): {len(outfield)}")
print(f"Goalkeepers (min {MIN_90S} 90s played): {len(keepers)}")


# ========================================================================
# Question 1: Who are the top 10 goal contributors (Goals + Assists) this
# season, and how does that break down between goals and assists?
# ========================================================================
top_contributors = outfield.nlargest(10, "G+A")[["Player", "Squad", "Gls", "Ast", "G+A"]]
print("\n--- Q1: Top 10 Goal Contributors ---")
print(top_contributors.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 6))
y = np.arange(len(top_contributors))
ax.barh(y, top_contributors["Gls"], color="#2E86AB", label="Goals")
ax.barh(
    y,
    top_contributors["Ast"],
    left=top_contributors["Gls"],
    color="#F18F01",
    label="Assists",
)
ax.set_yticks(y)
ax.set_yticklabels(
    top_contributors["Player"] + " (" + top_contributors["Squad"] + ")"
)
ax.invert_yaxis()
ax.set_xlabel("Goals + Assists")
ax.set_title("Top 10 Goal Contributors — 2025-2026 Season")
ax.legend()
save_fig(fig, "01_top_goal_contributors.png")


# ========================================================================
# Question 2: Which position group is most efficient at converting shots
# into goals?
# ========================================================================
pos_efficiency = (
    outfield[outfield["Sh"] > 0]
    .groupby("PosGroup")
    .agg(total_goals=("Gls", "sum"), total_shots=("Sh", "sum"))
)
pos_efficiency["Conversion_%"] = (
    pos_efficiency["total_goals"] / pos_efficiency["total_shots"] * 100
).round(2)
pos_efficiency = pos_efficiency.sort_values("Conversion_%", ascending=False)
print("\n--- Q2: Shot Conversion Rate by Position ---")
print(pos_efficiency)

fig, ax = plt.subplots(figsize=(8, 5))
scaled_barh(
    ax,
    pos_efficiency.index.tolist(),
    pos_efficiency["Conversion_%"].tolist(),
    color="#A23B72",
    value_fmt="{:.1f}%",
)
ax.set_xlabel("Shot Conversion Rate (%)")
ax.set_title("Shot-to-Goal Conversion Rate by Position")
save_fig(fig, "02_conversion_by_position.png")


# ========================================================================
# Question 3: Does a higher volume of minutes played correlate with more
# goal contributions per 90, or do "impact substitutes" outperform on a
# per-90 basis?
# ========================================================================
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(
    data=outfield,
    x="Min",
    y="G+A_per90",
    hue="PosGroup",
    alpha=0.6,
    ax=ax,
    palette="Set2",
)
ax.set_xlabel("Total Minutes Played")
ax.set_ylabel("Goal Contributions per 90 Minutes")
ax.set_title("Minutes Played vs. Goal Contribution Rate")
save_fig(fig, "03_minutes_vs_contribution_rate.png")

corr_min_ga90 = outfield["Min"].corr(outfield["G+A_per90"])
print(f"\n--- Q3: Correlation between Minutes Played and G+A per 90: {corr_min_ga90:.3f} ---")


# ========================================================================
# Question 4: Which club has the most combined goal output across the top
# 5 leagues?
# ========================================================================
club_goals = (
    outfield.groupby("Squad")["Gls"].sum().sort_values(ascending=False).head(10)
)
print("\n--- Q4: Top 10 Clubs by Total League Goals ---")
print(club_goals)

fig, ax = plt.subplots(figsize=(9, 6))
scaled_barh(ax, club_goals.index.tolist(), club_goals.values.tolist(), color="#3B7A57", value_fmt="{:.0f}")
ax.set_xlabel("Total Goals")
ax.set_title("Top 10 Clubs by Total Goals Scored (Top 5 Leagues)")
save_fig(fig, "04_top_clubs_by_goals.png")


# ========================================================================
# Question 5: At what age do players tend to peak in goal contribution
# output?
# ========================================================================
age_perf = (
    outfield.groupby("Age")["G+A_per90"]
    .mean()
    .reset_index()
    .query("Age >= 17 and Age <= 38")
)
print("\n--- Q5: Average Goal Contribution per 90 by Age ---")
print(age_perf.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(age_perf["Age"], age_perf["G+A_per90"], marker="o", color="#C73E1D")
ax.set_xlabel("Age")
ax.set_ylabel("Avg. Goal Contributions per 90")
ax.set_title("Average Goal Contribution Rate by Age")
ax.grid(True, alpha=0.3)
save_fig(fig, "05_age_vs_performance.png")


# ========================================================================
# Question 6: How does shooting accuracy (SoT%) differ across the 5
# leagues?
# ========================================================================
league_accuracy = outfield.groupby("League")["SoT%"].mean().sort_values(ascending=False)
print("\n--- Q6: Average Shot-on-Target % by League ---")
print(league_accuracy)

fig, ax = plt.subplots(figsize=(8, 5))
scaled_barh(
    ax,
    league_accuracy.index.tolist(),
    league_accuracy.values.tolist(),
    color="#1B998B",
    value_fmt="{:.1f}%",
)
ax.set_xlabel("Average Shot-on-Target Percentage")
ax.set_title("Shooting Accuracy by League")
save_fig(fig, "06_accuracy_by_league.png")


# ========================================================================
# Question 7: Which league is the most disciplined (fewest cards per 90)?
# ========================================================================
outfield["Cards_per90"] = (outfield["CrdY"] + outfield["CrdR"] * 2) / outfield["90s"]
league_discipline = (
    outfield.groupby("League")["Cards_per90"].mean().sort_values()
)
print("\n--- Q7: Average Card Points per 90 by League (Yellow=1, Red=2) ---")
print(league_discipline)

fig, ax = plt.subplots(figsize=(8, 5))
scaled_barh(
    ax,
    league_discipline.index.tolist(),
    league_discipline.values.tolist(),
    color="#F4A261",
    value_fmt="{:.2f}",
)
ax.set_xlabel("Avg. Card Points per 90 (Yellow=1, Red=2)")
ax.set_title("League Discipline Comparison")
save_fig(fig, "07_discipline_by_league.png")


# ========================================================================
# Question 8: Who are the top 10 goalkeepers by save percentage (min. 5
# full matches played)?
# ========================================================================
top_keepers = keepers.nlargest(10, "Save%")[["Player", "Squad", "Save%", "CS%", "GA90"]]
print("\n--- Q8: Top 10 Goalkeepers by Save % ---")
print(top_keepers.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 6))
scaled_barh(
    ax,
    (top_keepers["Player"] + " (" + top_keepers["Squad"] + ")").tolist(),
    top_keepers["Save%"].tolist(),
    color="#5B5F97",
    value_fmt="{:.1f}%",
)
ax.set_xlabel("Save Percentage")
ax.set_title("Top 10 Goalkeepers by Save % — 2025-2026 Season")
save_fig(fig, "08_top_goalkeepers.png")


# ========================================================================
# Question 9: Do teams with more defensive actions (tackles + interceptions)
# concede fewer goals? (Proxy analysis using squad-level aggregates)
# ========================================================================
squad_defense = outfield.groupby("Squad").agg(
    total_def_actions=("TklW", "sum"),
)
squad_def_int = outfield.groupby("Squad")["Int"].sum()
squad_defense["total_def_actions"] += squad_def_int

squad_keeper_ga = keepers.groupby("Squad")["GA"].sum()
squad_combined = squad_defense.join(squad_keeper_ga, how="inner").dropna()

fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(
    data=squad_combined,
    x="total_def_actions",
    y="GA",
    ax=ax,
    scatter_kws={"alpha": 0.6, "color": "#264653"},
    line_kws={"color": "#E76F51"},
)
ax.set_xlabel("Total Squad Defensive Actions (Tackles Won + Interceptions)")
ax.set_ylabel("Goals Against")
ax.set_title("Defensive Actions vs. Goals Conceded (by Squad)")
save_fig(fig, "09_defense_vs_goals_conceded.png")

corr_def_ga = squad_combined["total_def_actions"].corr(squad_combined["GA"])
print(f"\n--- Q9: Correlation between squad defensive actions and goals conceded: {corr_def_ga:.3f} ---")


# ========================================================================
# Question 10: Which players create the most chances for others relative
# to their own shot volume — i.e., who are the top "creators" (high
# assists relative to shots taken)?
# ========================================================================
creators = outfield[outfield["Sh"] >= 10].copy()
creators["Ast_per_Sh"] = creators["Ast"] / creators["Sh"]
top_creators = creators.nlargest(10, "Ast_per_Sh")[["Player", "Squad", "Ast", "Sh", "Ast_per_Sh"]]
print("\n--- Q10: Top 10 Creators (Assists per Shot Taken, min. 10 shots) ---")
print(top_creators.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 6))
scaled_barh(
    ax,
    (top_creators["Player"] + " (" + top_creators["Squad"] + ")").tolist(),
    top_creators["Ast_per_Sh"].tolist(),
    color="#6A4C93",
    value_fmt="{:.2f}",
)
ax.set_xlabel("Assists per Shot Taken")
ax.set_title("Top 10 Creators — Assists Relative to Own Shot Volume")
save_fig(fig, "10_top_creators.png")


print("\nAll analysis complete. Charts saved to the 'outputs/' directory.")