"""
Superhero recovery analysis — CLEANED + SEGMENTED (v2)
RQ: Are there differences between popular and nonpopular superheroes in
    their ability to recover from injury?

What v1 exposed:
- 4 impossible rows (negative heal time x2, negative friends x1, power=180 x1)
- A 'gold' subgroup (n=10) that is BOTH high-friend AND high-heal-time, which
  single-handedly drives a spurious "popular = slower recovery" result.
- Pearson(+0.77) vs Spearman(-0.29) sign flip = outliers hijacking the stat.
"""
import pandas as pd, numpy as np
from scipy import stats

raw = pd.read_csv("superheroes_dataset.csv")

# ---- 1. Clean impossible values ----
mask_bad = (raw.number_of_superhero_friends < 0) | (raw.injury_heal_time_days < 0) \
         | (raw.average_hours_of_superhero_power_used_per_day > 24)
df = raw.loc[~mask_bad].copy()
print(f"Removed {mask_bad.sum()} impossible rows -> n={len(df)} (from {len(raw)})")

med = df.number_of_superhero_friends.median()
df["popular"] = np.where(df.number_of_superhero_friends > med, "popular", "nonpopular")

def compare(data, col, higher_better, label):
    pop = data.loc[data.popular=="popular", col]; non = data.loc[data.popular=="nonpopular", col]
    u,pu = stats.mannwhitneyu(pop, non, alternative="two-sided")
    t,pt = stats.ttest_ind(pop, non, equal_var=False)
    print(f"  [{label}] {col} ({'hi' if higher_better else 'lo'}=better): "
          f"popular med={pop.median():.1f} mean={pop.mean():.1f} | "
          f"nonpop med={non.median():.1f} mean={non.mean():.1f} | "
          f"MWU p={pu:.3f} Welch p={pt:.3f}")

print("\n== A) Cleaned, ALL heroes (gold subgroup still included) ==")
compare(df, "injury_heal_time_days", False, "all")
compare(df, "recovery_quality_score", True, "all")

print("\n== B) Cleaned, EXCLUDING the gold subgroup (the confound) ==")
ng = df[df.outfit_color_code != "gold"].copy()
ng["popular"] = np.where(ng.number_of_superhero_friends > ng.number_of_superhero_friends.median(),
                         "popular","nonpopular")
compare(ng, "injury_heal_time_days", False, "no-gold")
compare(ng, "recovery_quality_score", True, "no-gold")

print("\n== C) Robust association: friends vs recovery (Spearman, cleaned) ==")
for sub,name in [(df,"all"),(ng,"no-gold")]:
    for col in ["injury_heal_time_days","recovery_quality_score"]:
        rho,p = stats.spearmanr(sub.number_of_superhero_friends, sub[col])
        print(f"  [{name:7s}] friends vs {col:24s}: Spearman rho={rho:+.2f} (p={p:.3f})")

print("\n== D) Is 'gold' a distinct population? (mean by outfit, cleaned) ==")
print(df.groupby("outfit_color_code")[["number_of_superhero_friends",
      "injury_heal_time_days","recovery_quality_score"]].mean().round(1).to_string())

print("\n== E) Power-usage confound (cleaned, NaNs dropped) ==")
p = df.dropna(subset=["average_hours_of_superhero_power_used_per_day"])
for a,b in [("number_of_superhero_friends","injury_heal_time_days"),
            ("average_hours_of_superhero_power_used_per_day","injury_heal_time_days")]:
    rho,pv = stats.spearmanr(p[a], p[b]); print(f"  {a} vs {b}: rho={rho:+.2f} (p={pv:.3f})")
