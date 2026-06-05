"""
Generates static PNG charts + a data.json payload for the interactive site.
Re-run this whenever superheroes_dataset.csv changes:  python3 make_charts.py
"""
import json, pathlib
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).parent
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)

NAVY, TEAL, GOLD, GREY = "#1c487b", "#2bb3a3", "#d9a521", "#9aa5b1"
plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": .25,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "white", "axes.facecolor": "white"})

raw = pd.read_csv(HERE / "superheroes_dataset.csv")
bad = (raw.number_of_superhero_friends < 0) | (raw.injury_heal_time_days < 0) \
    | (raw.average_hours_of_superhero_power_used_per_day > 24)
raw["valid"] = ~bad
clean = raw[raw.valid].copy()
clean["gold"] = clean.outfit_color_code == "gold"

# ---------- CHART 1: Simpson's paradox scatter ----------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
main = clean[~clean.gold]; gold = clean[clean.gold]
ax.scatter(main.number_of_superhero_friends, main.injury_heal_time_days,
           c=TEAL, s=42, alpha=.75, edgecolor="white", linewidth=.6, label="Regular heroes (n=%d)" % len(main))
ax.scatter(gold.number_of_superhero_friends, gold.injury_heal_time_days,
           c=GOLD, s=70, alpha=.95, edgecolor=NAVY, linewidth=1, label="Gold subgroup (n=%d)" % len(gold))
# trend within regular heroes
z = np.polyfit(main.number_of_superhero_friends, main.injury_heal_time_days, 1)
xs = np.linspace(main.number_of_superhero_friends.min(), main.number_of_superhero_friends.max(), 50)
ax.plot(xs, np.polyval(z, xs), color=NAVY, lw=2, ls="--", label="Trend (regular): more friends → faster heal")
ax.set_xlabel("Number of superhero friends  (popularity →)")
ax.set_ylabel("Injury heal time (days)  (↓ = better)")
ax.set_title("The trap: one subgroup reverses the story", color=NAVY, weight="bold")
ax.legend(fontsize=8.5, frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig(CHARTS / "scatter_simpsons.png", dpi=150); plt.close(fig)

# ---------- CHART 2: median heal time, popular vs nonpopular, all vs no-gold ----------
def split(d):
    m = d.number_of_superhero_friends.median()
    g = np.where(d.number_of_superhero_friends > m, "Popular", "Nonpopular")
    return d.assign(grp=g)
allh = split(clean); nog = split(clean[~clean.gold])
def med(d, grp): return d.loc[d.grp == grp, "injury_heal_time_days"].median()
labels = ["Popular", "Nonpopular"]
fig, ax = plt.subplots(figsize=(7.2, 4.2))
x = np.arange(2); w = .36
b1 = ax.bar(x - w/2, [med(allh, "Popular"), med(allh, "Nonpopular")], w, color=GREY, label="All heroes (raw)")
b2 = ax.bar(x + w/2, [med(nog, "Popular"), med(nog, "Nonpopular")], w, color=TEAL, label="Gold subgroup removed")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("Median heal time (days)  (↓ = better)")
ax.set_title("Remove the confound → the effect flips", color=NAVY, weight="bold")
ax.legend(fontsize=9, frameon=False)
for b in list(b1)+list(b2):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+.5, f"{b.get_height():.0f}", ha="center", fontsize=9)
fig.tight_layout(); fig.savefig(CHARTS / "bars_reversal.png", dpi=150); plt.close(fig)

# ---------- CHART 3: data-quality flags ----------
fig, ax = plt.subplots(figsize=(7.2, 3.6))
issues = {"Negative heal time": int((raw.injury_heal_time_days < 0).sum()),
          "Negative friends": int((raw.number_of_superhero_friends < 0).sum()),
          "Power > 24 h/day": int((raw.average_hours_of_superhero_power_used_per_day > 24).sum()),
          "Missing power value": int(raw.average_hours_of_superhero_power_used_per_day.isna().sum())}
ax.barh(list(issues.keys()), list(issues.values()), color=["#d9534f","#d9534f","#d9534f",GOLD])
for i, v in enumerate(issues.values()): ax.text(v+.03, i, str(v), va="center", fontsize=10)
ax.set_xlabel("rows affected"); ax.set_title("Data-quality red flags found in the raw file", color=NAVY, weight="bold")
ax.invert_yaxis(); fig.tight_layout(); fig.savefig(CHARTS / "data_quality.png", dpi=150); plt.close(fig)

# ---------- data.json for interactive charts ----------
payload = {
    "rows": raw[["hero_id","number_of_superhero_friends","injury_heal_time_days",
                 "recovery_quality_score","outfit_color_code",
                 "average_hours_of_superhero_power_used_per_day","valid"]]
            .where(pd.notna(raw), None).to_dict(orient="records"),
    "median_friends_clean": float(clean.number_of_superhero_friends.median()),
}
(HERE / "data.json").write_text(json.dumps(payload))
print(f"Wrote 3 charts + data.json ({len(payload['rows'])} rows, {int(raw.valid.sum())} valid)")
