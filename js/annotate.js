// Review gate. Every showcase page loads this file just before </body>:
//   <script type="module" src="../js/annotate.js"></script>   (path relative to the page)
// It loads Overnote (js/review.js + js/vendor/overnote.js) only when the URL
// has ?review=1, so regular visitors never download it. Modules don't load
// from file://; serve over HTTP to review.
if (new URLSearchParams(location.search).get('review') === '1') {
  import('./review.js');
}
