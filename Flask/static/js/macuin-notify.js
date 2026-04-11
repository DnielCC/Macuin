/**
 * Notificaciones discretas (cliente). Las del servidor usan flash + partial.
 * Uso: macuinNotify('Texto', 'success' | 'danger' | 'warning' | 'info');
 * Alias: mostrarToast (compatibilidad con plantillas admin en español).
 */
(function () {
  var STYLE_ID = 'macuin-toast-css-injected';
  function injectCss() {
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement('style');
    s.id = STYLE_ID;
    s.textContent =
      '.macuin-toast-stack{position:fixed;top:0.75rem;right:0.75rem;z-index:1090;max-width:min(440px,94vw);display:flex;flex-direction:column;gap:0.45rem;pointer-events:none;}' +
      '.macuin-toast-stack .macuin-toast{pointer-events:auto;margin:0;font-size:0.875rem;line-height:1.38;box-shadow:0 6px 20px rgba(15,23,42,0.14);border:none;border-radius:0.5rem;animation:macuinToastInJs 0.26s ease-out;}' +
      '@keyframes macuinToastInJs{from{opacity:0;transform:translateX(14px)}to{opacity:1;transform:translateX(0)}}' +
      '.macuin-toast.macuin-toast-hiding{opacity:0;transform:translateX(10px);transition:opacity .32s ease,transform .32s ease}';
    document.head.appendChild(s);
  }
  function ensureStack() {
    injectCss();
    var el = document.getElementById('macuin-toast-stack');
    if (!el) {
      el = document.createElement('div');
      el.id = 'macuin-toast-stack';
      el.className = 'macuin-toast-stack';
      el.setAttribute('aria-live', 'polite');
      document.body.appendChild(el);
    }
    return el;
  }
  var map = { danger: 'danger', success: 'success', warning: 'warning', info: 'info', primary: 'primary', secondary: 'secondary' };
  function notify(message, category) {
    var cat = map[category] || 'secondary';
    var stack = ensureStack();
    var n = stack.querySelectorAll('.macuin-toast').length;
    var div = document.createElement('div');
    div.className = 'alert alert-' + cat + ' macuin-toast mb-0 py-2 px-3';
    div.setAttribute('role', 'status');
    div.textContent = String(message || '');
    stack.appendChild(div);
    window.setTimeout(function () {
      div.classList.add('macuin-toast-hiding');
      window.setTimeout(function () {
        div.remove();
        if (stack && !stack.children.length) stack.remove();
      }, 380);
    }, 6200 + n * 320);
  }
  window.macuinNotify = notify;
  window.mostrarToast = notify;
})();
