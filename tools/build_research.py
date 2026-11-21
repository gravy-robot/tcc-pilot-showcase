"""Build research/index.html: Healthcare persona -> Journey -> Jobs to be done.

One standalone page with stable anchors for the kickoff Google Doc:
  #persona, #journey, #jobs-to-be-done
  #journey-notice ... #journey-return   (one per stage)
  #persona-notice ... #persona-return   (Dr. Maya's voice at each stage)
  #j1 ... #j7                           (one per job)

Sources:
  reference/persona-and-stages.md               persona and stage table
  reference/maps/Main.dc.html                   journey grid (via build_maps.py helpers)
  reference/requirements/content-example-jtbd.md jobs to be done
  RESEARCH below                                figures from the TCC and AU reports,
                                                checked against the PDFs (Nov 21, 2026)

Run from the site root after build_content_example.py (the journey links to its
per-example pages):  python3 tools/build_research.py .
"""
import html, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_maps  # noqa: E402  (helpers only; its builds run under __main__)

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
persona_md = (root / "reference" / "persona-and-stages.md").read_text()
jtbd_md = (root / "reference" / "requirements" / "content-example-jtbd.md").read_text()
map_src = (root / "reference" / "maps" / "Main.dc.html").read_text()

STAGES = ["notice", "explore", "join", "learn", "create", "share", "return"]
STAGE_NAMES = ["Notice", "Explore", "Join", "Learn", "Create", "Share", "Return and connect"]

# ---------------------------------------------------------------------------
# Research behind each job. Page numbers are PDF pages. Wording rule from
# reference/research-facts.md: "in the TCC/AU research" for survey figures,
# "in our audit" for view counts. Don't add a figure without checking the PDF.
# ---------------------------------------------------------------------------
TCC = "tcc"
AU = "au"
AUDIT = "audit"
REPORTS = {
    TCC: ("TCC insights report", "Who’s Really Talking About Climate? Mapping climate communication in the United States and Canada. Talking Climate Collaborative, Landscape Assessment 2026.", "https://talkingclimate.com"),
    AU: ("AU research report", "Fisher, D. R., Jayko, W. C., and Jasny, L. Mapping the Ecosystem of Climate Communication in the US and Canada: A Landscape Assessment. American University, July 30, 2026.", "https://doi.org/10.57912/32957927"),
    AUDIT: ("Example audit", "TCC curated content segment example audit, Nov 6, 2026.", "../audit/index.html"),
}
RESEARCH = {
    "j1": [
        (TCC, 5, "The messengers people know and trust, doctors among them, are rarely the ones with access to the research, the framing or local data."),
        (TCC, 6, "Only 19% of communicators in the TCC/AU research reach health professionals, though “people trust the people that they already know.”"),
    ],
    "j2": [
        (TCC, 7, "Of communicators who target by profession, fewer than one in five focus on the health sector itself."),
        (AU, 17, "34.7% say a regular feed of curated, trusted content to quote, share or repost would help them."),
    ],
    "j3": [],
    "j4": [
        (TCC, 7, "Communicators want regular updates on what works (54%) far more than training (27%) or science education (24%)."),
        (AU, 17, "The same survey table, unrounded: best-practice updates 53.5%, training 26.5%, science education 24.1%."),
        (TCC, 7, "Published findings rarely reach “the doctor with two dozen patients waiting.”"),
    ],
    "j5": [
        (TCC, 4, "Sharing alarming updates about global trends raises awareness and concern but erodes efficacy, the sense that action matters."),
        (AU, 17, "37.6% want customized tips for different forms of communication, such as social media and video."),
        (AUDIT, None, "In our audit, both segments miss most often on P4 Doable and P8 For Everyone (partisan framing)."),
    ],
    "j6": [
        (TCC, 6, "Endorsing candidates is communicators’ least common goal, chosen by only 1 in 25: evidence that the field isn’t partisan."),
        (AUDIT, None, "In our audit, the best health videos had only 20 and 55 views. Good precedent exists but few people see it."),
    ],
    "j7": [
        (TCC, 7, "57% of communicators want help finding peers and collaborators, tied with “what works” as the top need after funding (AU: 57.1%, PDF p. 17)."),
        (TCC, 5, "Communicators mostly work alone, rarely team up or share ideas, and connect mostly with people like themselves."),
        (AU, 4, "34% of respondents work alone; another 34% work in organizations of 10 or fewer full-time staff."),
    ],
}
NO_RESEARCH = {
    "j2": "No TCC/AU finding tests filtering by role, topic or place. That need comes from the journey’s pain point.",
    "j3": "No TCC/AU research finding. This job rests on the journey and persona only. Test it in clinician interviews.",
    "j6": "No TCC/AU finding on employer or comms-office approval. That need comes from the journey and persona.",
}

