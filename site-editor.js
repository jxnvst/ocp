/* One Compass Point - Edit Mode (v1): simple overlay editing.
   Click EDIT -> site dims to 50%, words + photos stay at 100%.
   Click any word -> type -> auto-saves. Click any photo -> pick a new one -> auto-saves.
   Changes persist on this device (localStorage); "Done" turns the overlay off. */
(function () {
  var EDITS_KEY = "ocp_edits_v1";
  var groups = [
    { label: "Hero headline", sel: ".hero-heading" },
    { label: "Hero sub-line", sel: ".hero-description .basic-text" },
    { label: "Hero CTA text", sel: ".hero-section .button.primary" },
    { label: "Section heading", sel: ".section-heading" },
    { label: "Section badge", sel: ".section-badge" }
  ];
  var PHOTO_SELS = [".property-image-wrap img", ".photo img", ".prop-img img"];

  function load() { try { return JSON.parse(localStorage.getItem(EDITS_KEY) || "{}"); } catch (e) { return {}; } }
  var edits = load();
  var active = false;

  function matches(s) { try { return document.querySelectorAll(s); } catch (e) { return []; } }

  // ---- apply saved edits whenever the page loads ----
  function applyEdits() {
    Object.keys(edits).forEach(function (key) {
      var v = edits[key];
      try {
        matches(key).forEach(function (el, i) {
          if (v && v[i] !== undefined) {
            if (v[i].t !== undefined) el.textContent = v[i].t;
            else if (v[i].s !== undefined) el.setAttribute("src", v[i].s);
          }
        });
      } catch (e) {}
    });
  }

  function enter() {
    active = true;
    var st = document.createElement("style");
    st.id = "ocp-edit-css";
    st.textContent =
      ".ocp-veil { position: fixed; inset: 0; background: rgba(10,20,35,0.5); z-index: 99990; pointer-events: none; }" +
      ".ocp-editbox { position: fixed; right: 24px; bottom: 24px; z-index: 99999; background:#fff; border:1px solid rgba(0,0,0,.12); border-radius:12px; box-shadow:0 12px 30px rgba(0,0,0,.2); padding:14px; width:300px; font:13px Montserrat,sans-serif; }" +
      ".ocp-editbox input { width:100%; box-sizing:border-box; border:1px solid #d3dce6; border-radius:8px; padding:9px 11px; font-family:inherit; font-size:13px; margin-bottom:8px; }" +
      ".ocp-editbox .row { display:flex; gap:8px; }" +
      ".ocp-editbox .row button { flex:1; background:#1a365d; color:#fff; border:0; border-radius:8px; padding:8px; font-family:inherit; font-size:13px; font-weight:700; cursor:pointer; }" +
      ".ocp-editbox .row button[data-act=cancel] { background:#e2e8f0; color:#475569; }" +
      ".ocp-editable { position: relative !important; z-index: 99995 !important; cursor: text; outline: 1.5px dashed rgba(49,151,149,0.6); outline-offset: 3px; border-radius: 4px; }" +
      ".ocp-photo { position: relative !important; z-index: 99995 !important; cursor: pointer; outline: 1.5px dashed rgba(49,151,149,0.6); outline-offset: 3px; border-radius: 6px; }" +
      ".ocp-editable:focus, .ocp-photo:hover { outline-color: #319795; background: rgba(49,151,149,0.08); }" +
      ".ocp-label { position: absolute; top: -10px; left: -2px; z-index: 99996; background:#1a365d; color:#fff;" +
      "  font: 600 9px/1 'Montserrat',sans-serif; letter-spacing:.06em; text-transform:uppercase; padding:2px 6px; border-radius:4px;" +
      "  opacity: 0; transition: opacity .15s; white-space: nowrap; pointer-events: none; }" +
      ".ocp-editable:hover .ocp-label, .ocp-photo:hover .ocp-label { opacity: 1; }" +
      ".ocp-pill { position: fixed; bottom: 22px; right: 22px; z-index: 99999; background:#1a365d; color:#fff; border:0;" +
      "  border-radius: 999px; padding: 11px 20px; font: 700 13px 'Montserrat',sans-serif; cursor: pointer; box-shadow: 0 8px 24px rgba(0,0,0,.3); }" +
      ".ocp-pill.on { background: #319795; }";
    document.head.appendChild(st);

    var veil = document.createElement("div");
    veil.className = "ocp-veil";
    document.body.appendChild(veil);

    // words
    groups.forEach(function (g) {
      matches(g.sel).forEach(function (el, i) {
        el.classList.add("ocp-editable");
        el.contentEditable = "true";
        // neutralize baked transform ancestors so z-index can lift the element above the veil
        var a = el.parentElement;
        if (a) { var cs = getComputedStyle(a); if (cs.transform && cs.transform !== "none") a.style.transform = "none"; }
        var lab = document.createElement("span");
        lab.className = "ocp-label"; lab.textContent = g.label;
        el.appendChild(lab);
        el.addEventListener("click", function (e) {
          e.preventDefault(); e.stopPropagation();
        });
        el.addEventListener("input", function () {
          edits[g.sel] = edits[g.sel] || [];
          edits[g.sel][i] = { t: el.textContent };
          localStorage.setItem(EDITS_KEY, JSON.stringify(edits));
        });
      });
    });

    // photos: click a photo -> a small text field pops up to paste a link / drive link
    var eb = null;
    PHOTO_SELS.forEach(function (sel) {
      matches(sel).forEach(function (img, i) {
        img.classList.add("ocp-photo");
        var lab = document.createElement("span");
        lab.className = "ocp-label"; lab.textContent = "Click photo to change";
        if (img.parentElement) {
          img.parentElement.style.position = img.parentElement.style.position || "relative";
          img.parentElement.appendChild(lab);
        }
        img.addEventListener("click", function (e) {
          e.preventDefault();
          e.stopPropagation();
          if (eb && eb.parentElement) eb.remove();
          eb = document.createElement("div");
          eb.className = "ocp-editbox";
          eb.innerHTML =
            '<div style="font:700 11px/1.2 Montserrat,sans-serif;color:#1a365d;margin-bottom:6px;">Change this photo</div>' +
            '<input type="text" placeholder="Paste a photo link or Google Drive link">' +
            '<div class="row"><button type="button" data-act="use">Use</button><button type="button" data-act="cancel">Cancel</button></div>';
          document.body.appendChild(eb);
          var inp = eb.querySelector("input");
          inp.value = img.getAttribute("src") || "";
          inp.focus();
          eb.querySelector('[data-act="cancel"]').addEventListener("click", function () { eb.remove(); eb = null; });
          eb.querySelector('[data-act="use"]').addEventListener("click", function () {
            var link = inp.value.trim();
            if (!link) { eb.remove(); eb = null; return; }
            var src = link;
            var m = link.match(/drive\.google\.com\/file\/d\/([\w-]{10,})/);
            if (m) src = "https://drive.google.com/thumbnail?id=" + m[1] + "&sz=w1200";
            img.setAttribute("src", src);
            edits[sel] = edits[sel] || [];
            edits[sel][i] = { s: src };
            localStorage.setItem(EDITS_KEY, JSON.stringify(edits));
            eb.remove(); eb = null;
          });
        });
      });
    });

    // Done button appears only inside edit mode (never on the public site)
    var ebDone = document.createElement("button");
    ebDone.id = "ocp-exit-btn";
    ebDone.className = "ocp-pill on";
    ebDone.textContent = "Done";
    ebDone.addEventListener("click", exit);
    document.body.appendChild(ebDone);
  }

  function exit() {
    active = false;
    var s = document.getElementById("ocp-edit-css");
    if (s) s.remove();
    var veil = document.querySelector(".ocp-veil");
    while (veil) { veil.remove(); veil = document.querySelector(".ocp-veil"); }
    document.querySelectorAll(".ocp-editable").forEach(function (el) {
      el.classList.remove("ocp-editable");
      el.contentEditable = "false";
      var l = el.querySelector(".ocp-label"); if (l) l.remove();
    });
    document.querySelectorAll(".ocp-photo").forEach(function (el) {
      el.classList.remove("ocp-photo");
      if (el.parentElement) { var l = el.parentElement.querySelector(".ocp-label"); if (l) l.remove(); }
    });
    var eb = document.getElementById("ocp-exit-btn");
    if (eb) eb.remove();
  }


  // remove the Webflow runtime badge whenever it appears
  var _badgeObserver = new MutationObserver(function () {
    var b = document.querySelector(".w-webflow-badge");
    if (b) b.remove();
  });
  _badgeObserver.observe(document.documentElement, { childList: true, subtree: true });

  document.addEventListener("DOMContentLoaded", function () {
    applyEdits();
    if (/[?&]ocpe(?:=1)?($|&)/.test(location.search)) enter();
  });
})();