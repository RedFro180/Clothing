// Foldable, dual-screen and split-screen sizes used by scroll_test.js fold and fold_test.js.
// Galaxy Z Fold 8 Ultra (published specs, July 2026): cover 6.5" 2520x1080, inner 8.0" 2504x2256.
// CSS sizes below are estimates: pixels / device scale (2.625 is Samsung's usual default; 3 if the phone's
// display zoom is raised), minus about 110 px of browser bars. Split screen = roughly half of the inner screen.
const UA = "Mozilla/5.0 (Linux; Android 16; SM-F976U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/28.0 Chrome/130.0.0.0 Mobile Safari/537.36";
const fold = (width, height, dpr = 2.625) => ({ viewport: { width, height }, deviceScaleFactor: dpr, isMobile: true, hasTouch: true, userAgent: UA });
const FOLD = [
  ["Fold cover",                 fold(411, 850)],
  ["Fold cover sideways",        fold(960, 330)],
  ["Fold open",                  fold(859, 845)],
  ["Fold open (bigger zoom)",    fold(752, 725, 3)],
  ["Fold open sideways",         fold(954, 750)],
  ["Fold split screen (half)",   fold(427, 845)],
  ["Fold split screen (1/3)",    fold(286, 845)],
  ["Fold split top/bottom",      fold(954, 360)],
  ["Fold half-folded (Flex)",    fold(859, 400)],
  ["Fold pop-up window",         fold(500, 620)],
  ["Dual screen, one side",      fold(540, 720, 2.5)],
  ["Dual screen, spanned",       fold(1114, 720, 2.5)],
  ["Desktop split screen",       { viewport: { width: 640, height: 860 } }],
];
module.exports = { FOLD, fold, UA };