# ---------------------------------------------------------------------------
# Parse sources
# ---------------------------------------------------------------------------
def esc(t):
    return html.escape(t, quote=False)

def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t

def md_section(md, heading):
    i = md.index(heading)
    j = md.find("\n## ", i + len(heading))
    return md[i + len(heading): j if j != -1 else None]

# Persona
psec = md_section(persona_md, "## Persona: Dr. Maya, family physician (composite)")
traits = [l[2:] for l in psec.splitlines() if l.startswith("- ")]
persona_note = next(l for l in psec.splitlines() if l.startswith("She is illustrative"))
stage_rows = []
for l in md_section(persona_md, "## The seven stages (shared by every segment)").splitlines():
    if re.match(r"\|\s*\d", l):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        stage_rows.append(dict(n=int(c[0]), stage=c[1], phase=c[2], goal=c[3], voice=c[4].strip('"“”'), pain=c[5], job=c[6]))
assert len(stage_rows) == 7

# Jobs
jobs = []
for m in re.finditer(r"### (J\d) · Stage (\d): ([^.]+)\. \*(.+?)\*\n(.*?)(?=\n### |\n---)", jtbd_md, re.S):
    jid, n, stage, title, body = m.groups()
    story = " ".join(l[2:] for l in body.splitlines() if l.startswith("> "))
    bullets = {}
    for b in re.findall(r"^- \*\*(.+?):\*\* (.+)$", body, re.M):
        bullets[b[0]] = b[1]
    bullets = {k: v[0].upper() + v[1:] for k, v in bullets.items()}
    jobs.append(dict(id=jid.lower(), label=jid, n=int(n), stage=stage, title=title.rstrip("."), story=story, bullets=bullets))
assert len(jobs) == 7, len(jobs)
core = md_section(jtbd_md, "## 2. The core job")
core_story = " ".join(l[2:] for l in core.splitlines() if l.startswith("> "))
core_why = [l[2:] for l in core.splitlines() if l.startswith("- ")]
core_after = [p.strip() for p in core.split("\n\n") if p.strip() and not p.strip().startswith((">", "-", "**Why"))]
what_is = md_section(jtbd_md, "## 1. Purpose")
what_is_items = [l[2:] for l in what_is.splitlines() if l.startswith("- ")]
stake = md_section(jtbd_md, "## 4. Jobs for other stakeholders")
stake_rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in stake.splitlines() if l.startswith("| **")]
needs = [re.sub(r"^\d+\.\s*", "", l) for l in md_section(jtbd_md, "## 5. Underlying needs, across all stages").splitlines() if re.match(r"\d+\.", l)]
caveats = [l[2:] for l in md_section(jtbd_md, "## 6. Evidence caveats").splitlines() if l.startswith("- ")]

# Journey grid from the canvas source
helmet = re.search(r"<helmet>(.*?)</helmet>", map_src, re.S).group(1)
map_css = re.search(r"<style>(.*?)</style>", helmet, re.S).group(1).replace("body{margin:0}", "")
grid = re.search(r'(<div class="jm-grid">.*?\n</div>)\n\n<div style="display: flex; gap: 28px', map_src, re.S).group(1)
legend = re.search(r'\n(<div style="display: flex; gap: 28px.*?</div>)\n</div>\n</x-dc>', map_src, re.S).group(1)
n = iter(STAGES)
grid, count = re.subn(r'<div style="(background: #1F2A30;[^"]*)"><div style="font-size: 12px; color: #C9D3D8">Stage (\d)</div>',
                      lambda m: f'<div class="jm-stage" id="journey-{next(n)}" style="{m.group(1)}"><div style="font-size: 12px; color: #C9D3D8">Stage {m.group(2)}</div>', grid)
assert count == 7, count
grid = build_maps.link_content(grid, "../")
grid = build_maps.add_ids(grid)
# Put Dr. Maya's voice cells in reach of the persona section.
n = iter(STAGES)
grid = re.sub(r'<div class="jm-quote" id="([^"]+)">', lambda m: f'<div class="jm-quote" id="{m.group(1)}" data-stage="{next(n)}">', grid)

# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
def anchor(hid, label):
    return f'<a class="h-anchor" href="#{hid}" aria-label="Link to {esc(label)}">#</a>'

def stage_link(i, text=None):
    return f'<a href="#journey-{STAGES[i]}">{esc(text or f"Stage {i+1}: {STAGE_NAMES[i]}")}</a>'

AVATAR = ('<svg viewBox="0 0 88 88" role="img" aria-label="Illustrated initial M for Dr. Maya. No photo: she is a composite.">'
          '<circle cx="44" cy="44" r="44" fill="#F0E0B0"/>'
          '<text x="44" y="58" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="900" font-size="40" fill="#1B2D5B">M</text></svg>')

voice_rows = "".join(
    f'<tr id="persona-{STAGES[i]}"><th scope="row">{stage_link(i, str(r["n"]) + " " + r["stage"])}</th>'
    f'<td class="voice">“{esc(r["voice"])}”</td><td>{inline(r["goal"])}</td><td>{inline(r["pain"])}</td></tr>'
    for i, r in enumerate(stage_rows))

persona_html = f"""
<section class="block anchor-target" id="persona" aria-labelledby="persona-h">
  <div class="wrap">
    <div class="sec-head">
      <div><h2 id="persona-h">Healthcare persona {anchor("persona", "Healthcare persona")}</h2></div>
    </div>
    <div class="tile persona-card">
      <div class="persona">
        <div class="avatar">{AVATAR}</div>
        <div>
          <h3>Dr. Maya, family physician <span class="badge">Composite</span></h3>
          <ul class="small">{"".join(f"<li>{inline(t)}</li>" for t in traits)}</ul>
          <p class="small muted">{inline(persona_note.split(" Never")[0])} Her voice lines below are illustrative, not interview quotes.</p>
        </div>
      </div>
    </div>
    <h3 class="sub" id="persona-voice">Her voice, goal and pain point at each stage</h3>
    <p class="scroll-hint" aria-hidden="true">Scroll the table sideways to see every column.</p>
    <div class="table-scroll" role="region" aria-labelledby="persona-voice" tabindex="0">
      <table class="plain voice-table">
        <thead><tr><th scope="col">Stage</th><th scope="col">Her voice (illustrative)</th><th scope="col">Her goal</th><th scope="col">Pain point</th></tr></thead>
        <tbody>{voice_rows}</tbody>
      </table>
    </div>
  </div>
</section>"""

journey_html = f"""
<section class="block anchor-target" id="journey" aria-labelledby="journey-h">
  <div class="wrap">
    <div class="sec-head">
      <div><h2 id="journey-h">Journey {anchor("journey", "Journey")}</h2></div>
      <p>How curated examples help Dr. Maya: from noticing climate in the clinic to sharing what works. In the “Curated content's job” row, each named example opens its Content Example prototype.</p>
    </div>
    <p class="scroll-hint rj-hint">The map is wider than the screen. Scroll it sideways to see all seven stages.</p>
  </div>
  <div class="rj-scroll" role="region" aria-label="Journey map, scrolls sideways" tabindex="0">
    <div class="rj-map">
{grid}
<div class="rj-legend">{legend}</div>
    </div>
  </div>
  <div class="wrap">
    <p class="small muted rj-more">Also as full-size maps: <a href="../maps/journey.html">journey map</a> and <a href="../maps/touchpoints.html">touchpoint map</a>.</p>
  </div>
</section>"""

def cite(src, page, text):
    short, _, _ = REPORTS[src]
    where = f"{short}, PDF p. {page}" if page else short
    href = "../audit/index.html" if src == AUDIT else f"#src-{src}"
    return f'<li>{inline(text)} <span class="cite">(<a href="{href}">{esc(where)}</a>)</span></li>'

