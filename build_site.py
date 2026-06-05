"""
Builds a single self-contained index.html from data.json + the .py source files.
Update workflow:  edit data/CSV  ->  python3 make_charts.py  ->  python3 build_site.py
"""
import json, html, pathlib, datetime
HERE = pathlib.Path(__file__).parent
data = json.loads((HERE / "data.json").read_text())
def code(fn): return html.escape((HERE / fn).read_text())
updated = datetime.date.today().isoformat()

PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Superhero Recovery — Data Session</title>
<meta name="color-scheme" content="light">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>%F0%9F%A6%B8</text></svg>">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js" integrity="sha384-JUh163oCRItcbPme8pYnROHQMC6fNKTBWtRG3I3I0erJkzNgL7uxKlNwcrcFKeqF" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css" integrity="sha384-oaMLBGEzBOJx3UHwac0cVndtX5fxGQIfnAeFZ35RTgqPcYlbprH9o9PUV/F8Le07" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js" integrity="sha384-F/bZzf7p3Joyp5psL90p/p89AZJsndkSoGwRpXcZhleCWhd8SnRuoYo4d0yirjJp" crossorigin="anonymous"></script>
<style>
:root{--navy:#1c487b;--teal:#2bb3a3;--gold:#d9a521;--cream:#f7f5ef;--ink:#1f2933;--mut:#5b6770;--line:#e6e2d8;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
 color:var(--ink);background:var(--cream);line-height:1.6}
