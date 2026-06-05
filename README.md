# Superhero Recovery — MTM Data Session

A worked example in **data hygiene, confounding, and not trusting auto-generated analysis**, built from a workshop breakout dataset.

**Research question:** Are there differences between popular and nonpopular superheroes regarding their ability to recover from injury?

**Short answer:** It depends entirely on data quality. The raw data "shows" popular heroes recover worse (p=0.008) — but that's an artifact of impossible values and one confounding subgroup (the 10 "gold" heroes, a Simpson's paradox). After cleaning and de-confounding, popular heroes actually heal *faster*, with equal recovery quality.

## View the site
Open `index.html` in any browser. It's a single self-contained file (interactive charts load Chart.js from CDN).

## Files
| File | Purpose |
|------|---------|
| `index.html` | The mini-site (generated — don't hand-edit) |
| `superheroes_dataset.csv` | Source data (110 heroes) |
| `analysis.py` | First pass — surfaces the data traps |
| `analysis_clean.py` | Cleaned + segmented analysis |
| `make_charts.py` | Generates static PNG charts + `data.json` |
| `build_site.py` | Builds `index.html` from data + code |
| `charts/` | Generated PNG visuals |

## Update workflow (living document)
```bash
# edit superheroes_dataset.csv (or the .py analysis), then:
python3 make_charts.py     # regenerate charts + data.json
python3 build_site.py      # rebuild index.html
```
Requires: `pandas`, `scipy`, `numpy`, `matplotlib`.

---
Meet the Moment · Data Session