def job_card(j):
    i = j["n"] - 1
    r = stage_rows[i]
    research = RESEARCH[j["id"]]
    gap = NO_RESEARCH.get(j["id"])
    res_html = ""
    if research:
        res_html += '<ul class="cites">' + "".join(cite(*c) for c in research) + "</ul>"
    if gap:
        res_html += f'<p class="gap"><span class="gap-tag">Gap</span> {esc(gap)}</p>'
    b = j["bullets"]
    return f"""
<article class="tile job anchor-target" id="{j["id"]}" aria-labelledby="{j["id"]}-h">
  <p class="eyebrow">{j["label"]} · Stage {j["n"]}: {esc(j["stage"])}</p>
  <h3 id="{j["id"]}-h">{esc(j["title"])} {anchor(j["id"], j["label"])}</h3>
  <blockquote class="story">{inline(j["story"])}</blockquote>
  <dl class="jobfacts">
    <dt>Practical</dt><dd>{inline(b.get("Practical", ""))}</dd>
    <dt>Emotional and social</dt><dd>{inline(b.get("Emotional/social", ""))}</dd>
  </dl>
  <div class="from">
    <p class="from-h">Where this job comes from</p>
    <dl class="from-grid">
      <dt><span class="src src-journey">Journey</span></dt>
      <dd>{stage_link(i)}. Pain point: {inline(r["pain"])}. Curated content's job: {inline(r["job"])}.</dd>
      <dt><span class="src src-persona">Persona</span></dt>
      <dd><a href="#persona-{STAGES[i]}">Dr. Maya</a>: “{esc(r["voice"])}” Her goal: {inline(r["goal"][0].lower() + r["goal"][1:])}.</dd>
      <dt><span class="src src-research">Research</span></dt>
      <dd>{res_html}</dd>
    </dl>
  </div>
</article>"""

stake_html = "".join(f'<tr><th scope="row">{inline(a)}</th><td>{inline(b)}</td></tr>' for a, b in stake_rows)
jobs_html = f"""
<section class="block anchor-target" id="jobs-to-be-done" aria-labelledby="jtbd-h">
  <div class="wrap">
    <div class="sec-head">
      <div><h2 id="jtbd-h">Jobs to be done {anchor("jobs-to-be-done", "Jobs to be done")}</h2></div>
      <p>Seven jobs, one per journey stage. Each shows where it comes from: the <span class="src src-journey">Journey</span> stage, Dr. Maya's <span class="src src-persona">Persona</span> voice, and the <span class="src src-research">Research</span> in TCC's and AU's landscape reports.</p>
    </div>
    <div class="grid g2 core">
      <div class="tile">
        <p class="eyebrow">The core job</p>
        <blockquote class="story">{inline(core_story)}</blockquote>
        <p class="small">{inline(core_after[-1]) if core_after else ""}</p>
      </div>
      <div class="tile">
        <p class="eyebrow">Why examples, rather than training</p>
        <ul class="small prose">{"".join(f"<li>{inline(x)}</li>" for x in core_why)}</ul>
        <p class="small muted">A Content Example is any curated piece of real climate communication TCC shows a messenger: {inline("; ".join(x[0].lower() + x[1:] for x in what_is_items))}.</p>
      </div>
    </div>
    <nav class="jump" aria-label="Jump to a job">
      {"".join(f'<a class="btn btn-ghost" href="#{j["id"]}">{j["label"]} {esc(j["stage"])}</a>' for j in jobs)}
    </nav>
    <div class="jobs">{"".join(job_card(j) for j in jobs)}</div>

    <div class="grid g2" style="margin-top:32px">
      <div class="tile" id="jtbd-stakeholders">
        <h3>Jobs for other stakeholders</h3>
        <div class="table-scroll" role="region" aria-label="Jobs for other stakeholders" tabindex="0">
          <table class="plain"><thead><tr><th scope="col">Stakeholder</th><th scope="col">Job the Content Example does for them</th></tr></thead><tbody>{stake_html}</tbody></table>
        </div>
      </div>
      <div class="tile" id="jtbd-needs">
        <h3>Underlying needs, across all stages</h3>
        <ol class="small prose">{"".join(f"<li>{inline(x)}</li>" for x in needs)}</ol>
      </div>
    </div>
    <div class="tile caveats" id="evidence-caveats">
      <h3>Evidence caveats</h3>
      <ul class="small prose">{"".join(f"<li>{inline(x)}</li>" for x in caveats)}</ul>
    </div>
    <div class="tile" id="sources">
      <h3>Sources</h3>
      <ul class="small prose sources">
        <li id="src-tcc"><b>TCC insights report.</b> {esc(REPORTS[TCC][1])} <a href="{REPORTS[TCC][2]}">talkingclimate.com</a></li>
        <li id="src-au"><b>AU research report.</b> {esc(REPORTS[AU][1])} <a href="{REPORTS[AU][2]}">doi.org/10.57912/32957927</a></li>
        <li><b>Example audit.</b> {esc(REPORTS[AUDIT][1])} <a href="../audit/index.html">Open the audit</a></li>
      </ul>
      <p class="small muted">Page numbers are PDF pages. Survey figures are from the TCC/AU research; view counts are from our audit. The TCC and AU reports round some figures differently (for example, LinkedIn use 87% vs. 83%).</p>
    </div>
  </div>
</section>"""

