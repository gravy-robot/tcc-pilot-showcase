// Shared Overnote setup: review comments and sticky notes on showcase pages.
// Spec: overnote/docs/OVERNOTE_REQUIREMENT.md. Don't edit overnote.js; replace it to upgrade.
//
// Load once, just before </body>, with a path relative to the page:
//   index.html              <script type="module" src="js/annotate.js"></script>
//   maps/, audit/, mockups/ <script type="module" src="../js/annotate.js"></script>
// Relative (not root-relative) so it works on any host or subpath.
// ES modules don't load from file://. Serve over HTTP to annotate.
// From file:// the page still works, just without the toolbar.
import Overnote from './overnote.js';

const overnote = new Overnote({
  author: 'Reviewer',
  storageKey: `overnote:${location.pathname}`, // one key per page
  ignore: '.skip, .tcc-banner, .review-export', // stay clickable in Sticky mode
  position: 'bottom-right',
});

overnote.init();
window.overnote = overnote;

/* ---------------------------------------------------------------
   LOCAL: "Export notes" button (not part of Overnote).
   Downloads one JSON file with the saved notes from every page of
   the showcase in this browser. Each entry in `pages` is a normal
   Overnote export, so it can go back in with importAnnotations().
   Sits bottom-left so it never covers Overnote's toolbar, and below
   Overnote's z-index (reserved range ~2147483000).
   --------------------------------------------------------------- */
const PREFIX = 'overnote:';

function savedPages() {
  const pages = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (!key || !key.startsWith(PREFIX)) continue;
      const data = JSON.parse(localStorage.getItem(key) || 'null');
      if (data && Array.isArray(data.annotations) && data.annotations.length) {
        pages.push({ path: key.slice(PREFIX.length), ...data });
      }
    }
  } catch { /* storage blocked: export what this page has */ }
  // Make sure the current page reflects what's on screen right now.
  const here = overnote.exportAnnotations();
  const i = pages.findIndex((p) => p.path === location.pathname);
  if (here.annotations.length) {
    const entry = { path: location.pathname, ...here };
    if (i === -1) pages.push(entry); else pages[i] = entry;
  } else if (i !== -1) {
    pages.splice(i, 1);
  }
  return pages.sort((a, b) => a.path.localeCompare(b.path));
}

function countNotes(pages) {
  return pages.reduce((n, p) => n + p.annotations.length, 0);
}

const style = document.createElement('style');
style.id = 'review-export-styles';
style.textContent = `
.review-export{position:fixed;left:16px;bottom:16px;z-index:2147482000;display:inline-flex;align-items:center;gap:8px;
  font:700 14px/1 "Ubuntu",system-ui,sans-serif;color:#FFFFFF;background:#1B2D5B;border:0;border-radius:999px;
  padding:11px 16px;box-shadow:0 1px 2px rgba(27,45,91,.12),0 8px 24px rgba(27,45,91,.18);cursor:pointer}
.review-export:hover{background:#2C3D6B}
.review-export:focus-visible{outline:3px solid #33C6F5;outline-offset:3px}
.review-export[aria-disabled="true"]{background:#5E6380;cursor:default}
.review-export b{display:inline-grid;place-items:center;min-width:22px;height:22px;padding:0 6px;border-radius:999px;
  background:#F28030;color:#1B2D5B;font-size:12px}
@media (max-width:480px){.review-export .label-long{display:none}}
@media print{.review-export{display:none}}`;
document.head.appendChild(style);

const button = document.createElement('button');
button.type = 'button';
button.className = 'review-export';
button.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"
  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>
  <span>Export<span class="label-long"> notes</span></span><b>0</b>`;
document.body.appendChild(button);

function update() {
  const pages = savedPages();
  const n = countNotes(pages);
  button.querySelector('b').textContent = String(n);
  button.setAttribute('aria-disabled', n ? 'false' : 'true');
  button.setAttribute('aria-label', n
    ? `Export ${n} note${n === 1 ? '' : 's'} from ${pages.length} page${pages.length === 1 ? '' : 's'} as a JSON file`
    : 'Export notes. No notes yet');
  button.title = n ? 'Download every page\'s notes as one file' : 'No notes yet';
}

button.addEventListener('click', () => {
  const pages = savedPages();
  if (!countNotes(pages)) return;
  const bundle = {
    format: 'overnote-bundle',
    version: 1,
    site: 'TCC Curated Content: Health Professionals Pilot',
    exportedAt: new Date().toISOString(),
    pages,
  };
  const blob = new Blob([JSON.stringify(bundle, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `tcc-pilot-notes-${bundle.exportedAt.slice(0, 10)}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

overnote.on('change', update);
window.addEventListener('storage', update); // notes added in another tab
update();
