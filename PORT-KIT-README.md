# TCC pilot showcase: Claude Code port kit

Unzip into a new folder, e.g. `~/Documents/consultancy/code/tcc/tcc-pilot-showcase/`, then open Claude Code there and paste `prompts/00-hub.md`.

## Contents

| Path | What it is | Ported from |
|---|---|---|
| `prompts/00-hub.md` | Claude Code prompt for the hub and reference pages | Written for this kit |
| `reference/audit.md` | Segment example audit, full text with links | Claude Doc "TCC Curated Content: Segment Example Audit" (Markdown export, Nov 6, 2026) |
| `reference/maps/Main.dc.html` | Journey map source | Design canvas "TCC Health Professionals Journey & Touchpoints" |
| `reference/maps/Touchpoints.dc.html` | Touchpoint map source, four pilot tags | Same canvas (includes your latest edits) |
| `reference/maps/canvas.json` | Canvas layout, for reference only | Same canvas |
| `reference/persona-and-stages.md` | Dr. Maya, the seven stages, lanes, pilot loop | Extracted from the maps |
| `reference/research-facts.md` | Approved stats and how to use them | TCC/AU landscape assessments and the audit |
| `reference/principles/1–8` | Rare's 8 Principles | Speak Sustainability skill |
| `reference/requirements/01-tcc-social-post.md` | Agreed spec for mockup 1 | This chat |
| `reference/source-docs/` | Project narrative, TCC and AU landscape PDFs | Claude Project files |
| `reference/parked/gemini-creator-tools-note.txt` | Notion/Airtable template idea, parked | Your attachment |

Not included, already on your computer: the TCC design system at `/Users/brandonschauer/Documents/consultancy/code/tcc/design-system`.

Optional: export PNGs of the two maps from the canvas (Share › Export) into `reference/maps/` if you want Claude Code to compare its rebuild against the original visually.

## Added Nov 9, 2026: Content Example prototypes

| Path | What it is |
|---|---|
| `reference/requirements/content-example-jtbd.md` | Jobs to be done (J1–J7) for a Content Example |
| `reference/requirements/content-example-requirements.md` | Component requirements v3, traced to J1–J7, with W3C Web Sustainability Guidelines alignment |
| `prompts/01-content-example-prototypes.md` | Claude Code prompt: generator script plus Stage, Canvas and requirements-only prototypes |
| `tools/push-to-github.sh` | Commits the site and pushes it to a private repo in the gravy-robot GitHub organization |
