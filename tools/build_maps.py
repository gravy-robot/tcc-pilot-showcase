"""Rebuild the two canvas maps as standalone static HTML.

Keeps every row, column, card and label from reference/maps/*.dc.html,
drops the canvas runtime (support.js, <x-dc>, <helmet>, DCLogic script).
"""
import re, sys, pathlib

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
src = root / "reference" / "maps"
out = root / "maps"

PILOTS = [  # in document order
    ("01-tcc-social-post", "Mockup 1"),
    ("02-health-library", "Mockup 2"),
    ("03-ai-chatbot", "Mockup 3"),
    ("04-maya-linkedin-post", "Mockup 4"),
]

LOCAL_CSS = """
/* ---- Added for the static rebuild (not in the canvas source) ---- */
html{-webkit-text-size-adjust:100%}
body{background:#F6F5F1}
.map-intro{max-width:1200px;margin:0 auto;padding:14px 24px 10px;font:500 14px/1.45 Inter,system-ui,sans-serif;color:#45535A}
@media (max-width:640px){.map-intro{padding:12px 16px 8px}}
.map-scroll{overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch}
.map-scroll:focus-visible{outline:3px solid #0F5F59;outline-offset:-3px}
.map-scroll > div{margin:0 auto}
a:focus-visible{outline:3px solid #0F5F59;outline-offset:2px;border-radius:4px}
.tp-go,.tp-soon{align-self:flex-start;margin-top:6px;font-size:12px;font-weight:600;border-radius:999px;padding:4px 10px}
.tp-go{color:#FFFFFF;background:#0F5F59;text-decoration:none}
.tp-go:hover{background:#0B4743;color:#FFFFFF}
.tp-soon{color:#45535A;background:#F6F5F1;border:1px dashed #9AA5AA}
.jm-link{color:#0B3B37;text-decoration:underline;text-decoration-color:#0F5F59;text-underline-offset:3px}
.jm-link:hover{color:#0F5F59}
.jm-soon small{display:inline-block;font-size:11px;font-weight:600;color:#45535A;border:1px dashed #9AA5AA;border-radius:999px;padding:1px 8px}
"""

# Journey "Curated content's job" row: each named piece links to its stable
# Content Example URL (prototypes/content-example/examples/<id>.html), which
# survives the Stage vs. Canvas choice. A missing target renders "coming soon".
CONTENT_LINKS = [  # (exact text inside <b>, example or pair id, fragment)
    ("Courtney Howard on wildfire smoke", "howard-wildfire-smoke", ""),
    ("Ashley Lawson's heat-dome speech", "lawson-heat-dome-speech", ""),
    ("Lawson vs. the Seattle op-ed", "pair-heat-dome", ""),
    ("Howard vs. Vossler", "pair-smoke-and-heat", ""),
    ("Howard's structure", "howard-wildfire-smoke", "#pattern"),
]
EXAMPLES_DIR = pathlib.Path("prototypes/content-example/examples")

def link_content(body, prefix):
    """prefix: path from the output page to the site root, e.g. '../'."""
    for text, target, frag in CONTENT_LINKS:
        b = f"<b>{text}</b>"
        assert b in body, text
        href = f"{prefix}{EXAMPLES_DIR.as_posix()}/{target}.html{frag}"
        if (root / EXAMPLES_DIR / f"{target}.html").exists():
            rep = f'<a class="jm-link" href="{href}"><b>{text}</b></a>'
        else:
            rep = f'<span class="jm-soon"><b>{text}</b> <small>Prototype coming soon</small></span>'
        body = body.replace(b, rep)
    return body

def slug(t):
    t = re.sub(r"<[^>]+>", "", t).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40]

