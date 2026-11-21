# Content Example prototypes

Three static prototypes of the Content Example player, built to compare presentation models with clinicians before choosing one (requirements section 7.2, WS-9). All three show the same 18 examples from the audit, from one dataset and one generator.

Open `index.html` (the compare page) to start.

## Regenerate

From the site root:

```bash
python3 tools/build_content_example.py .
```

Python 3 standard library only. It overwrites only generated files:

- `data/examples.json`
- every `*.html` in `stage/`, `canvas/`, `spec/`, `examples/` and `mockups/` (deleted and rewritten)
- `index.html` (the compare page)
- the weight table between the `weights` markers below

Hand-written, never overwritten: `shared/ce-core.css`, `shared/compare.css`, `shared/ce-enhance.js`, `stage/stage.css`, `canvas/canvas.css`, `spec/spec.css`, `data/schema.md`, and the rest of this README. Curation text (paraphrase, notes, stand-in regions) lives in the `CURATION` table at the top of the generator.

## What's here

```
index.html          compare page: matrix, pairs, weights
data/examples.json  one record per audit example (generated)
data/schema.md      fields used, mapped to requirements section 3
shared/ce-core.css  tokens, fonts, anatomy parts, stand-ins, print, dark mode
shared/ce-enhance.js  the one script (progressive enhancement only)
shared/fonts/       Nunito (variable) and Ubuntu 400/500/700, latin subset woff2, with licences
stage/  canvas/  spec/   per model: index.html (messenger view), curator.html,
                         one page per example, one page per contrast pair
examples/           one stable page per example and pair (21): opens the default
                    model and offers the others; link here from outside
mockups/            standalone Stage page per health piece (8), no navigation,
                    for review with Overnote (?review=1)
```

**Mockups for review:** `mockups/<id>.html` is a standalone Stage page for each health piece in the audit (8), with no banner and no links to the library, other examples, pairs or model pages. Built by `mockup_page()` from the same Stage code, so a change there reaches every mockup. Add `?review=1` to review with Overnote.

**Linking from elsewhere:** use `examples/<id>.html`, not a model's page, so links survive the Stage vs. Canvas decision. `DEFAULT_MODEL` in the generator sets which model it opens first. Add `#pattern` (or `#why`) to land on that section in whichever model opens.

Each model has 2 library pages + 18 detail pages + 3 pair pages = 23 pages, so 69, plus the compare page and 21 per-example pages.

## What each model tests

All three render the same anatomy in the same order (section 5): messenger strip, fit tags, content, why it works, reusable pattern, trust line, actions, connection line. They differ only in layout and in how notes and details are revealed.

| | Model A: Stage | Model B: Canvas | Model C: Requirements only |
|---|---|---|---|
| Metaphor | Video site | Map app | None |
| Content | A dark stage; long formats scroll inside it | Fills the screen; drag, pinch, wheel, +/– and keys to pan and zoom | In the page flow, full length |
| Details | Below the stage on phones, right column on desktop | Floating card (messenger) and a side panel; bottom sheet on phones (collapsed, half, full) | One column, parts numbered 1–8 |
| Overlay notes | Pins on the stage; tap jumps to and highlights the note | Pins open a floating note card with next/previous | Pins jump to a numbered list under the content |
| Pair | Two stages side by side (stacked on phones), comparison table below | Split view with a draggable divider; both canvases zoom together | Stacked, comparison table at the end |
| Library | Thumbnail grid with filter chips | A pannable board, clustered by segment, with a search & filter pill | A single list |
| Questions it answers | Does a familiar layout make fit obvious on a phone? Does video feel natural? Do long docs become a tall scroll? | Does spatial annotation help people see why it works? Do floating panels crowd a phone? Is pan/zoom worth its cost (WSG 3.1)? | Is the plain anatomy enough? What's the weight and robustness floor? |
| Without JavaScript | Works; no instant search | Canvas becomes a scroll area; details follow; no pan/zoom or note cards | Works fully |

Common to all three:

