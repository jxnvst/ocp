/* One Compass Point - Edit Mode overlay (ver0)
   Always applies saved text edits (ocp_edits_v1) to the page.
   When the URL has ?edit=1 (or edit mode toggled), every editable element is
   outlined with a role label, and typing over an element saves it instantly
   to localStorage so the site reflects your words. */
(function () {
  var EDITS_KEY = "ocp_edits_v1";
  var groups = [
    { label: "Hero headline", sel: ".hero-heading" },
    { label: "Hero sub-line", sel: ".hero-description .basic-text" },
    { label: "Hero CTA text", sel: ".hero-section .button.primary" },
    { label: "Section heading", sel: ".section-heading" },
    { label: "Section badge", sel: ".section-badge" }
  ];

  function load() {
    try { return JSON.parse(localStorage.getItem(EDITS_KEY) || "{}"); } catch (e) { return {}; }
  }
  var edits = load();

  // 1) always apply saved edits
  function applyEdits() {
    Object.keys(edits).forEach(function (sel) {
      try {
        document.querySelectorAll(sel).forEach(function (el, i) {
          var v = edits[sel][i];
          if (typeof v === "string") el.textContent = v;
        });
      } catch (e) {}
    });
  }

  function matches(s) {
    try { return document.querySelectorAll(s); } catch (e) { return []; }
  }

  function enterEditMode() {
    var style = document.createElement("style");
    style.id = "ocp-edit-css";
    style.textContent =
      ".ocp-editable {" +
      "  outline: 2px dashed #319795 !important;" +
      "  outline-offset: 3px;" +
      "  cursor: text;" +
      "  transition: background .2s;" +
      "}" +
      ".ocp-editable:hover { background: rgba(49,151,149,0.08); }" +
      ".ocp-label {" +
      "  position: absolute; z-index: 99999;" +
      "  background: #1a365d; color: #fff;" +
      "  font: 600 10px/1 'Montserrat', sans-serif;" +
      "  letter-spacing: .05em; text-transform: uppercase;" +
      "  padding: 3px 8px; border-radius: 6px;" +
      "  pointer-events: none; white-space: nowrap;" +
      "}" +
      ".ocp-exit { position: fixed; bottom: 20px; right: 20px; z-index: 99999;" +
      "  background: #1a365d; color: #fff; border: 0; border-radius: 999px;" +
      "  padding: 10px 18px; font: 600 13px 'Montserrat', sans-serif; cursor: pointer;" +
      "  box-shadow: 0 6px 18px rgba(0,0,0,.25); }" +
      ".ocp-exit.on { background: #319795; }";
    document.head.appendChild(style);

    // label + editable everything in the groups
    groups.forEach(function (g) {
      matches(g.sel).forEach(function (el, i) {
        el.classList.add("ocp-editable");
        el.contentEditable = "true";
        el.setAttribute("data-ocp", g.sel + "|" + i);
        el.addEventListener("input", function () {
          edits[g.sel] = edits[g.sel] || [];
          edits[g.sel][i] = el.textContent;
          localStorage.setItem(EDITS_KEY, JSON.stringify(edits));
        });
        var lab = document.createElement("span");
        lab.className = "ocp-label";
        lab.textContent = g.label;
        el.style.position = el.style.position || "relative";
        el.appendChild(lab);
      });
    });

    var exit = document.createElement("button");
    exit.className = "ocp-exit on";
    exit.textContent = "Done Editing";
    exit.addEventListener("click", function () {
      exitEditMode();
      var u = new URL(location.href);
      u.searchParams.delete("edit");
      history.replaceState({}, "", u.toString());
    });
    document.body.appendChild(exit);
  }

  function exitEditMode() {
    var s = document.getElementById("ocp-edit-css");
    if (s) s.remove();
    document.querySelectorAll(".ocp-editable").forEach(function (el) {
      el.classList.remove("ocp-editable");
      el.contentEditable = "false";
      var l = el.querySelector(".ocp-label");
      if (l) l.remove();
    });
    var b = document.querySelector(".ocp-exit");
    if (b) b.remove();
  }

  document.addEventListener("DOMContentLoaded", applyEdits);
  if (/[?&]edit(?:=1)?($|&)/.test(location.search)) {
    document.addEventListener("DOMContentLoaded", enterEditMode);
  }
})();