# Generators for the reference pages

The site has no build step. These scripts write the static pages from the
sources. Re-run them only if the sources change.

```bash
python3 tools/build_maps.py .              # reference/maps/*.dc.html -> maps/*.html
python3 tools/build_audit.py .             # reference/audit.md       -> audit/index.html
python3 tools/build_content_example.py .   # reference/audit.md       -> prototypes/content-example/
python3 tools/build_research.py .          # persona, journey, jobs   -> research/index.html
```

Run `build_content_example.py` before `build_maps.py`, `build_research.py` and
`build_audit.py`: the journey's "Curated content's job" row links each named piece to its
Stage mockup in `prototypes/content-example/mockups/` (pairs to their page in
`examples/`), and shows "Prototype coming soon" if the page doesn't exist yet. The links
live in `CONTENT_LINKS` in `build_maps.py`. The audit's health rows get a "Mockup" link
from `data/examples.json`.

`build_research.py` builds one standalone page with three linkable sections: `#persona`,
`#journey` and `#jobs-to-be-done`. Each job cites its journey stage, persona line and the
TCC/AU research; the figures and PDF page numbers are in `RESEARCH` at the top of the script.

Run from the site root. Each overwrites only its own output pages.
`build_content_example.py` writes `data/examples.json`, the three prototype
models (`stage/`, `canvas/`, `spec/`) and the compare page; its CSS, script
and README are hand-written. See `prototypes/content-example/README.md`.

`build_maps.py` turns each pilot card's "Coming next" label into a link once the matching
file exists in `mockups/`.
