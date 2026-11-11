/* Content Example prototypes: progressive enhancement. Hand-written.
   Everything works without this file. It only adds:
   instant filtering and search, overlay sync and note highlighting,
   copy and print buttons, the YouTube swap (on click only), and, for the
   Canvas model, pan/zoom, the bottom sheet, floating note cards and the
   split divider. No dependencies. */
(function () {
  "use strict";
  var doc = document;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  var narrow = window.matchMedia("(max-width: 899px)");
  var INTERACTIVE = "a,button,input,select,textarea,summary,label,iframe,[contenteditable],pre";

  /* ---------- Library filters ---------- */
  function initFilters() {
    var form = $(".filters");
    if (!form) return;
    var lib = form.closest(".lib") || doc;
    var cards = $$(".card", lib);
    var q = $("#q", form);
    var status = $("[data-fstatus]", form);
    var empty = $("[data-fempty]", form);
    var params = new URLSearchParams(location.search);
    params.forEach(function (v, k) {
      if (k === "q" && q) { q.value = v; return; }
      var r = form.querySelector('input[name="' + k + '"][value="' + CSS.escape(v) + '"]');
      if (r) r.checked = true;
    });
    function run(push) {
      var term = q ? q.value.trim().toLowerCase() : "";
      cards.forEach(function (c) { c.classList.toggle("is-hidden", !!term && c.dataset.text.indexOf(term) === -1); });
      var shown = cards.filter(function (c) { return getComputedStyle(c).display !== "none"; }).length;
      if (status) status.textContent = shown + " of " + cards.length + " shown";
      if (empty) empty.hidden = shown !== 0;
      if (push) {
        var p = new URLSearchParams();
        $$("input[type=radio]:checked", form).forEach(function (r) { if (r.value) p.set(r.name, r.value); });
        if (term) p.set("q", term);
        var s = p.toString();
        history.replaceState(null, "", s ? "?" + s : location.pathname);
      }
    }
    form.addEventListener("change", function () { run(true); });
    if (q) q.addEventListener("input", function () { run(true); });
    form.addEventListener("submit", function (ev) { ev.preventDefault(); run(true); });
    run(false);
  }

  /* ---------- Overlay toggles, copy, print, video ---------- */
  function initCommon() {
    var toggles = $$(".ov-toggle");
    toggles.forEach(function (t) {
      t.addEventListener("change", function () {
        toggles.forEach(function (o) { o.checked = t.checked; });
        if (!t.checked) closeNote();
      });
    });
    $$("[data-print]").forEach(function (b) { b.hidden = false; b.addEventListener("click", function () { window.print(); }); });
    $$(".ce-copy").forEach(function (b) {
      if (!navigator.clipboard) return;
      b.hidden = false;
      b.addEventListener("click", function () {
        var pre = $("#" + b.dataset.copy + " pre");
        navigator.clipboard.writeText(pre.textContent).then(function () {
          b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy"; }, 2000);
        });
      });
    });
    $$("[data-open-details]").forEach(function (a) {
      a.addEventListener("click", function () {
        var d = $(a.getAttribute("href"));
        if (d && d.tagName === "DETAILS") d.open = true;
      });
    });
    $$("[data-yt-load]").forEach(function (a) {
      a.addEventListener("click", function (ev) {
        ev.preventDefault();
        var box = a.closest("[data-yt]");
        var f = doc.createElement("iframe");
        f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(box.dataset.yt) + "?rel=0";
        f.title = "Video: " + box.dataset.ytTitle;
        f.allow = "encrypted-media; picture-in-picture; fullscreen";
        f.setAttribute("allowfullscreen", "");
        box.innerHTML = "";
        box.appendChild(f);
        f.focus();
      });
    });
    // Stage and requirements-only: pins jump to the note (native anchor); add a highlight.
    if (!doc.body.classList.contains("m-canvas")) {
      doc.addEventListener("click", function (ev) {
        var pin = ev.target.closest(".pin, .ce-note-jump");
        if (!pin) return;
        var target = $(pin.getAttribute("href"));
        if (!target) return;
        $$(".is-hl").forEach(function (x) { x.classList.remove("is-hl"); });
        target.classList.add("is-hl");
        setTimeout(function () { target.classList.remove("is-hl"); }, 2500);
      });
    }
  }

  /* ---------- Canvas: pan and zoom with CSS transforms ---------- */
  var canvases = [];
  function PanZoom(cv) {
    var self = this;
    var content = $("[data-cv-content]", cv);
    var root = cv.closest(".cvp");
    var s = 1, x = 0, y = 0, MIN = 0.2, MAX = 3;
    self.cv = cv; self.content = content;
    content.style.position = "relative";

    function area() {
      var r = cv.getBoundingClientRect();
      var a = { left: 0, top: 0, right: r.width, bottom: r.height };
      if (!narrow.matches) {
        var sheet = $(".sheet", root);
        if (sheet) {
          var sr = sheet.getBoundingClientRect();
          if (sr.left < r.right && sr.left > r.left) a.right = Math.min(a.right, sr.left - r.left - 12);
        }
        var card = $(".fl-card", root);
        if (card) a.left = Math.max(a.left, card.getBoundingClientRect().right - r.left + 12);
      } else {
        var sh = $(".sheet", root);
        if (sh) a.bottom = Math.min(a.bottom, sh.getBoundingClientRect().top - r.top - 8);
      }
      // Keep clear of floating controls along the top edge.
      $$(narrow.matches ? ".fl-card, .fl-pill, .fl-layers" : ".fl-pill", root).forEach(function (el) {
        var b = el.getBoundingClientRect();
        if (b.height && b.bottom > r.top && b.top < r.top + 120) a.top = Math.max(a.top, b.bottom - r.top + 8);
      });
      a.w = a.right - a.left; a.h = a.bottom - a.top;
      return a;
    }
    function clamp() {
      var r = cv.getBoundingClientRect();
      var w = content.offsetWidth * s, h = content.offsetHeight * s;
      x = Math.min(r.width - 80, Math.max(80 - w, x));
      y = Math.min(r.height - 80, Math.max(80 - h, y));
    }
    function apply(fromSync) {
      clamp();
      content.style.transform = "translate(" + x + "px," + y + "px) scale(" + s + ")";
      positionNote();
    }
    // Paired canvases zoom and pan together: relative moves are mirrored,
    // each keeps its own fit.
    function peers(fn) {
      if (!cv.dataset.cvSync) return;
      canvases.forEach(function (o) { if (o !== self && o.cv.dataset.cvSync === cv.dataset.cvSync) fn(o); });
    }
    self.fit = function () {
      var a = area();
      var target = cv.dataset.cvFit ? $(cv.dataset.cvFit, content) : null;
      if (target) {
        var tw = target.offsetWidth + 32;
        s = Math.max(MIN, Math.min(1, a.w / tw));
        x = a.left + (a.w - target.offsetWidth * s) / 2 - target.offsetLeft * s;
        y = a.top + 8 - target.offsetTop * s;
      } else {
        var cw = content.offsetWidth;
        var pad = parseFloat(getComputedStyle(content).paddingTop) || 0;
        s = Math.max(MIN, Math.min(1, a.w / cw));
        x = a.left + (a.w - cw * s) / 2;
        y = a.top + 8 - pad * s;
      }
      apply();
    };
    self.zoomAt = function (factor, px, py, fromPeer) {
      var ns = Math.max(MIN, Math.min(MAX, s * factor));
      if (px == null) { var a = area(); px = a.left + a.w / 2; py = a.top + a.h / 2; }
      x = px - (px - x) * (ns / s);
      y = py - (py - y) * (ns / s);
      s = ns; apply();
      if (!fromPeer) peers(function (o) { o.zoomAt(factor, px, py, true); });
    };
    self.pan = function (dx, dy, fromPeer) {
      x += dx; y += dy; apply();
      if (!fromPeer) peers(function (o) { o.pan(dx, dy, true); });
    };
    self.show = function (el, animate) {
      var a = area();
      var cr = content.getBoundingClientRect(), er = el.getBoundingClientRect();
      var ex = (er.left - cr.left) / s, ey = (er.top - cr.top) / s;
      var ew = er.width / s;
      x = a.left + a.w / 2 - (ex + ew / 2) * s;
      y = a.top + a.h * 0.3 - ey * s;
      if (animate && !reduced.matches) {
        content.style.transition = "transform .3s ease";
        setTimeout(function () { content.style.transition = ""; }, 320);
      }
      apply();
    };

    // Pointer: one finger pans, two fingers pinch.
    var pts = new Map(), last = null, moved = 0;
    cv.addEventListener("pointerdown", function (ev) {
      if (ev.target.closest(INTERACTIVE) || ev.button > 0) return;
      cv.setPointerCapture(ev.pointerId);
      pts.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
      last = null; moved = 0;
    });
    cv.addEventListener("pointermove", function (ev) {
      if (!pts.has(ev.pointerId)) return;
      var prev = pts.get(ev.pointerId);
      pts.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
      if (pts.size === 1) {
        moved += Math.abs(ev.clientX - prev.x) + Math.abs(ev.clientY - prev.y);
        if (moved > 3) cv.classList.add("is-dragging");
        self.pan(ev.clientX - prev.x, ev.clientY - prev.y);
      } else if (pts.size === 2) {
        var p = Array.from(pts.values());
        var r = cv.getBoundingClientRect();
        var mid = { x: (p[0].x + p[1].x) / 2 - r.left, y: (p[0].y + p[1].y) / 2 - r.top };
        var dist = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
        if (last) { self.pan(mid.x - last.mid.x, mid.y - last.mid.y); self.zoomAt(dist / last.dist, mid.x, mid.y); }
        last = { mid: mid, dist: dist };
      }
    });
    function up(ev) { pts.delete(ev.pointerId); last = null; if (!pts.size) cv.classList.remove("is-dragging"); }
    cv.addEventListener("pointerup", up);
    cv.addEventListener("pointercancel", up);
    cv.addEventListener("wheel", function (ev) {
      ev.preventDefault();
      var r = cv.getBoundingClientRect();
      if (ev.ctrlKey || ev.metaKey) self.zoomAt(Math.exp(-ev.deltaY * 0.01), ev.clientX - r.left, ev.clientY - r.top);
      else self.pan(-ev.deltaX, -ev.deltaY);
    }, { passive: false });
    cv.addEventListener("keydown", function (ev) {
      if (ev.target !== cv) return;
      var k = ev.key, step = ev.shiftKey ? 200 : 60;
      if (k === "ArrowUp") self.pan(0, step);
      else if (k === "ArrowDown") self.pan(0, -step);
      else if (k === "ArrowLeft") self.pan(step, 0);
      else if (k === "ArrowRight") self.pan(-step, 0);
      else if (k === "+" || k === "=") self.zoomAt(1.25);
      else if (k === "-" || k === "_") self.zoomAt(0.8);
      else if (k === "0") self.fit();
      else return;
      ev.preventDefault();
    });
    // Tabbing to a pin or link inside the canvas: keep it in view without native scrolling.
    cv.addEventListener("focusin", function (ev) {
      if (ev.target === cv) return;
      cv.scrollTop = 0; cv.scrollLeft = 0;
      var a = area(), r = cv.getBoundingClientRect(), er = ev.target.getBoundingClientRect();
      if (er.left < r.left + a.left || er.right > r.left + a.right || er.top < r.top || er.bottom > r.top + a.bottom) self.show(ev.target, false);
    });
    cv.addEventListener("scroll", function () { cv.scrollTop = 0; cv.scrollLeft = 0; });
    canvases.push(self);
  }

  /* ---------- Canvas: floating note cards ---------- */
  var note = null, notePins = [], noteIdx = -1;
  function pzFor(el) { for (var i = 0; i < canvases.length; i++) if (canvases[i].cv.contains(el)) return canvases[i]; return null; }
  function positionNote() {
    if (!note || note.hidden || noteIdx < 0) return;
    var pin = notePins[noteIdx], root = note.parentElement;
    var rr = root.getBoundingClientRect(), pr = pin.getBoundingClientRect();
    var w = note.offsetWidth, h = note.offsetHeight;
    var left = pr.right - rr.left + 10, top = pr.top - rr.top - 8;
    var limitRight = rr.width - 12;
    var sheet = $(".sheet", root);
    if (sheet && !narrow.matches) limitRight = sheet.getBoundingClientRect().left - rr.left - 12;
    if (left + w > limitRight) left = pr.left - rr.left - w - 10;
    left = Math.max(12, Math.min(left, rr.width - w - 12));
    var maxTop = rr.height - h - 12;
    if (sheet && narrow.matches) maxTop = sheet.getBoundingClientRect().top - rr.top - h - 12;
    top = Math.max(12, Math.min(top, maxTop));
    note.style.left = left + "px"; note.style.top = top + "px";
  }
  function openNote(i, focus) {
    var pin = notePins[i]; if (!pin) return;
    noteIdx = i;
    var li = $("#" + pin.dataset.note);
    $(".nc-h", note).textContent = "Note " + (i + 1) + " of " + notePins.length + " · " + $(".ce-note-h", li).textContent;
    $(".nc-body", note).innerHTML = "";
    var p = doc.createElement("p"); p.textContent = $(".ce-note-t", li).textContent; $(".nc-body", note).appendChild(p);
    $("[data-nc-count]", note).textContent = (i + 1) + " / " + notePins.length;
    note.hidden = false;
    var pz = pzFor(pin);
    if (pz) pz.show(pin, true);
    positionNote();
    setTimeout(positionNote, 340);
    if (focus) { note.tabIndex = -1; note.focus(); }
  }
  function closeNote(returnFocus) {
    if (!note || note.hidden) return;
    note.hidden = true;
    if (returnFocus && notePins[noteIdx]) notePins[noteIdx].focus();
    noteIdx = -1;
  }
  function initNotes() {
    note = $("[data-notecard]");
    if (!note) return;
    notePins = $$(".cv .pin");
    notePins.forEach(function (pin, i) {
      pin.addEventListener("click", function (ev) { ev.preventDefault(); openNote(i, true); });
    });
    note.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-nc]"); if (!b) return;
      if (b.dataset.nc === "close") closeNote(true);
      if (b.dataset.nc === "next") openNote((noteIdx + 1) % notePins.length, false);
      if (b.dataset.nc === "prev") openNote((noteIdx - 1 + notePins.length) % notePins.length, false);
    });
    doc.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closeNote(true); });
    // "Show in the content" links in the details panel move the canvas instead of scrolling.
    doc.addEventListener("click", function (ev) {
      var a = ev.target.closest('a[href^="#rg-"]'); if (!a) return;
      var el = $(a.getAttribute("href")); var pz = el && pzFor(el); if (!pz) return;
      ev.preventDefault();
      var sheet = $(".sheet"); if (sheet && narrow.matches) setSheet(sheet, "collapsed");
      pz.show(el, true);
      $$(".is-hl").forEach(function (x) { x.classList.remove("is-hl"); });
      el.classList.add("is-hl");
      setTimeout(function () { el.classList.remove("is-hl"); }, 2500);
    });
  }

  /* ---------- Canvas: bottom sheet (phones) ---------- */
  var STATES = ["collapsed", "half", "full"];
  function setSheet(sheet, st) {
    sheet.dataset.sheet = st;
    sheet.style.height = "";
    var h = $("[data-sheet-handle]", sheet);
    if (h) h.setAttribute("aria-expanded", st === "collapsed" ? "false" : "true");
  }
  function initSheet() {
    var sheet = $(".sheet"); if (!sheet) return;
    var handle = $("[data-sheet-handle]", sheet); if (!handle) return;
    var startY = null, startH = 0, dragged = false;
    handle.addEventListener("click", function () {
      if (dragged) { dragged = false; return; }
      var i = STATES.indexOf(sheet.dataset.sheet);
      setSheet(sheet, STATES[(i + 1) % STATES.length]);
    });
    handle.addEventListener("pointerdown", function (ev) {
      if (!narrow.matches) return;
      startY = ev.clientY; startH = sheet.getBoundingClientRect().height; dragged = false;
      handle.setPointerCapture(ev.pointerId); sheet.classList.add("is-dragging");
    });
    handle.addEventListener("pointermove", function (ev) {
      if (startY === null) return;
      var dy = startY - ev.clientY;
      if (Math.abs(dy) > 4) dragged = true;
      sheet.style.height = Math.max(60, startH + dy) + "px";
    });
    handle.addEventListener("pointerup", function () {
      if (startY === null) return;
      startY = null; sheet.classList.remove("is-dragging");
      if (!dragged) return;
      var h = sheet.getBoundingClientRect().height, H = sheet.parentElement.getBoundingClientRect().height;
      var targets = [92, H * 0.48, H - 56], best = 0;
      targets.forEach(function (t, i) { if (Math.abs(t - h) < Math.abs(targets[best] - h)) best = i; });
      setSheet(sheet, STATES[best]);
    });
  }

  /* ---------- Canvas: split divider (pairs) ---------- */
  function initSplit() {
    var split = $("[data-split]"); if (!split) return;
    var div = $("[data-split-divider]", split);
    var val = 50;
    function setV(v) {
      val = Math.max(20, Math.min(80, v));
      split.style.setProperty("--split", val + "%");
      div.setAttribute("aria-valuenow", Math.round(val));
      div.setAttribute("aria-orientation", narrow.matches ? "horizontal" : "vertical");
    }
    var dragging = false;
    div.addEventListener("pointerdown", function (ev) { dragging = true; div.setPointerCapture(ev.pointerId); });
    div.addEventListener("pointermove", function (ev) {
      if (!dragging) return;
      var r = split.getBoundingClientRect();
      setV(narrow.matches ? (ev.clientY - r.top) / r.height * 100 : (ev.clientX - r.left) / r.width * 100);
    });
    div.addEventListener("pointerup", function () { dragging = false; });
    div.addEventListener("keydown", function (ev) {
      var k = ev.key;
      if (k === "ArrowLeft" || k === "ArrowUp") setV(val - 5);
      else if (k === "ArrowRight" || k === "ArrowDown") setV(val + 5);
      else if (k === "Home") setV(20);
      else if (k === "End") setV(80);
      else return;
      ev.preventDefault();
    });
    setV(50);
    narrow.addEventListener && narrow.addEventListener("change", function () { setV(val); });
  }

  function initCanvas() {
    $$("[data-cv]").forEach(function (cv) { new PanZoom(cv); });
    if (!canvases.length) return;
    $$("[data-zoom]").forEach(function (b) {
      b.addEventListener("click", function () {
        var root = b.closest(".cvp");
        var pz = canvases.filter(function (c) { return root.contains(c.cv); })[0];
        if (!pz) return;
        if (b.dataset.zoom === "in") pz.zoomAt(1.25);
        else if (b.dataset.zoom === "out") pz.zoomAt(0.8);
        else canvases.forEach(function (c) { if (root.contains(c.cv)) c.fit(); });
      });
    });
    var fitAll = function () { canvases.forEach(function (c) { c.fit(); }); };
    initSheet(); initSplit(); initNotes();
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(fitAll); else fitAll();
    fitAll();
    var t; window.addEventListener("resize", function () { clearTimeout(t); t = setTimeout(fitAll, 120); });
  }

  function init() { initFilters(); initCommon(); initCanvas(); }
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", init); else init();
})();
