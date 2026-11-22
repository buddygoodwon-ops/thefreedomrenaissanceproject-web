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
