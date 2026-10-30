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
        el.addEventListener("input", function () {
          edits[g.sel] = edits[g.sel] || [];
          edits[g.sel][i] = { t: el.textContent };
          localStorage.setItem(EDITS_KEY, JSON.stringify(edits));
        });
      });
    });

    // photos: click = replace with your own image
    var fileInput = document.createElement("input");
    fileInput.type = "file"; fileInput.accept = "image/*"; fileInput.style.display = "none";
    document.body.appendChild(fileInput);
    var currentImg = null;
    PHOTO_SELS.forEach(function (sel) {
      matches(sel).forEach(function (img, i) {
        img.classList.add("ocp-photo");
        var lab = document.createElement("span");
        lab.className = "ocp-label"; lab.textContent = "Click to change photo";
        if (img.parentElement) {
          img.parentElement.style.position = img.parentElement.style.position || "relative";
          img.parentElement.appendChild(lab);
        }
        img.addEventListener("click", function (e) {
          e.stopPropagation();
          currentImg = { img: img, sel: sel, i: i };
          fileInput.value = "";
          fileInput.click();
        });
      });
    });

    fileInput.addEventListener("change", function () {
      if (!currentImg || !fileInput.files || !fileInput.files[0]) return;
      var f = fileInput.files[0];
      var reader = new FileReader();
      reader.onload = function (ev) {
        var src = ev.target.result;
        currentImg.img.setAttribute("src", src);
        edits[currentImg.sel] = edits[currentImg.sel] || [];
        edits[currentImg.sel][currentImg.i] = { s: src };
        localStorage.setItem(EDITS_KEY, JSON.stringify(edits));
      };
      reader.readAsDataURL(f);
    });

    pill.textContent = "Done";
    pill.classList.add("on");
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
    pill.textContent = "Edit Site";
    pill.classList.remove("on");
  }

  // floating toggle pill (always available - no URL required)
  var pill = document.createElement("button");
  pill.className = "ocp-pill";
  pill.textContent = "Edit Site";
  pill.addEventListener("click", function () { active ? exit() : enter(); });
  document.body.appendChild(pill);

  document.addEventListener("DOMContentLoaded", function () {
    applyEdits();
    if (/[?&]edit(?:=1)?($|&)/.test(location.search)) enter();
  });
})();