.wrap{max-width:920px;margin:0 auto;padding:0 20px}
header{background:var(--navy);color:#fff;padding:38px 0 30px}
header .badge{display:inline-block;background:rgba(255,255,255,.15);color:#dcebff;font-size:12px;
 font-weight:600;padding:4px 11px;border-radius:20px;letter-spacing:.3px}
header h1{margin:14px 0 6px;font-size:30px;line-height:1.2}
header p.sub{margin:0;color:#bcd4ec;font-size:15px}
.rq{background:#fff;border-left:5px solid var(--teal);border-radius:8px;margin:26px 0;padding:18px 22px;
 box-shadow:0 1px 3px rgba(0,0,0,.05)}
.rq b{color:var(--navy)}
section{padding:30px 0;border-bottom:1px solid var(--line)}
h2{color:var(--navy);font-size:22px;margin:0 0 4px}
h2 .n{color:var(--teal);font-weight:800;margin-right:8px}
.lead{color:var(--mut);margin:0 0 18px;font-size:15px}
.answer{background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:8px 0 4px}
.answer table{width:100%;border-collapse:collapse;font-size:14.5px}
.answer th,.answer td{padding:11px 16px;text-align:left;border-top:1px solid var(--line)}
.answer th{background:#eef4fa;color:var(--navy)}
.bad{color:#b23b34;font-weight:700}.good{color:#16876f;font-weight:700}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card .big{font-size:24px;font-weight:800;color:var(--navy)}
.card .lbl{font-size:12.5px;color:var(--mut)}
ul.flags{list-style:none;padding:0;margin:0}
ul.flags li{background:#fff;border:1px solid var(--line);border-left:4px solid #d9534f;border-radius:8px;
 padding:10px 14px;margin:8px 0;font-size:14.5px}
ul.flags li.subtle{border-left-color:var(--gold)}
.chartbox{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px;margin:14px 0}
.chartbox h3{margin:0 0 4px;color:var(--navy);font-size:16px}
.chartbox p{margin:0 0 12px;font-size:13.5px;color:var(--mut)}
.toggle{font-size:13px;color:var(--navy);cursor:pointer;user-select:none;display:inline-flex;align-items:center;gap:7px}
.toggle input{transform:scale(1.15)}
.gallery{display:grid;grid-template-columns:1fr;gap:14px}
.gallery img{width:100%;border:1px solid var(--line);border-radius:10px;background:#fff}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:0}
.tabs button{background:#e9eef3;border:none;color:var(--navy);font-weight:600;font-size:13px;
 padding:8px 14px;border-radius:8px 8px 0 0;cursor:pointer}
.tabs button.active{background:#282c34;color:#fff}
pre{margin:0;border-radius:0 10px 10px 10px;max-height:460px;overflow:auto}
pre code{font-size:12.5px;line-height:1.5}
.takeaway{background:var(--navy);color:#fff;border-radius:10px;padding:20px 24px;margin:10px 0}
.takeaway b{color:#9fe6d9}
footer{padding:26px 0 50px;color:var(--mut);font-size:13px}
footer code{background:#ece8de;padding:2px 6px;border-radius:4px;font-size:12px}
@media(max-width:560px){header h1{font-size:24px}}
</style></head>
<body>
<header><div class="wrap">
 <span class="badge">MTM DATA SESSION · LIVING DOCUMENT · updated __UPDATED__</span>
 <h1>Popular vs. nonpopular superheroes:<br>do they recover from injury differently?</h1>
 <p class="sub">A worked example in data hygiene, confounding, and not trusting auto-generated analysis.</p>
</div></header>

<div class="wrap">

<div class="rq"><b>Research question.</b> Are there differences between popular and nonpopular
 superheroes regarding their ability to recover from injury? &nbsp;<i>(n = 110 heroes; 6 variables)</i></div>

<section>
 <h2><span class="n">TL;DR</span>The answer flips depending on data quality</h2>
 <p class="lead">Run the numbers on the raw file and you "find" that popular heroes recover worse.
  Clean the data and remove one confounding subgroup, and the effect reverses.</p>
 <div class="answer"><table>
  <tr><th>Approach</th><th>Result</th><th>Verdict</th></tr>
  <tr><td><b>Naive</b> — stats on raw data</td><td>Popular heal <b>slower</b> (41.6 vs 34.7 days, MWU p=0.008)</td><td class="bad">✗ Confounded</td></tr>
  <tr><td><b>Cleaned + de-confounded</b></td><td>Popular heal <b>faster</b> (median 27 vs 35 days, p&lt;0.001); recovery quality equal (p=0.77)</td><td class="good">✓ Real signal</td></tr>
 </table></div>
</section>

<section>
 <h2><span class="n">1</span>Method &amp; approach</h2>
 <ul>
  <li><b>"Popularity" has no column</b> → operationalized as <code>number_of_superhero_friends</code> (median split, <em>and</em> kept continuous so the answer doesn't hinge on a cutoff).</li>
  <li><b>"Recovery" is two things</b> → tested both <code>injury_heal_time_days</code> (lower = better) and <code>recovery_quality_score</code> (higher = better).</li>
  <li><b>Robust + parametric side by side</b> — Welch t-test, Mann–Whitney U, Spearman, medians. The disagreements between them are what exposed the traps.</li>
  <li><b>Checked confounds</b> — power usage, outfit color, and a distinct subgroup.</li>
 </ul>
</section>

<section>
 <h2><span class="n">2</span>The data-quality traps</h2>
 <p class="lead">Before any test: eyeball the min/max. This file is salted with errors.</p>
 <ul class="flags">
  <li><b>Negative heal time</b> — 2 heroes heal in −5 and −8 days (impossible)</li>
  <li><b>Negative friends</b> — 1 hero has −7 friends (impossible)</li>
  <li><b>Power &gt; 24 h/day</b> — 1 hero "uses powers" 180 hours per day</li>
  <li class="subtle"><b>Missing values</b> — 2 heroes have no power-usage value</li>
 </ul>
 <div class="chartbox"><h3>Red flags in the raw file</h3>
  <p>4 rows have impossible values and were removed (110 → 106).</p>
  <img src="charts/data_quality.png" alt="Data quality flags" style="width:100%;border-radius:8px"></div>
 <p style="font-size:14.5px"><b>The bigger trap — a confounding subgroup.</b> The 10 <span style="color:var(--gold);font-weight:700">gold-outfit</span>
  heroes are a distinct cluster: ~44 friends <em>and</em> ~91-day heal times, vs. ~9 friends / ~31 days for everyone else.
  Being both high-popularity and slow-healing, they single-handedly manufacture the "popularity hurts recovery" headline — a
  textbook <b>Simpson's paradox</b>.</p>
</section>

<section>
 <h2><span class="n">3</span>Interactive analysis</h2>
 <p class="lead">Toggle the gold subgroup to watch the relationship reverse.</p>
 <div class="cards">
  <div class="card"><div class="big">−0.77</div><div class="lbl">Spearman ρ, friends vs heal time <em>(regular heroes)</em> — more friends, faster heal</div></div>
  <div class="card"><div class="big">−0.31</div><div class="lbl">…diluted to this when the gold cluster is mixed back in</div></div>
  <div class="card"><div class="big">ρ ≈ 0.00</div><div class="lbl">friends vs recovery <em>quality</em> (no real link)</div></div>
  <div class="card"><div class="big">106 / 110</div><div class="lbl">valid rows after cleaning</div></div>
 </div>

 <div class="chartbox">
  <h3>Friends vs. heal time — the Simpson's paradox</h3>
  <p>Each point is a hero. The dashed line is the trend among regular heroes (downward = more friends → faster heal).</p>
  <label class="toggle"><input type="checkbox" id="goldToggle" checked> Show gold subgroup</label>
  <canvas id="scatter" height="170"></canvas>
 </div>

 <div class="chartbox">
  <h3>Median heal time: popular vs nonpopular</h3>
  <p>Grey = raw (all heroes). Teal = with the gold confound removed. Watch the bars cross.</p>
  <canvas id="bars" height="150"></canvas>
 </div>
</section>

<section>
 <h2><span class="n">4</span>Static visuals</h2>
 <p class="lead">Regeneratable PNGs (for slides / sharing) — produced by <code>make_charts.py</code>.</p>
 <div class="gallery">
  <img src="charts/scatter_simpsons.png" alt="Simpson's paradox scatter">
  <img src="charts/bars_reversal.png" alt="Effect reversal bars">
 </div>
</section>

<section>
 <h2><span class="n">5</span>The code</h2>
 <p class="lead">Every number above is reproducible. Three scripts, shown in full.</p>
 <div class="tabs" id="tabs">
  <button class="active" data-t="c1">analysis.py</button>
  <button data-t="c2">analysis_clean.py</button>
  <button data-t="c3">make_charts.py</button>
 </div>
 <div id="c1" class="codepane"><pre><code class="language-python">__CODE1__</code></pre></div>
 <div id="c2" class="codepane" style="display:none"><pre><code class="language-python">__CODE2__</code></pre></div>
 <div id="c3" class="codepane" style="display:none"><pre><code class="language-python">__CODE3__</code></pre></div>
</section>

<section>
 <h2><span class="n">6</span>Takeaways</h2>
 <div class="takeaway">
  <p style="margin:0 0 10px"><b>The lesson isn't the superheroes.</b> An AI/tool that just runs a t-test and reports
   "p = 0.008, popular heroes recover worse" hands you the <em>opposite</em> of the truth.</p>
  <p style="margin:0">Three habits would have caught it: &nbsp;<b>(1)</b> read the min/max before testing —
   negative heal times are a tell; &nbsp;<b>(2)</b> compare robust vs. parametric stats — a Pearson/Spearman
   sign flip screams "outliers"; &nbsp;<b>(3)</b> look for subgroups before trusting an aggregate p-value.</p>
 </div>
 <p style="font-size:14.5px;margin-top:14px"><b>So, the real answer:</b> among ordinary heroes, more popular ones
  <b>heal faster</b>, with equal recovery quality. The "popularity hurts recovery" finding is an artifact of impossible
  values and one outlier subgroup — not a real effect.</p>
</section>

<footer>
 <b>Living document.</b> To update: edit <code>superheroes_dataset.csv</code> → run
 <code>python3 make_charts.py</code> → <code>python3 build_site.py</code>. Open <code>index.html</code> in any browser.<br>
 Meet the Moment · Data Session · updated __UPDATED__
</footer>
</div>

<script>
const DATA = __DATA__;
const NAVY="#1c487b", TEAL="#2bb3a3", GOLD="#d9a521";
const rows = DATA.rows.filter(r => r.valid);
const reg = rows.filter(r => r.outfit_color_code!=="gold");
const gold = rows.filter(r => r.outfit_color_code==="gold");
const pt = r => ({x:r.number_of_superhero_friends, y:r.injury_heal_time_days});
// linear fit on regular heroes
function fit(pts){let n=pts.length,sx=0,sy=0,sxy=0,sxx=0;pts.forEach(p=>{sx+=p.x;sy+=p.y;sxy+=p.x*p.y;sxx+=p.x*p.x});
 let m=(n*sxy-sx*sy)/(n*sxx-sx*sx),b=(sy-m*sx)/n;let xs=pts.map(p=>p.x);
 let lo=Math.min(...xs),hi=Math.max(...xs);return [{x:lo,y:m*lo+b},{x:hi,y:m*hi+b}];}
const trend = fit(reg.map(pt));
const scatter = new Chart(document.getElementById("scatter"),{type:"scatter",
 data:{datasets:[
  {label:"Regular heroes",data:reg.map(pt),backgroundColor:TEAL,pointRadius:4},
  {label:"Gold subgroup",data:gold.map(pt),backgroundColor:GOLD,borderColor:NAVY,borderWidth:1,pointRadius:5.5},
  {label:"Trend (regular): more friends → faster heal",data:trend,type:"line",borderColor:NAVY,borderDash:[6,5],borderWidth:2,pointRadius:0,fill:false}
 ]},
 options:{plugins:{legend:{labels:{boxWidth:12,font:{size:11}}}},
  scales:{x:{title:{display:true,text:"Number of superhero friends (popularity →)"}},
   y:{title:{display:true,text:"Heal time (days) — ↓ better"}}}}});
document.getElementById("goldToggle").addEventListener("change",e=>{
 scatter.setDatasetVisibility(1,e.target.checked);scatter.update();});

function med(arr){arr=arr.slice().sort((a,b)=>a-b);let n=arr.length;return n?(n%2?arr[(n-1)/2]:(arr[n/2-1]+arr[n/2])/2):0;}
function split(rs){let f=rs.map(r=>r.number_of_superhero_friends),m=med(f);
 let pop=rs.filter(r=>r.number_of_superhero_friends>m),non=rs.filter(r=>r.number_of_superhero_friends<=m);
 return [med(pop.map(r=>r.injury_heal_time_days)), med(non.map(r=>r.injury_heal_time_days))];}
const allM=split(rows), nogM=split(reg);
new Chart(document.getElementById("bars"),{type:"bar",
 data:{labels:["Popular","Nonpopular"],datasets:[
  {label:"All heroes (raw)",data:allM,backgroundColor:"#9aa5b1"},
  {label:"Gold removed",data:nogM,backgroundColor:TEAL}]},
 options:{plugins:{legend:{labels:{boxWidth:12}}},
  scales:{y:{title:{display:true,text:"Median heal time (days) — ↓ better"}}}}});

document.querySelectorAll("#tabs button").forEach(b=>b.addEventListener("click",()=>{
 document.querySelectorAll("#tabs button").forEach(x=>x.classList.remove("active"));
 b.classList.add("active");
 ["c1","c2","c3"].forEach(id=>document.getElementById(id).style.display="none");
 document.getElementById(b.dataset.t).style.display="block";}));
hljs.highlightAll();
</script>
</body></html>"""

out = (PAGE.replace("__DATA__", json.dumps(data))
           .replace("__CODE1__", code("analysis.py"))
           .replace("__CODE2__", code("analysis_clean.py"))
           .replace("__CODE3__", code("make_charts.py"))
           .replace("__UPDATED__", updated))
(HERE / "index.html").write_text(out)
print(f"Built index.html ({len(out):,} bytes), updated {updated}")
