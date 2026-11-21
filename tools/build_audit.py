"""Render reference/audit.md as audit/index.html using TCC styles."""
import re, sys, html, pathlib

root = pathlib.Path(sys.argv[1])
md = (root / "reference" / "audit.md").read_text()

NEWTAB = '<span class="sr-only"> (opens in a new tab)</span>'

def inline(t):
    t = t.replace("\\~", "~")
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}{NEWTAB}</a>', t)
    return t

def section(title_start, next_title_prefix="## "):
    i = md.index(title_start)
    j = md.find("\n" + next_title_prefix, i + len(title_start))
    return md[i + len(title_start): j if j != -1 else None]

def tables(sec):
    out = []
    for block in re.findall(r"((?:^\|.*\|\s*$\n?)+)", sec, re.M):
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in block.strip().splitlines()]
        out.append((rows[0], rows[2:]))
    return out

def bullets_after(sec, heading):
    i = sec.index(heading) + len(heading)
    rest = sec[i:].lstrip("\n")
    items = []
    for line in rest.splitlines():
        if line.startswith("- "):
            items.append(line[2:])
        elif line.strip() == "" and items:
            break
        elif line.strip() and not line.startswith("- "):
            break
    return items

def first_paras(sec, n):
    paras = [p.strip() for p in sec.strip().split("\n\n") if p.strip() and not p.strip().startswith("|")]
    return paras[:n]

PRIN = ["Personal", "Accessible", "Empowering", "Doable", "Collective", "Normal", "Trustworthy", "For Everyone"]
GRADE = {"+": ("g-strong", "+", "strong"), "~": ("g-mixed", "~", "mixed"),
         "–": ("g-weak", "–", "weak"), "·": ("g-na", "·", "not in play"),
         "": ("g-blank", "—", "not graded")}
ICON = {
    "Good example": ("v-good", '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg>'),
    "So-so": ("v-soso", '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14"/></svg>'),
    "Not yet usable": ("v-not", '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><circle cx="12" cy="12" r="7"/></svg>'),
}

def verdict(v):
    cls, icon = ICON[v]
    return f'<span class="verdict {cls}">{icon}{v}</span>'

def audit_table(head, rows, caption, tid):
    ths = ['<th scope="col">Example</th>', '<th scope="col">Content type</th>',
           '<th scope="col">Messenger</th>', '<th scope="col">Date</th>']
    ths += [f'<th scope="col" class="p"><abbr title="{p}">P{i+1}</abbr><span class="sr-only"> {p}</span></th>' for i, p in enumerate(PRIN)]
    ths.append('<th scope="col">Verdict</th>')
    body = []
    for r in rows:
        ex = r[0]
        m = re.match(r"\[([^\]]+)\]\(([^)]+)\)\s*(\((.+)\))?$", ex)
        if m:
            src = f'<small>{html.escape(m.group(4))}</small>' if m.group(4) else ""
            exh = f'<a href="{m.group(2)}" target="_blank" rel="noopener">{inline(m.group(1))}{NEWTAB}</a>{src}'
        else:
            exh = inline(ex)
        cells = [f'<th scope="row" class="ex" style="font-weight:400">{exh}</th>',
                 f'<td class="type">{inline(r[1])}</td>', f'<td class="who">{inline(r[2])}</td>',
                 f'<td class="date">{inline(r[3])}</td>']
        for g in r[4:12]:
            g = g.replace("\\~", "~").strip()
            cls, sym, label = GRADE[g]
            cells.append(f'<td class="g {cls}"><span aria-hidden="true">{sym}</span><span class="sr-only">{label}</span></td>')
        cells.append(f"<td>{verdict(r[12])}</td>")
        rid = "ex-" + re.sub(r"[^a-z0-9]+", "-", (m.group(1) if m else ex).lower()).strip("-")[:40]
        body.append(f'<tr id="{rid}">' + "".join(cells) + "</tr>")
    return f"""<p class="scroll-hint" aria-hidden="true">Scroll the table sideways to see every principle.</p>
<div class="table-scroll" role="region" aria-labelledby="{tid}" tabindex="0">
<table class="audit">
<caption class="sr-only" id="{tid}">{caption}</caption>
<thead><tr>{''.join(ths)}</tr></thead>
<tbody>
{chr(10).join(body)}
</tbody>
</table>
</div>"""

def ul(items, cls="notes"):
    return f'<ul class="{cls}">' + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>"

def segment(heading, sid, eyebrow, h2, caption):
    sec = section(heading)
    paras = first_paras(sec, 2)
    (head, rows), = tables(sec)
    land = bullets_after(sec, "**What makes each one land or miss:**")
    social = bullets_after(sec, "**Added from social media:**")
    return f"""
<section class="block anchor-target" id="{sid}" aria-labelledby="{sid}-h">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">{eyebrow}</p><h2 id="{sid}-h">{h2}</h2></div>
      <p>{inline(paras[0])}</p>
    </div>
    <p class="prose small">{inline(paras[1])}</p>
    {audit_table(head, rows, caption, sid + "-caption")}
    <h3 class="sub">What makes each one land or miss</h3>
    <div class="notes-wrap">{ul(land)}</div>
    <h3 class="sub">Added from social media</h3>
    <div class="notes-wrap">{ul(social)}</div>
  </div>
</section>"""

# ---- purpose
purpose = section("## Purpose and method")
pparas = [p.strip() for p in purpose.strip().split("\n\n")]
intro, keyline = pparas[0], pparas[1]
verdict_line, screen_line, principles_line = pparas[3], pparas[4], pparas[5]

