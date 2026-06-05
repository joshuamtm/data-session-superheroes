"""
Generates static PNG charts (FORENSIC DARK theme) + data.json for the site.
Re-run whenever superheroes_dataset.csv changes:  python3 make_charts.py
"""
import json, pathlib
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

HERE = pathlib.Path(__file__).parent
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)

# ---- forensic palette ----
INK="#15120D"; PANEL="#1f1b14"; CREAM="#ECE4D2"; MUT="#9A8F77"
TEAL="#6FB7AE"; GOLD="#E0A53B"; RED="#E5472D"; LINE="#3a3328"
plt.rcParams.update({
    "font.size": 11, "font.family": "monospace",
    "text.color": CREAM, "axes.labelcolor": CREAM, "axes.edgecolor": LINE,
    "xtick.color": MUT, "ytick.color": MUT,
    "axes.grid": True, "grid.color": LINE, "grid.alpha": .5, "grid.linewidth": .6,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": INK, "axes.facecolor": PANEL,
})

raw = pd.read_csv(HERE / "superheroes_dataset.csv")
bad = (raw.number_of_superhero_friends < 0) | (raw.injury_heal_time_days < 0) \
    | (raw.average_hours_of_superhero_power_used_per_day > 24)
raw["valid"] = ~bad
clean = raw[raw.valid].copy()
clean["gold"] = clean.outfit_color_code == "gold"

def stamp(ax, text):
    ax.set_title(text, color=CREAM, weight="bold", loc="left", fontsize=13, pad=10,
                 fontfamily="monospace")

# ---------- EXHIBIT A: scatter ----------
fig, ax = plt.subplots(figsize=(7.4, 4.7))
main = clean[~clean.gold]; gold = clean[clean.gold]
ax.scatter(main.number_of_superhero_friends, main.injury_heal_time_days,
           c=TEAL, s=44, alpha=.85, edgecolor=INK, linewidth=.6,
           label="Regular heroes (n=%d)" % len(main))
ax.scatter(gold.number_of_superhero_friends, gold.injury_heal_time_days,
           c=GOLD, s=78, alpha=.98, edgecolor=INK, linewidth=1,
           label="GOLD subgroup — prime suspect (n=%d)" % len(gold))
z = np.polyfit(main.number_of_superhero_friends, main.injury_heal_time_days, 1)
xs = np.linspace(main.number_of_superhero_friends.min(), main.number_of_superhero_friends.max(), 50)
ax.plot(xs, np.polyval(z, xs), color=RED, lw=2.2, ls=(0,(6,4)),
        label="Trend (regular): more friends → faster heal")
# circle the suspects
gx, gy = gold.number_of_superhero_friends.mean(), gold.injury_heal_time_days.mean()
ax.add_patch(mpatches.Ellipse((gx, gy), 26, 38, fill=False, edgecolor=RED, lw=1.6, ls=":"))
ax.annotate("THE ALIBI", (gx, gy+24), color=RED, fontsize=9, ha="center", weight="bold")
ax.set_xlabel("number_of_superhero_friends  (popularity →)")
ax.set_ylabel("injury_heal_time_days  (↓ = better)")
stamp(ax, "EXHIBIT A — one subgroup reverses the story")
ax.legend(fontsize=8, frameon=False, labelcolor=CREAM, loc="upper left")
fig.tight_layout(); fig.savefig(CHARTS / "scatter_simpsons.png", dpi=150, facecolor=INK); plt.close(fig)

# ---------- EXHIBIT B: reversal bars ----------
def split(d):
    m = d.number_of_superhero_friends.median()
    return d.assign(grp=np.where(d.number_of_superhero_friends > m, "Popular", "Nonpopular"))
allh = split(clean); nog = split(clean[~clean.gold])
def med(d, g): return d.loc[d.grp == g, "injury_heal_time_days"].median()
fig, ax = plt.subplots(figsize=(7.4, 4.2))
x = np.arange(2); w = .36
b1 = ax.bar(x - w/2, [med(allh,"Popular"), med(allh,"Nonpopular")], w, color=MUT, label="All heroes (raw evidence)")
b2 = ax.bar(x + w/2, [med(nog,"Popular"), med(nog,"Nonpopular")], w, color=TEAL, label="Suspect removed")
ax.set_xticks(x); ax.set_xticklabels(["Popular","Nonpopular"], color=CREAM)
ax.set_ylabel("median injury_heal_time_days  (↓ = better)")
stamp(ax, "EXHIBIT B — remove the suspect, the verdict flips")
ax.legend(fontsize=9, frameon=False, labelcolor=CREAM)
for b in list(b1)+list(b2):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+.5, f"{b.get_height():.0f}",
            ha="center", fontsize=9, color=CREAM)
fig.tight_layout(); fig.savefig(CHARTS / "bars_reversal.png", dpi=150, facecolor=INK); plt.close(fig)

# ---------- EXHIBIT C: tampering ----------
fig, ax = plt.subplots(figsize=(7.4, 3.6))
issues = {"Negative heal time": int((raw.injury_heal_time_days < 0).sum()),
          "Negative friends": int((raw.number_of_superhero_friends < 0).sum()),
          "Power > 24 h/day": int((raw.average_hours_of_superhero_power_used_per_day > 24).sum()),
          "Missing power value": int(raw.average_hours_of_superhero_power_used_per_day.isna().sum())}
cols = [RED, RED, RED, GOLD]
ax.barh(list(issues.keys()), list(issues.values()), color=cols, edgecolor=INK)
for i, v in enumerate(issues.values()): ax.text(v+.03, i, str(v), va="center", fontsize=10, color=CREAM)
ax.set_xlabel("rows affected")
stamp(ax, "EXHIBIT C — signs of tampering in the raw file")
ax.invert_yaxis(); fig.tight_layout(); fig.savefig(CHARTS / "data_quality.png", dpi=150, facecolor=INK); plt.close(fig)

# ---------- data.json ----------
payload = {
    "rows": raw[["hero_id","number_of_superhero_friends","injury_heal_time_days",
                 "recovery_quality_score","outfit_color_code",
                 "average_hours_of_superhero_power_used_per_day","valid"]]
            .where(pd.notna(raw), None).to_dict(orient="records"),
    "median_friends_clean": float(clean.number_of_superhero_friends.median()),
}
(HERE / "data.json").write_text(json.dumps(payload))
print(f"Wrote 3 forensic charts + data.json ({len(payload['rows'])} rows, {int(raw.valid.sum())} valid)")