def add_ids(body):
    """Stable ids so Overnote sticky notes survive layout changes."""
    used, row, col = set(), "header", 0
    def uid(base):
        b, n = base, 2
        while base in used:
            base = f"{b}-{n}"; n += 1
        used.add(base); return base
    def rep(m):
        nonlocal row, col
        cls, rest = m.group(1), m.group(2)
        if cls == "jm-label":
            row, col = slug(rest.split("<small>")[0]), 0
            return f'<div class="{cls}" id="{uid("row-" + row)}"{rest[:0]}'
        if cls in ("jm-cell", "jm-quote", "jm-pain", "jm-ex", "jm-opp"):
            col += 1
            return f'<div class="{cls}" id="{uid(f"{row}-stage-{col}")}"'
        if cls == "tp-lane":
            row, col = slug(rest.split("<small")[0]), 0
            return f'<div class="{cls}" id="{uid("lane-" + row)}"'
        if cls.startswith("tp-col"):
            col += 1
            return f'<div class="{cls}" id="{uid(f"{row}-stage-{col}")}"'
        if cls == "tp-card":
            title = re.search(r"<b>(.*?)</b>", rest)
            return f'<div class="{cls}" id="{uid("tp-" + slug(title.group(1)))}"'
        return m.group(0)
    return re.sub(r'<div class="(jm-label|jm-cell|jm-quote|jm-pain|jm-ex|jm-opp|tp-lane|tp-col [a-z]+|tp-card)"(?=([^\n]*))', rep, body)

def build(name, outname, title, page_name, intro, pilots=False):
    s = (src / name).read_text()
    helmet = re.search(r"<helmet>(.*?)</helmet>", s, re.S).group(1)
    body = re.search(r"</helmet>(.*)</x-dc>", s, re.S).group(1).strip()
    if pilots:
        n = iter(PILOTS)
        def add(m):
            slug, label = next(n)
            mock = root / "mockups" / f"{slug}.html"
            if mock.exists():
                extra = f'<a class="tp-go" href="../mockups/{slug}.html">Open {label.lower()} →</a>'
            else:
                extra = f'<span class="tp-soon">{label} · Coming next</span>'
            return m.group(1) + extra
        body, count = re.subn(
            r'(<span class="tp-pilot">Pilot candidate</span><b>.*?</b><span class="tp-ex">.*?</span>)',
            add, body, flags=re.S)
        assert count == 4, count
    if name == "Main.dc.html":
        body = link_content(body, "../")
    body = add_ids(body)
    helmet = helmet.replace("<style>", "<style>" + LOCAL_CSS, 1) if False else helmet
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="robots" content="noindex">
<!-- Rebuilt from reference/maps/{name} (canvas source). Research artifact:
     keeps its own palette and fonts (Inter, Space Grotesk), not TCC branding. -->
<link rel="stylesheet" href="../assets/banner.css">
<link rel="stylesheet" href="../assets/overnote-theme.css">
{helmet.strip()}
<style>{LOCAL_CSS}</style>
</head>
<body>
<nav class="tcc-banner" aria-label="Where you are">
  <div class="tcc-banner__inner">
    <p class="tcc-banner__trail">
      <span class="tcc-banner__kind">Reference</span>
      <span>{page_name}</span>
    </p>
    <a class="tcc-banner__back" href="../research/index.html#journey">Messenger-centered design →</a>
  </div>
</nav>
<main>
<p class="map-intro">{intro}</p>
<div class="map-scroll" id="{outname.split('.')[0]}-map" role="region" aria-label="{page_name}, scrolls sideways" tabindex="0">
{body}
</div>
</main>
<!-- Overnote review layer. Needs HTTP; see js/annotate.js. -->
<script type="module" src="../js/annotate.js"></script>
</body>
</html>
"""
    (out / outname).write_text(html)
    print("wrote", outname, len(html))

if __name__ == "__main__":
    build("Main.dc.html", "journey.html", "Journey map · Health professionals",
          "Journey map",
          "The full map is 2,480 pixels wide. Scroll sideways to see all seven stages.")
    build("Touchpoints.dc.html", "touchpoints.html", "Touchpoint map · Health professionals",
          "Touchpoint map",
          "The full map is 2,480 pixels wide. Scroll sideways to see all seven stages. The four pilot candidates link to their mockups when they are ready.",
          pilots=True)
