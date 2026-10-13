// Canonical Optimizely widget bootstrap pattern.
// Copy this shape into script.js, swap ROOT_CLASS to match your widget's root wrapper class.
// This pattern is idempotent (won't double-render) and fails safely if the mount target is missing.

(function () {
  var ROOT_CLASS = 'so-widget-root'; // change to your widget's root wrapper class
  var utils = optimizely.get('utils');
  var selector = widget.selector;

  function init() {
    if (!selector) {
      console.warn('[widget] No widget.selector configured');
      return;
    }

    utils.waitForElement(selector).then(function (target) {
      if (!target) {
        console.warn('[widget] Target not found for selector:', selector);
        return;
      }

      // Idempotency guard — bail if widget already inserted.
      if (target.querySelector('.' + ROOT_CLASS)) {
        return;
      }

      target.insertAdjacentHTML('beforeend', widget.$html);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
