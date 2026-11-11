/* Stage tabs on the hub (LOCAL, not in the design system).
   Turns the stage rail (anchor links) and its panels into ARIA tabs:
   one stage's card shows at a time, at full width.
   - Click or tap a stage, or use Left/Right, Home/End on the rail.
   - "Next in the loop" links (data-stage-link) switch tabs too.
   - A #stage-n hash in the URL opens that stage. Default: stage 1.
   Without JS, the rail stays a list of jump links and every panel shows.
   Classic script (not a module), so it also runs from file://. */
(function () {
  var root = document.getElementById('stage-tabs');
  if (!root) return;
  var tabs = Array.prototype.slice.call(root.querySelectorAll('.rail a'));
  var panels = tabs.map(function (t) { return document.getElementById(t.hash.slice(1)); });
  if (panels.some(function (p) { return !p; })) return;

  root.classList.add('js-tabs');
  var rail = root.querySelector('.rail');
  rail.setAttribute('role', 'tablist');
  rail.removeAttribute('aria-label');
  rail.setAttribute('aria-label', 'Journey stages');
  Array.prototype.forEach.call(rail.children, function (li) { li.setAttribute('role', 'presentation'); });

  tabs.forEach(function (tab, i) {
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', panels[i].id);
    panels[i].setAttribute('role', 'tabpanel');
    panels[i].setAttribute('aria-labelledby', tab.id);
    panels[i].setAttribute('tabindex', '0');
  });

  function select(i, opts) {
    opts = opts || {};
    tabs.forEach(function (tab, j) {
      var on = i === j;
      tab.setAttribute('aria-selected', on ? 'true' : 'false');
      tab.setAttribute('tabindex', on ? '0' : '-1');
      panels[j].hidden = !on;
    });
    if (opts.focus) tabs[i].focus();
    if (opts.updateHash && history.replaceState) history.replaceState(null, '', '#' + panels[i].id);
    if (opts.scroll) rail.scrollIntoView({ block: 'start', behavior: 'smooth' });
    // Let Overnote re-place any notes whose element just appeared.
    if (window.overnote && typeof window.overnote.refresh === 'function') window.overnote.refresh();
  }

  function indexForHash(hash) {
    for (var i = 0; i < panels.length; i++) if ('#' + panels[i].id === hash) return i;
    return -1;
  }

  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function (e) {
      e.preventDefault();
      select(i, { updateHash: true });
    });
    tab.addEventListener('keydown', function (e) {
      var n = tabs.length, to = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') to = (i + 1) % n;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') to = (i - 1 + n) % n;
      else if (e.key === 'Home') to = 0;
      else if (e.key === 'End') to = n - 1;
      if (to === null) return;
      e.preventDefault();
      select(to, { focus: true, updateHash: true });
    });
  });

  // "Next in the loop" links inside the panels.
  Array.prototype.forEach.call(root.querySelectorAll('[data-stage-link]'), function (a) {
    a.addEventListener('click', function (e) {
      var i = indexForHash(a.hash);
      if (i === -1) return;
      e.preventDefault();
      select(i, { focus: true, updateHash: true, scroll: true });
    });
  });

  window.addEventListener('hashchange', function () {
    var i = indexForHash(location.hash);
    if (i !== -1) select(i);
  });

  var start = indexForHash(location.hash);
  select(start === -1 ? 0 : start);
})();