# ---- patterns
pat = section("## Patterns and what they mean for the platform")
pat_intro = first_paras(pat, 1)[0]
(phead, prows), = tables(pat)
needs1 = bullets_after(pat, "Two platform needs show up already:")
needs2 = bullets_after(pat, "Social media adds two more needs:")
pt = "<thead><tr>" + "".join(f'<th scope="col">{inline(h)}</th>' for h in phead) + "</tr></thead><tbody>"
for r in prows:
    pt += f'<tr><th scope="row">{inline(r[0])}</th>' + "".join(f"<td>{inline(c)}</td>" for c in r[1:]) + "</tr>"
pt += "</tbody>"

nexts = [l[6:] for l in section("## Next steps").splitlines() if l.startswith("- [ ] ")]
sources = [l[2:] for l in section("## Sources").splitlines() if l.startswith("- ")]

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Example audit · Health professionals pilot</title>
<meta name="robots" content="noindex">
<meta name="description" content="Health and athlete examples graded against Rare's 8 Principles.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="../assets/tcc.css">
<!-- Generated from reference/audit.md (Nov 6, 2026). -->
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<main id="main">
<section class="block" id="purpose" aria-labelledby="purpose-h">
  <div class="wrap">
    <p class="eyebrow">TCC curated content</p>
    <h1 style="font-weight:900;font-size:clamp(32px,5vw,52px);margin:0 0 20px">Content example audit</h1>
    <div class="prose">
      <p>{inline(intro)}</p>
      <p>{inline(screen_line)}</p>
    </div>
    <nav class="jump" aria-label="Jump to">
      <a class="btn btn-ghost" href="#health">Health professionals</a>
      <a class="btn btn-ghost" href="#athletes">Outdoor and athlete voices</a>
      <a class="btn btn-ghost" href="#patterns">Patterns</a>
    </nav>

    <div class="grid g2" style="margin-top:32px">
      <div class="tile">
        <h3 id="key-h">Grading key</h3>
        <p class="small">Each piece gets one mark per principle.</p>
        <ul class="key" aria-labelledby="key-h">
          <li><span class="g g-strong"><span aria-hidden="true">+</span></span><span><b>Strong.</b> Clearly does what the principle asks.</span></li>
          <li><span class="g g-mixed"><span aria-hidden="true">~</span></span><span><b>Mixed.</b> Partly there, or one fixable miss.</span></li>
          <li><span class="g g-weak"><span aria-hidden="true">–</span></span><span><b>Weak.</b> Works against the principle.</span></li>
          <li><span class="g g-na"><span aria-hidden="true">·</span></span><span><b>Not in play</b> for this piece.</span></li>
        </ul>
      </div>
      <div class="tile">
        <h3 id="verdict-h">Verdicts</h3>
        <ul class="key" aria-labelledby="verdict-h" style="grid-template-columns:1fr">
          <li>{verdict("Good example")}<span>Mostly +, no –.</span></li>
          <li>{verdict("So-so")}<span>Useful to teach a fix.</span></li>
          <li>{verdict("Not yet usable")}<span>Too thin to grade.</span></li>
        </ul>
        <h3 class="sub" style="margin-top:20px">The 8 Principles</h3>
        <p class="small" style="margin:0">P1 Personal · P2 Accessible · P3 Empowering · P4 Doable · P5 Collective · P6 Normal · P7 Trustworthy · P8 For Everyone</p>
      </div>
    </div>
  </div>
</section>
{segment("## Primary segment: health professionals", "health", "Primary segment", "Health professionals", "Health professionals: examples graded against the 8 Principles")}
{segment("## Flex segment: outdoor and athlete voices", "athletes", "Flex segment", "Outdoor and athlete voices", "Outdoor and athlete voices: examples graded against the 8 Principles")}

<section class="block anchor-target" id="patterns" aria-labelledby="patterns-h">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Across both segments</p><h2 id="patterns-h">Patterns and what they mean for the platform</h2></div>
      <p>{inline(pat_intro)}</p>
    </div>
    <p class="scroll-hint" aria-hidden="true">Scroll the table sideways to see every column.</p>
    <div class="table-scroll" role="region" aria-labelledby="patterns-caption" tabindex="0">
      <table class="plain">
        <caption class="sr-only" id="patterns-caption">Patterns by segment and what they mean for the platform</caption>
        {pt}
      </table>
    </div>
    <div class="grid g2">
      <div class="tile" id="needs-now"><h3>Two platform needs already</h3>{ul(needs1, "notes")}</div>
      <div class="tile" id="needs-social"><h3>Two more from social media</h3>{ul(needs2, "notes")}</div>
    </div>
  </div>
</section>

<section class="block" id="next" aria-labelledby="next-h">
  <div class="wrap">
    <div class="grid g2">
      <div class="tile"><h3 id="next-h">Next steps</h3><ul class="small prose">{"".join(f"<li>{inline(n)}</li>" for n in nexts)}</ul></div>
      <div class="tile"><h3>Sources</h3><ul class="small prose">{"".join(f"<li>{inline(s)}</li>" for s in sources)}</ul></div>
    </div>
  </div>
</section>
</main>

<footer class="site on-navy">
  <div class="wrap">
    <img class="logo" src="../assets/tcc-logo-white.png" width="618" height="432" alt="Talking Climate Collaborative">
    <div>
      <p>Source: TCC curated content segment audit (Nov 2026), graded against Rare's 8 Principles.</p>
      <p>A first-pass screen. Each piece needs a full read before it goes into the library.</p>
    </div>
  </div>
</footer>
<!-- Overnote review layer, loaded only with ?review=1. See js/annotate.js. -->
<script type="module" src="../js/annotate.js"></script>
</body>
</html>
"""
(root / "audit" / "index.html").write_text(page)
print("wrote audit", len(page))
