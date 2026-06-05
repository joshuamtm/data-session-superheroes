"""
Builds a single self-contained index.html (FORENSIC CASE-FILE design)
from data.json + the .py source files.
Update workflow:  edit data/CSV  ->  python3 make_charts.py  ->  python3 build_site.py
"""
import json, html, pathlib, datetime
HERE = pathlib.Path(__file__).parent
data = json.loads((HERE / "data.json").read_text())
def code(fn): return html.escape((HERE / fn).read_text())
updated = datetime.date.today().isoformat()

PAGE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Case File SH-110 — The Dataset That Lied</title>
<meta name="color-scheme" content="dark">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>%F0%9F%95%B5%EF%B8%8F</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,900;1,9..144,500;1,9..144,900&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js" integrity="sha384-JUh163oCRItcbPme8pYnROHQMC6fNKTBWtRG3I3I0erJkzNgL7uxKlNwcrcFKeqF" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css" integrity="sha384-oaMLBGEzBOJx3UHwac0cVndtX5fxGQIfnAeFZ35RTgqPcYlbprH9o9PUV/F8Le07" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js" integrity="sha384-F/bZzf7p3Joyp5psL90p/p89AZJsndkSoGwRpXcZhleCWhd8SnRuoYo4d0yirjJp" crossorigin="anonymous"></script>
<style>
:root{
 --ink:#15120D; --panel:#211C14; --panel2:#2a2419; --paper:#E9E0CB;
 --cream:#ECE4D2; --mut:#9A8F77; --faint:#6b6151;
 --red:#E5472D; --gold:#E0A53B; --teal:#6FB7AE; --line:#3a3328;
 --serif:'Fraunces',Georgia,serif; --mono:'IBM Plex Mono',ui-monospace,monospace; --body:'Archivo',system-ui,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ink);color:var(--cream);font-family:var(--body);line-height:1.65;
 -webkit-font-smoothing:antialiased;overflow-x:hidden}
