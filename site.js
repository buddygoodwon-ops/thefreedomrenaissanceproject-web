/* Swipe between pages (like SlamDunk) + registration form handling. */
(function () {
  var ORDER = ["index", "story", "idea", "plan", "movement", "place", "white-paper", "join"];
  function cur() {
    var p = location.pathname.split("/").pop().replace(/\.html$/i, "");
    return p || "index";
  }
  function go(d) {
    var i = ORDER.indexOf(cur());
    if (i < 0) return;
    var n = ORDER[(i + d + ORDER.length) % ORDER.length];
    location.href = n + ".html";
  }
  var x0 = null, y0 = null;
  document.addEventListener("touchstart", function (e) {
    if (e.target.closest("input,textarea,select,table,.table-wrap")) { x0 = null; return; }
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
  }, { passive: true });
  document.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
    if (Math.abs(dx) > 90 && Math.abs(dx) > Math.abs(dy) * 2) go(dx < 0 ? 1 : -1);
    x0 = null;
  }, { passive: true });

  var form = document.getElementById("register-form");
  if (!form) return;
  var status = document.getElementById("form-status");
  function show(kind, msg) { status.className = "form-status " + kind; status.textContent = msg; }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var data = {};
    new FormData(form).forEach(function (v, k) {
      if (data[k] !== undefined) data[k] = [].concat(data[k], v); else data[k] = v;
    });
    var btn = form.querySelector("button[type=submit]");
    btn.disabled = true; btn.textContent = "Sending…";
    fetch(form.action, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      form.reset();
      show("ok", "You're registered. Welcome to the Movement — watch your inbox for the next step, including where the first county is.");
    }).catch(function () {
      show("err", "We couldn't send your registration just now. Please try again in a minute, or email us directly.");
    }).finally(function () {
      btn.disabled = false; btn.textContent = "Register";
    });
  });
})();

/* Save to Home Screen button + instructions */
(function () {
  var standalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone;
  if (standalone) return;
  var deferred = null;
  window.addEventListener("beforeinstallprompt", function (e) { e.preventDefault(); deferred = e; });

  var ua = navigator.userAgent || "";
  var isIOS = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  var isAndroid = /Android/.test(ua);
  var share = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px"><path d="M12 3v12"/><path d="M8 7l4-4 4 4"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>';
  var plus = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="vertical-align:-3px"><rect x="3" y="3" width="18" height="18" rx="4"/><path d="M12 8v8M8 12h8"/></svg>';
  var steps = isIOS
    ? '<li>Tap the <b>Share</b> button ' + share + ' at the bottom (or top) of Safari.</li><li>Scroll down and tap <b>Add to Home Screen</b> ' + plus + '.</li><li>Tap <b>Add</b>. The monkey icon appears on your home screen as <b>100th</b>.</li>'
    : isAndroid
    ? '<li>Tap the browser menu <b>&#8942;</b> at the top right.</li><li>Tap <b>Add to Home screen</b> or <b>Install app</b>.</li><li>Tap <b>Add</b>. The monkey icon appears on your home screen as <b>100th</b>.</li>'
    : '<li>On your phone, open <b>thefreedomrenaissanceproject.com</b>.</li><li>iPhone: tap <b>Share</b> ' + share + ', then <b>Add to Home Screen</b>.</li><li>Android: tap the menu <b>&#8942;</b>, then <b>Add to Home screen</b>.</li>';

  var modal = document.createElement("div");
  modal.className = "a2hs-modal";
  modal.setAttribute("role", "dialog");
  modal.setAttribute("aria-modal", "true");
  modal.setAttribute("aria-label", "Save to your home screen");
  modal.innerHTML = '<div class="a2hs-card"><button class="a2hs-close" aria-label="Close">&times;</button>' +
    '<img src="/apple-touch-icon.png" alt="" width="84" height="84"><h3>Save to your home screen</h3>' +
    '<p>Keep the Movement one tap away.</p><ol>' + steps + '</ol></div>';
  document.body.appendChild(modal);
  function close() { modal.classList.remove("open"); }
  modal.addEventListener("click", function (e) { if (e.target === modal || e.target.closest(".a2hs-close")) close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });

  function open() {
    if (deferred) {
      deferred.prompt();
      deferred.userChoice.finally(function () { deferred = null; });
      return;
    }
    modal.classList.add("open");
  }

  var icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="3"/><path d="M12 7v7M9 11l3 3 3-3"/><path d="M10.5 18.5h3"/></svg>';
  var bar = document.querySelector(".footer-bar");
  if (bar) {
    var d = document.createElement("div"); d.className = "fb-divider";
    var b = document.createElement("button");
    b.className = "footer-btn a2hs-btn"; b.type = "button";
    b.setAttribute("aria-label", "Save to your home screen"); b.title = "Save to your home screen";
    b.innerHTML = icon;
    b.addEventListener("click", open);
    bar.appendChild(d); bar.appendChild(b);
  }
  var cta = document.querySelector(".hero .cta-row");
  if (cta) {
    var g = document.createElement("button");
    g.type = "button"; g.className = "btn btn-ghost a2hs-cta";
    g.innerHTML = icon + "<span>Save to Home Screen</span>";
    g.addEventListener("click", open);
    cta.appendChild(g);
  }
})();