LOCAL_CSS = """
/* LOCAL: research page additions. TCC tokens come from assets/tcc.css. */
h2 .h-anchor,h3 .h-anchor{font-size:.7em;font-weight:700;text-decoration:none;color:var(--tcc-cerulean-ink);opacity:0;margin-left:.2em;padding:0 .15em;transition:opacity .15s}
h2:hover .h-anchor,h3:hover .h-anchor,.h-anchor:focus-visible{opacity:1}
@media (hover:none){.h-anchor{opacity:.55}}
h2 .h-anchor{display:inline}
.badge{display:inline-block;vertical-align:middle;font:700 12px/1 var(--tcc-font-ui);letter-spacing:.06em;text-transform:uppercase;color:var(--tcc-navy);background:var(--tcc-cream);border-radius:999px;padding:5px 10px;margin-left:6px}
.persona-card{margin-bottom:28px}
.persona h3{margin:0 0 6px}
.voice-table{min-width:760px}
.voice-table td.voice{font-style:italic;color:var(--tcc-navy);white-space:nowrap}
.voice-table tr:target{background:var(--tcc-sky)}
.anchor-target{scroll-margin-top:16px}
.jump .btn{min-height:40px;padding:8px 14px;font-size:14px}
.rj-hint{display:block;margin:16px 0 20px}
.rj-scroll{overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;background:#F6F5F1;border-top:1px solid #DDE2DF;border-bottom:1px solid #DDE2DF}
.rj-scroll:focus-visible{outline:3px solid #0F5F59;outline-offset:-3px}
.rj-map{width:2000px;margin:0 auto;padding:24px;font-family:Inter,system-ui,sans-serif;color:#1F2A30}
.rj-map .jm-grid{grid-template-columns:180px repeat(7,minmax(0,1fr))}
.rj-map .jm-stage{scroll-margin:16px 24px 16px 188px}
/* Row titles stay put while the stages scroll sideways. The 8px spread in the
   page color hides cells sliding through the gaps between titles. */
.rj-map .jm-label,.rj-map .jm-grid > div:empty{position:sticky;left:0;z-index:2;box-shadow:0 0 0 8px #F6F5F1}
.rj-map .jm-grid > div:empty{background:#F6F5F1}
@media (max-width:640px){.rj-map .jm-grid{grid-template-columns:124px repeat(7,minmax(0,1fr))}.rj-map .jm-label{padding:12px;font-size:15px}.rj-map .jm-stage{scroll-margin-left:132px}}
.rj-map .jm-stage:target{outline:4px solid var(--tcc-pumpkin);outline-offset:2px}
.rj-map .jm-link{color:#0B3B37;text-decoration:underline;text-decoration-color:#0F5F59;text-underline-offset:3px}
.rj-map .jm-link:hover{color:#0F5F59}
.rj-map .jm-soon small{display:inline-block;font-size:11px;font-weight:600;color:#45535A;border:1px dashed #9AA5AA;border-radius:999px;padding:1px 8px}
.rj-legend > div{flex-wrap:wrap;margin-top:20px}
.rj-more{margin-top:12px}
.core{margin-bottom:24px}
.story{margin:8px 0 16px;padding:12px 16px;border-left:4px solid var(--tcc-pumpkin);background:var(--tcc-linen);border-radius:0 8px 8px 0;font-size:17px;line-height:1.5;color:var(--tcc-navy)}
.jobs{display:grid;gap:24px;margin-top:24px}
.job h3{font-size:clamp(22px,3vw,28px);margin:0 0 4px}
.job:target{box-shadow:0 0 0 4px var(--tcc-pumpkin),var(--tcc-shadow)}
.jobfacts{display:grid;grid-template-columns:max-content 1fr;gap:6px 16px;margin:0 0 16px;font-size:15px}
.jobfacts dt{font-weight:700;color:var(--tcc-navy)}
.jobfacts dd{margin:0}
.from{border-top:1px solid var(--tcc-sand);padding-top:14px}
.from-h{font:700 13px/1.3 var(--tcc-font-ui);letter-spacing:.1em;text-transform:uppercase;color:var(--tcc-muted);margin:0 0 10px}
.from-grid{display:grid;grid-template-columns:110px 1fr;gap:12px 16px;margin:0;font-size:15px;line-height:1.55}
.from-grid dd{margin:0}
@media (max-width:560px){.from-grid,.jobfacts{grid-template-columns:1fr;gap:4px}.from-grid dd{margin-bottom:10px}}
.src{display:inline-block;font:700 12px/1 var(--tcc-font-ui);letter-spacing:.04em;border-radius:999px;padding:5px 10px;white-space:nowrap}
.src-journey{background:#E7F3F1;color:#0B3B37}
.src-persona{background:var(--tcc-cream);color:var(--tcc-navy)}
.src-research{background:var(--tcc-mist);color:var(--tcc-navy)}
.cites{margin:0;padding-left:18px}
.cites li{margin:0 0 6px}
.cite{color:var(--tcc-muted);font-size:14px;white-space:nowrap}
.gap{margin:6px 0 0;color:var(--tcc-slate)}
.gap-tag{display:inline-block;font:700 11px/1 var(--tcc-font-ui);letter-spacing:.06em;text-transform:uppercase;color:var(--local-bad);border:1px solid var(--local-bad);border-radius:999px;padding:3px 8px;margin-right:4px}
.caveats,#sources{margin-top:24px}
.sources li{margin-bottom:8px}
.sources li:target{background:var(--tcc-sky)}
"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Messenger-centered design · Health professionals pilot</title>
<meta name="robots" content="noindex">
<meta name="description" content="Healthcare persona, journey and jobs to be done for TCC's curated content pilot.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="../assets/tcc.css">
<link rel="stylesheet" href="../assets/overnote-theme.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Space+Grotesk:wght@500;600;700&amp;display=swap" rel="stylesheet">
<style>
/* Journey map palette, from reference/maps/Main.dc.html. Used only inside the map. */
{map_css.strip()}
{LOCAL_CSS}</style>
<!-- Generated by tools/build_research.py from reference/persona-and-stages.md,
     reference/maps/Main.dc.html and reference/requirements/content-example-jtbd.md. -->
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<main id="main">
<section class="block" id="top" aria-labelledby="top-h">
  <div class="wrap">
    <p class="eyebrow">TCC curated content</p>
    <h1 id="top-h" style="font-weight:900;font-size:clamp(32px,5vw,52px);margin:0 0 16px">Messenger-centered design</h1>
    <div class="prose">
      <p><strong>Where does curated content support the messenger's journey? Nearly every stage.</strong> But to help, it has to show up in touchpoints TCC owns or in tools messengers already use every day.</p>
      <p>A <strong>healthcare persona</strong> is the basis of the proposed journey below. The <strong>journey</strong> shows the role of example content at each stage.</p>
      <p>Requirements for example content are translated into <strong>Jobs to be done</strong>. Each job links back to the stage, the persona line, and the research it comes from.</p>
    </div>
    <nav class="jump" aria-label="Jump to">
      <a class="btn btn-ghost" href="#persona">Healthcare persona</a>
      <a class="btn btn-ghost" href="#journey">Journey</a>
      <a class="btn btn-ghost" href="#jobs-to-be-done">Jobs to be done</a>
    </nav>
  </div>
</section>
{persona_html}
{journey_html}
{jobs_html}
</main>
<footer class="site on-navy">
  <div class="wrap">
    <img class="logo" src="../assets/tcc-logo-white.png" width="618" height="432" alt="Talking Climate Collaborative">
    <div>
      <p>Sources: TCC and American University landscape assessments (2026); TCC curated content segment audit (Nov 2026).</p>
      <p>Dr. Maya is a composite. Draft for review, Nov 2026.</p>
    </div>
  </div>
</footer>
<!-- Overnote review layer. Needs HTTP; see js/annotate.js. -->
<script type="module" src="../js/annotate.js"></script>
</body>
</html>
"""
out = root / "research"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(page)
print("wrote research/index.html", len(page))