/* film grain + vignette */
body::before{content:"";position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.05;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
body::after{content:"";position:fixed;inset:0;z-index:1;pointer-events:none;
 background:radial-gradient(120% 80% at 50% -10%, transparent 55%, rgba(0,0,0,.55) 100%)}
.wrap{max-width:980px;margin:0 auto;padding:0 24px;position:relative;z-index:2}
a{color:var(--gold)}
.mono{font-family:var(--mono);text-transform:uppercase;letter-spacing:.16em;font-size:11.5px;color:var(--mut)}

/* status bar */
.statusbar{border-bottom:1px solid var(--line);background:rgba(0,0,0,.25);position:relative;z-index:2}
.statusbar .wrap{display:flex;justify-content:space-between;gap:14px;padding-top:11px;padding-bottom:11px;flex-wrap:wrap}
.statusbar .red{color:var(--red)}

/* masthead */
.mast{position:relative;padding:64px 0 30px;z-index:2}
.ghostno{position:absolute;right:8px;top:-6px;font-family:var(--serif);font-weight:900;font-size:200px;
 line-height:.8;color:#fff;opacity:.035;letter-spacing:-.04em;pointer-events:none;z-index:0}
.kicker{color:var(--red);font-family:var(--mono);text-transform:uppercase;letter-spacing:.3em;font-size:12px;margin-bottom:18px}
h1.title{font-family:var(--serif);font-weight:900;font-style:italic;font-size:clamp(44px,8.5vw,98px);
 line-height:.92;letter-spacing:-.02em;margin:0 0 20px;color:#fff}
h1.title em{font-style:normal;color:var(--gold)}
.dek{font-family:var(--serif);font-weight:500;font-size:clamp(18px,2.4vw,23px);color:var(--cream);max-width:640px;line-height:1.4}
.brief{margin-top:26px;border:1px solid var(--line);border-left:3px solid var(--teal);background:var(--panel);
 padding:16px 20px;max-width:680px;font-size:15px}
.brief .mono{display:block;margin-bottom:6px;color:var(--teal)}

/* red stamp */
.stamp{position:absolute;z-index:3;font-family:var(--mono);font-weight:600;text-transform:uppercase;
 color:var(--red);border:3px double var(--red);border-radius:6px;padding:8px 16px;letter-spacing:.18em;font-size:15px;
 box-shadow:0 0 0 1px rgba(229,71,45,.25);background:rgba(229,71,45,.05);text-align:center;line-height:1.25;
 opacity:.92;mix-blend-mode:screen}
.stamp small{display:block;font-size:9.5px;letter-spacing:.22em;color:#f0a99c;margin-top:2px}
.stamp.mast-stamp{top:50px;right:18px;transform:rotate(-9deg) scale(1);animation:slam .7s cubic-bezier(.2,1.4,.3,1) .5s both}
@keyframes slam{0%{opacity:0;transform:rotate(-9deg) scale(2.6)}60%{opacity:1}100%{opacity:.92;transform:rotate(-9deg) scale(1)}}
@media(max-width:680px){.stamp.mast-stamp{position:static;display:inline-block;margin-top:20px;transform:rotate(-3deg)}}

/* generic section */
section{padding:54px 0;border-top:1px solid var(--line);position:relative;z-index:2}
.label{display:flex;align-items:baseline;gap:14px;margin-bottom:18px}
.label .ex{font-family:var(--mono);color:var(--red);font-size:12px;letter-spacing:.2em;border:1px solid var(--red);
 padding:3px 8px;white-space:nowrap}
.label h2{font-family:var(--serif);font-weight:900;font-size:clamp(26px,4vw,40px);line-height:1;margin:0;color:#fff;letter-spacing:-.01em}
.lead{color:var(--mut);font-size:15.5px;max-width:680px;margin:0 0 24px}
.reveal{transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.2,1)}
html.js .reveal{opacity:0;transform:translateY(26px)}
html.js .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){html.js .reveal{opacity:1;transform:none}}

/* paper clipping (the dispatch) */
.clip{background:var(--paper);color:#211a10;border-radius:3px;padding:38px 40px;position:relative;
 box-shadow:0 30px 60px -20px rgba(0,0,0,.7),0 2px 0 rgba(255,255,255,.06);transform:rotate(-.5deg)}
.clip::before,.clip::after{content:"";position:absolute;width:16px;height:16px;border:2px solid #b9ac8c}
.clip::before{top:10px;left:10px;border-right:0;border-bottom:0}
.clip::after{bottom:10px;right:10px;border-left:0;border-top:0}
.clip .head{font-family:var(--mono);text-transform:uppercase;letter-spacing:.2em;font-size:11px;color:#8a6d3b;
 border-bottom:2px solid #211a10;padding-bottom:8px;margin-bottom:18px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
.clip h3{font-family:var(--serif);font-weight:900;font-size:clamp(28px,4.6vw,44px);line-height:1.02;margin:0 0 6px;color:#191309}
.clip .byline{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#7a5d2e;margin-bottom:20px}
.clip .cols{columns:2;column-gap:34px;column-rule:1px solid #cdbf9d;font-size:15.5px;color:#2c2316;line-height:1.62}
.clip .cols p{margin:0 0 14px;break-inside:avoid}
.clip .cols p:first-of-type::first-letter{font-family:var(--serif);font-weight:900;float:left;font-size:64px;
 line-height:.72;padding:6px 10px 0 0;color:var(--red)}
.clip .kick{font-family:var(--serif);font-style:italic;font-weight:600;font-size:17px;color:#191309;margin-top:6px;
 border-top:1px solid #cdbf9d;padding-top:14px;column-span:all}
@media(max-width:680px){.clip .cols{columns:1}.clip{padding:26px 22px}}

/* accusation vs truth */
.docket{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.docket>div{padding:22px 24px}
.docket .acc{background:var(--panel);border-right:1px solid var(--line)}
.docket .tru{background:linear-gradient(180deg,rgba(111,183,174,.07),transparent)}
.docket h4{font-family:var(--mono);text-transform:uppercase;letter-spacing:.2em;font-size:11px;margin:0 0 12px}
.docket .acc h4{color:var(--red)}.docket .tru h4{color:var(--teal)}
.docket p{margin:0;font-size:15px}.docket .stat{font-family:var(--serif);font-weight:900;font-size:24px;display:block;margin-top:8px;color:#fff}
@media(max-width:620px){.docket{grid-template-columns:1fr}.docket .acc{border-right:0;border-bottom:1px solid var(--line)}}

/* evidence tags */
.tags{display:flex;flex-direction:column;gap:12px}
.tag{display:flex;align-items:center;gap:16px;background:var(--panel);border:1px solid var(--line);
 border-left:4px solid var(--red);border-radius:4px;padding:13px 18px}
.tag.amber{border-left-color:var(--gold)}
.tag .id{font-family:var(--mono);font-size:11px;color:var(--mut);letter-spacing:.1em;white-space:nowrap}
.tag .what{font-size:15px}.tag b{color:#fff}
.tag .ct{margin-left:auto;font-family:var(--serif);font-weight:900;font-size:26px;color:var(--red)}
.tag.amber .ct{color:var(--gold)}

/* exhibit panels (charts) */
.exhibit{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:22px;position:relative;margin:16px 0}
.exhibit::before,.exhibit::after,.exhibit .c1,.exhibit .c2{content:"";position:absolute;width:14px;height:14px;border:2px solid var(--faint)}
.exhibit::before{top:9px;left:9px;border-right:0;border-bottom:0}
.exhibit::after{top:9px;right:9px;border-left:0;border-bottom:0}
.exhibit .c1{bottom:9px;left:9px;border-right:0;border-top:0}
.exhibit .c2{bottom:9px;right:9px;border-left:0;border-top:0}
.exhibit h3{font-family:var(--mono);text-transform:uppercase;letter-spacing:.14em;font-size:13px;color:var(--gold);margin:4px 0 2px}
.exhibit p.cap{font-size:13px;color:var(--mut);margin:0 0 14px}
.chartwrap{position:relative;height:340px;width:100%}
@media(max-width:560px){.chartwrap{height:300px}}
.toggle{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--cream);
 cursor:pointer;user-select:none;display:inline-flex;align-items:center;gap:9px;margin-bottom:8px}
.toggle input{accent-color:var(--gold);transform:scale(1.2)}

/* evidence markers (stats) */
.markers{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:18px 0}
.marker{border:1px solid var(--line);border-radius:5px;padding:16px 18px;background:var(--panel);position:relative}
.marker .big{font-family:var(--serif);font-weight:900;font-size:30px;color:var(--gold);line-height:1}
.marker .lbl{font-size:12.5px;color:var(--mut);margin-top:8px}
.marker .lbl b{color:var(--cream)}

/* locker (static pngs) */
.locker{display:grid;grid-template-columns:1fr;gap:16px}
.locker figure{margin:0;border:1px solid var(--line);border-radius:6px;overflow:hidden;background:var(--ink)}
.locker img{width:100%;display:block}
.locker figcaption{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);padding:9px 14px;border-top:1px solid var(--line)}

/* method list */
.method{list-style:none;padding:0;margin:0;counter-reset:m}
.method li{counter-increment:m;position:relative;padding:14px 0 14px 52px;border-bottom:1px solid var(--line);font-size:15.5px}
.method li::before{content:counter(m,decimal-leading-zero);position:absolute;left:0;top:13px;font-family:var(--mono);
 color:var(--red);font-size:13px;border:1px solid var(--line);padding:2px 7px}
.method b{color:#fff}.method code{font-family:var(--mono);font-size:13px;background:#000;color:var(--teal);padding:1px 6px;border-radius:3px}

/* code */
.tabs{display:flex;gap:0;flex-wrap:wrap;margin-bottom:0;border-bottom:1px solid var(--line)}
.tabs button{background:transparent;border:0;border-bottom:2px solid transparent;color:var(--mut);
 font-family:var(--mono);font-size:12.5px;letter-spacing:.05em;padding:10px 16px;cursor:pointer}
.tabs button.active{color:var(--gold);border-bottom-color:var(--gold)}
pre{margin:0;border-radius:0 0 8px 8px;max-height:480px;overflow:auto;border:1px solid var(--line);border-top:0}
pre code{font-size:12.5px;line-height:1.55;font-family:var(--mono)}

/* verdict */
.verdict{position:relative;border:1px solid var(--line);border-radius:8px;padding:40px 36px;background:
 linear-gradient(180deg,var(--panel2),var(--panel));overflow:hidden}
.verdict .vstamp{position:absolute;top:22px;right:-6px;transform:rotate(8deg);font-family:var(--mono);font-weight:600;
 color:var(--teal);border:3px double var(--teal);border-radius:6px;padding:7px 14px;letter-spacing:.2em;font-size:14px;
 opacity:.9;mix-blend-mode:screen}
.verdict h3{font-family:var(--serif);font-weight:900;font-size:clamp(24px,3.6vw,34px);margin:0 0 14px;color:#fff;max-width:660px}
.verdict p{font-size:16px;max-width:680px}
.protocol{margin-top:26px;display:grid;gap:12px}
.protocol .p{display:flex;gap:14px;align-items:flex-start;font-size:15px}
.protocol .p .n{font-family:var(--mono);color:var(--gold);font-size:12px;border:1px solid var(--gold);padding:2px 7px;white-space:nowrap;margin-top:2px}
.protocol b{color:#fff}

footer{padding:44px 0 70px;border-top:1px solid var(--line);position:relative;z-index:2}
footer .mono{display:block;margin-bottom:8px}
footer code{font-family:var(--mono);background:#000;color:var(--teal);padding:2px 7px;border-radius:3px;font-size:12px}
</style></head>
<body>

<div class="statusbar"><div class="wrap">
 <span class="mono">Case File No. <span style="color:var(--cream)">SH-110</span> · Data Forensics Unit</span>
 <span class="mono">Status: <span class="red">▌ Closed</span> · Updated __UPDATED__</span>
</div></div>

<div class="mast"><div class="wrap">
 <div class="ghostno">110</div>
 <div class="stamp mast-stamp">Tampering Detected<small>4 exhibits · 1 suspect</small></div>
 <div class="kicker">Data Forensics · Exhibit Dossier</div>
 <h1 class="title">The Dataset<br>That <em>Lied</em></h1>
 <p class="dek">An investigation into 110 superheroes, one impossible spreadsheet, and the statistic that nearly got away with it.</p>
 <div class="brief">
  <span class="mono">The question on file</span>
  Are there differences between <b>popular</b> and <b>nonpopular</b> superheroes in their ability to <b>recover from injury</b>? &nbsp;<span class="mono" style="display:inline">n=110 · 6 variables</span>
 </div>
</div></div>

<!-- THE DISPATCH -->
<section><div class="wrap reveal">
 <div class="clip">
  <div class="head"><span>The Metro Wire · Superhero Beat</span><span>Filed: Tuesday · Page A1</span></div>
  <h3>Popularity Is "Hurting" Our Heroes. So We Opened the File.</h3>
  <div class="byline">By the Data Forensics Unit · Photographs withheld pending review</div>
  <div class="cols">
   <p>It started, as these things always do, with a confident chart. One hundred and ten working superheroes — friend counts logged, injuries timed, costumes filed by color — landed on our desk with a damning headline stapled to the front: the more popular the hero, the worse they heal. Fame, the study warned, is hazardous to your cape.</p>
   <p>It's a great story. Capes love a great story. But great stories and good data are not always the same animal, and this one had a tell. Heroes healing in negative five days. A caped crusader with minus seven friends. Someone clocking 180 hours of superpower use inside a 24-hour day. Either physics filed for bankruptcy — or the spreadsheet did.</p>
   <p>So we did the one thing no press release wants you to do. We opened the file. What we found wasn't a trend. It was a line-up — and standing at the front, dressed head to toe in gold, was a suspect with an alibi too clean to trust.</p>
   <p class="kick">This is the case file. The evidence is below. You decide who's lying — the heroes, or the histogram.</p>
  </div>
 </div>
</div></section>

<!-- THE ACCUSATION -->
<section><div class="wrap reveal">
 <div class="label"><span class="ex">The Charge</span><h2>A confession the data didn't mean</h2></div>
 <p class="lead">Run a test on the raw file and you get a tidy, publishable, completely wrong result. Clean it and the story inverts.</p>
 <div class="docket">
  <div class="acc"><h4>The accusation (raw data)</h4><p>"Popular heroes recover worse."<span class="stat">41.6 vs 34.7 days · p=0.008</span></p></div>
  <div class="tru"><h4>The truth (cleaned + de-confounded)</h4><p>Popular heroes recover <b>faster</b>; recovery quality is equal.<span class="stat">27 vs 35 days · p&lt;0.001</span></p></div>
 </div>
</div></section>

<!-- EXHIBIT C: tampering -->
<section><div class="wrap reveal">
 <div class="label"><span class="ex">Exhibit C</span><h2>Signs of tampering</h2></div>
 <p class="lead">Before a single test: read the min and max. Four rows hold values that cannot physically exist — removed (110 → 106).</p>
 <div class="tags">
  <div class="tag"><span class="id">EV-01</span><span class="what"><b>Negative heal time</b> — two heroes "recover" in −5 and −8 days</span><span class="ct">2</span></div>
  <div class="tag"><span class="id">EV-02</span><span class="what"><b>Negative friends</b> — one hero logged at −7 acquaintances</span><span class="ct">1</span></div>
  <div class="tag"><span class="id">EV-03</span><span class="what"><b>Power &gt; 24 h/day</b> — one hero at 180 hours in a 24-hour day</span><span class="ct">1</span></div>
  <div class="tag amber"><span class="id">EV-04</span><span class="what"><b>Missing values</b> — two power-usage readings absent</span><span class="ct">2</span></div>
 </div>
 <div class="exhibit" style="margin-top:18px"><span class="c1"></span><span class="c2"></span>
  <h3>Exhibit C · tampering ledger</h3><img src="charts/data_quality.png" alt="Data quality flags" style="width:100%;border-radius:4px"></div>
</div></section>

<!-- EXHIBIT A: suspect -->
<section><div class="wrap reveal">
 <div class="label"><span class="ex">Exhibit A</span><h2>The prime suspect</h2></div>
 <p class="lead">The 10 <span style="color:var(--gold);font-weight:700">gold-outfit</span> heroes are a separate population: ~44 friends <em>and</em> ~91-day heal times, against ~9 friends / ~31 days for everyone else. Being both high-popularity and slow-healing, they alone manufacture the headline — a textbook <b>Simpson's paradox</b>. Pull them from the line-up:</p>
 <div class="exhibit"><span class="c1"></span><span class="c2"></span>
  <h3>Exhibit A · friends vs. heal time</h3>
  <p class="cap">Each point is a hero. Dashed red line = trend among regular heroes (down = more friends → faster heal).</p>
  <label class="toggle"><input type="checkbox" id="goldToggle" checked> Show the gold suspects</label>
  <div class="chartwrap"><canvas id="scatter"></canvas></div>
 </div>
 <div class="markers">
  <div class="marker"><div class="big">−0.77</div><div class="lbl">Spearman ρ, friends vs heal time <b>(regular heroes)</b> — more friends, faster heal</div></div>
  <div class="marker"><div class="big">−0.31</div><div class="lbl">…diluted to this once the gold suspects rejoin the data</div></div>
  <div class="marker"><div class="big">ρ≈0.00</div><div class="lbl">friends vs recovery <b>quality</b> — no real link</div></div>
  <div class="marker"><div class="big">106/110</div><div class="lbl">valid rows after removing tampered evidence</div></div>
 </div>
</div></section>

<!-- EXHIBIT B: alibi -->
<section><div class="wrap reveal">
 <div class="label"><span class="ex">Exhibit B</span><h2>The alibi collapses</h2></div>
 <p class="lead">Median heal time, popular vs nonpopular. Grey is the raw line-up; teal is the same comparison with the suspect removed. Watch the bars cross.</p>
 <div class="exhibit"><span class="c1"></span><span class="c2"></span>
  <h3>Exhibit B · median heal time by group</h3>
  <p class="cap">Lower = better recovery.</p>
  <div class="chartwrap"><canvas id="bars"></canvas></div>
 </div>
</div></section>

<!-- METHOD -->
<section><div class="wrap reveal">
 <div class="label"><span class="ex">The Method</span><h2>How we worked the case</h2></div>
 <ol class="method">
  <li><b>Named the suspect variable.</b> "Popularity" has no column → used <code>number_of_superhero_friends</code> (median split <em>and</em> kept continuous, so no single cutoff carries the verdict).</li>
  <li><b>Two definitions of "recovery."</b> Tested <code>injury_heal_time_days</code> (lower = better) and <code>recovery_quality_score</code> (higher = better) separately.</li>
  <li><b>Robust vs. parametric, side by side.</b> Welch t, Mann–Whitney U, Spearman, medians. A Pearson <b>+0.77</b> / Spearman <b>−0.31</b> sign-flip was the tell that outliers were testifying.</li>
  <li><b>Ran down the confounds.</b> Power usage (red herring), outfit color (where the suspect was hiding), and the gold subgroup itself.</li>
 </ol>
</div></section>

<!-- CODE -->
<section><div class="wrap reveal">
 <div class="label"><span class="ex">The Lab Notebook</span><h2>Reproducible to the last number</h2></div>
 <p class="lead">Every figure above comes from these three scripts — shown in full.</p>
 <div class="tabs" id="tabs">
  <button class="active" data-t="c1">analysis.py</button>
  <button data-t="c2">analysis_clean.py</button>
  <button data-t="c3">make_charts.py</button>
 </div>
 <div id="c1" class="codepane"><pre><code class="language-python">__CODE1__</code></pre></div>
 <div id="c2" class="codepane" style="display:none"><pre><code class="language-python">__CODE2__</code></pre></div>
 <div id="c3" class="codepane" style="display:none"><pre><code class="language-python">__CODE3__</code></pre></div>
</div></section>

<!-- EVIDENCE LOCKER -->
<section><div class="wrap reveal">
 <div class="label"><span class="ex">Evidence Locker</span><h2>Printable exhibits</h2></div>
 <p class="lead">Regeneratable PNGs for slides &amp; sharing — output of <code style="font-family:var(--mono);color:var(--teal)">make_charts.py</code>.</p>
 <div class="locker">
  <figure><img src="charts/scatter_simpsons.png" alt="Exhibit A"><figcaption>Exhibit A — the prime suspect</figcaption></figure>
  <figure><img src="charts/bars_reversal.png" alt="Exhibit B"><figcaption>Exhibit B — the alibi collapses</figcaption></figure>
 </div>
</div></section>

<!-- VERDICT -->
<section><div class="wrap reveal">
 <div class="label"><span class="ex">The Verdict</span><h2>Case closed</h2></div>
 <div class="verdict">
  <div class="vstamp">Ruling Entered</div>
  <h3>Among ordinary heroes, the more popular ones heal <em style="color:var(--teal);font-style:normal">faster</em> — with equal recovery quality.</h3>
  <p>The "popularity hurts recovery" headline was never a finding. It was an artifact of impossible values and one outlier subgroup. The lesson isn't the superheroes — it's that an AI or tool that simply runs a test and reports <span style="font-family:var(--mono);color:var(--red)">p=0.008</span> will hand you the <b>opposite</b> of the truth.</p>
  <div class="protocol">
   <div class="p"><span class="n">01</span><span><b>Read the min/max before the model.</b> Negative heal times confess on sight.</span></div>
   <div class="p"><span class="n">02</span><span><b>Compare robust vs. parametric.</b> A Pearson/Spearman sign-flip means outliers are running the show.</span></div>
   <div class="p"><span class="n">03</span><span><b>Look for subgroups before trusting any aggregate p-value.</b> One hidden cluster can invent — or erase — an entire effect.</span></div>
  </div>
 </div>
</div></section>

<footer><div class="wrap">
 <span class="mono">Living document · to update</span>
 Edit <code>superheroes_dataset.csv</code> → run <code>python3 make_charts.py</code> → <code>python3 build_site.py</code> → open <code>index.html</code>.<br><br>
 <span class="mono" style="color:var(--faint)">Meet the Moment · Data Forensics Unit · Case SH-110 · Updated __UPDATED__</span>
</div></footer>

<script>
const DATA = __DATA__;
const INK="#15120D",CREAM="#ECE4D2",MUT="#9A8F77",LINE="#3a3328",TEAL="#6FB7AE",GOLD="#E0A53B",RED="#E5472D";
const rows = DATA.rows.filter(r=>r.valid);
const reg = rows.filter(r=>r.outfit_color_code!=="gold");
const gold = rows.filter(r=>r.outfit_color_code==="gold");
const pt = r => ({x:r.number_of_superhero_friends, y:r.injury_heal_time_days});
function fit(pts){let n=pts.length,sx=0,sy=0,sxy=0,sxx=0;pts.forEach(p=>{sx+=p.x;sy+=p.y;sxy+=p.x*p.y;sxx+=p.x*p.x});
 let m=(n*sxy-sx*sy)/(n*sxx-sx*sx),b=(sy-m*sx)/n,xs=pts.map(p=>p.x),lo=Math.min(...xs),hi=Math.max(...xs);
 return [{x:lo,y:m*lo+b},{x:hi,y:m*hi+b}];}
if(window.Chart){
 Chart.defaults.color=MUT; Chart.defaults.font.family="'IBM Plex Mono',monospace"; Chart.defaults.font.size=11;
 Chart.defaults.borderColor=LINE;
 const trend=fit(reg.map(pt));
 const scatter=new Chart(document.getElementById("scatter"),{type:"scatter",
  data:{datasets:[
   {label:"Regular heroes",data:reg.map(pt),backgroundColor:TEAL,pointRadius:4,pointHoverRadius:6},
   {label:"Gold suspects",data:gold.map(pt),backgroundColor:GOLD,borderColor:INK,borderWidth:1,pointRadius:6,pointHoverRadius:8},
   {label:"Trend (regular)",data:trend,type:"line",borderColor:RED,borderDash:[6,5],borderWidth:2,pointRadius:0,fill:false}
  ]},
  options:{maintainAspectRatio:false,plugins:{legend:{labels:{color:CREAM,boxWidth:12,font:{size:10}}},
   tooltip:{backgroundColor:"#000",borderColor:LINE,borderWidth:1,titleColor:GOLD,bodyColor:CREAM}},
   scales:{x:{grid:{color:LINE},title:{display:true,text:"friends (popularity →)",color:MUT}},
    y:{grid:{color:LINE},title:{display:true,text:"heal time (days) ↓ better",color:MUT}}}}});
 document.getElementById("goldToggle").addEventListener("change",e=>{scatter.setDatasetVisibility(1,e.target.checked);scatter.update();});
 function med(a){a=a.slice().sort((x,y)=>x-y);let n=a.length;return n?(n%2?a[(n-1)/2]:(a[n/2-1]+a[n/2])/2):0;}
 function split(rs){let f=rs.map(r=>r.number_of_superhero_friends),m=med(f);
  return [med(rs.filter(r=>r.number_of_superhero_friends>m).map(r=>r.injury_heal_time_days)),
          med(rs.filter(r=>r.number_of_superhero_friends<=m).map(r=>r.injury_heal_time_days))];}
 new Chart(document.getElementById("bars"),{type:"bar",
  data:{labels:["Popular","Nonpopular"],datasets:[
   {label:"All heroes (raw)",data:split(rows),backgroundColor:MUT},
   {label:"Suspect removed",data:split(reg),backgroundColor:TEAL}]},
  options:{maintainAspectRatio:false,plugins:{legend:{labels:{color:CREAM,boxWidth:12}},
   tooltip:{backgroundColor:"#000",borderColor:LINE,borderWidth:1,titleColor:GOLD,bodyColor:CREAM}},
   scales:{x:{grid:{color:"transparent"},ticks:{color:CREAM}},
    y:{grid:{color:LINE},title:{display:true,text:"median heal time (days) ↓ better",color:MUT}}}}});
}
// tabs
document.querySelectorAll("#tabs button").forEach(b=>b.addEventListener("click",()=>{
 document.querySelectorAll("#tabs button").forEach(x=>x.classList.remove("active"));b.classList.add("active");
 ["c1","c2","c3"].forEach(id=>document.getElementById(id).style.display="none");
 document.getElementById(b.dataset.t).style.display="block";}));
// reveal on scroll (staggered) — progressive enhancement
document.documentElement.classList.add("js");
const io=new IntersectionObserver((es)=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}}),{threshold:.12,rootMargin:"0px 0px -8% 0px"});
document.querySelectorAll(".reveal").forEach((el,i)=>{el.style.transitionDelay=(i%3*90)+"ms";io.observe(el);});
// safety net: never leave content hidden
setTimeout(()=>document.querySelectorAll(".reveal:not(.in)").forEach(e=>e.classList.add("in")),2600);
if(window.hljs) hljs.highlightAll();
</script>
</body></html>"""

out = (PAGE.replace("__DATA__", json.dumps(data))
           .replace("__CODE1__", code("analysis.py"))
           .replace("__CODE2__", code("analysis_clean.py"))
           .replace("__CODE3__", code("make_charts.py"))
           .replace("__UPDATED__", updated))
(HERE / "index.html").write_text(out)
print(f"Built index.html ({len(out):,} bytes), updated {updated}")
