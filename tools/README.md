# Generators for the reference pages

The site has no build step. These scripts write the static pages from the
sources. Re-run them only if the sources change.

```bash
python3 tools/build_maps.py .              # reference/maps/*.dc.html -> maps/*.html
python3 tools/build_audit.py .             # reference/audit.md       -> audit/index.html
python3 tools/build_content_example.py .   # reference/audit.md       -> prototypes/content-example/
```

Run from the site root. Each overwrites only its own output pages.
`build_content_example.py` writes `data/examples.json`, the three prototype
models (`stage/`, `canvas/`, `spec/`) and the compare page; its CSS, script
and README are hand-written. See `prototypes/content-example/README.md`.

`build_maps.py` turns each pilot card's "Coming next" label into a link once the matching
file exists in `mockups/`.