- **"Show why it works"** is a checkbox, off by default (PR-4, WS-2). It shows numbered pins on the stand-in using CSS `:has()`, so it works without JavaScript. Every note is also in a plain list (section 11).
- **Messenger view** (`index.html`) applies rules R2 and R3: only Good examples appear alone, So-so examples appear only inside contrast pairs, Not-yet-usable is hidden. **Curator view** (`curator.html`) shows all 18 with verdicts.
- **Filters** (segment, content type, verdict, topic) are radio groups. CSS `:has()` rules apply them without JavaScript; the script adds text search, a result count, the empty state and shareable URLs (`?topic=heat`).
- **Pair pages print** as a draft precedent sheet (6.7): controls hidden, URLs printed after links.
- **Video**: a static facade with duration and an estimated data size. "Load video from YouTube" swaps in a `youtube-nocookie.com` iframe only on click, with no autoplay. Without JavaScript, the button opens YouTube.

## Rights

We don't have permission to reproduce these works, so nothing from them is copied into the repo: no article text, transcripts, screenshots, photos of people or platform logos. Each original is drawn as an HTML/CSS stand-in of its format, filled with TCC's paraphrase from the audit and, at most, one short quote that the audit already quotes. Each stand-in is labelled "Illustration of the original. View it at [venue] ↗". Messengers get an illustrated initial.

## Weight

Bytes for each page plus every CSS, script and font file it references, with media not loaded. Measured by the generator from files on disk, uncompressed, so real transfers with gzip or Brotli will be smaller. Budgets (WS-11): library ≤ 300 KB, detail ≤ 500 KB.

<!-- weights:start -->
| Model | Library | Detail: article | Detail: video (not loaded) | Pair | Heaviest detail |
|---|---|---|---|---|---|
| Model A: Stage | 162 KB | 145 KB | 145 KB | 153 KB | 145 KB (howard-wildfire-smoke.html) |
| Model B: Canvas | 168 KB | 149 KB | 149 KB | 159 KB | 149 KB (suter-outrider-oped.html) |
| Model C: Requirements only | 160 KB | 141 KB | 141 KB | 135 KB | 141 KB (suter-outrider-oped.html) |
<!-- weights:end -->

About 82 KB of every figure is the four font files, which a browser caches after the first page. Gzipped, a library page's HTML is about 5–7 KB.

## Check results (Nov 11, 2026)

- **Pages:** compare page, each library, two detail pages per model (Lawson video, Seattle op-ed) and one pair per model, at 390 px and 1440 px. Screenshots are in `screenshots/content-example/` (390 px from the in-app browser at 2×; 1440 px from headless Chrome). No page scrolls sideways at 390 px.
- **Links:** all 1,298 internal links and anchors across the 70 pages resolve. All 54 "View original" and stand-in links (18 examples × 3 models) match the audit's URLs.
- **Third parties:** no page has a third-party `src` or stylesheet. In the browser, every page loaded only same-origin files (HTML, two stylesheets, the script where used, four fonts). "Load video" inserts a `youtube-nocookie.com` iframe only on click, with no autoplay.
- **Keyboard (Canvas detail, Howard):** every control is reachable and visible when focused: banner links, the canvas (arrow keys pan, +/– zoom, 0 fits), the stand-in's source link, search pill, Layers, zoom buttons, then the details panel. Pins open a note card that takes focus; Previous/Next work; Escape closes it and returns focus to the pin. Two things to know: pins are hidden until "Why it works pins" is turned on in Layers, and because Layers comes after the canvas in the tab order, you then Shift+Tab back to reach the pins. Pinch and drag have keyboard equivalents; the split divider in pairs takes arrow keys.
- **Dark mode, reduced motion, high contrast, print:** dark mode checked visually on a library page. Reduced motion and high contrast are handled in CSS but weren't tested with the OS settings. Print styles exist for detail and pair pages but weren't printed.

## Known gaps

See `data/schema.md` for every field left `null`. In short: no full text, renders, clinician review, sources cited, captions, reshare or "made with" data. Draft curation (structure, step, topics, place, notes) is labelled on every page. The prototype matrix row "Report or talking-points memo" has no example yet.
