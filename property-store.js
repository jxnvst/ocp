/* One Compass Point - property store renderer (ver0)
   Reads properties added via /admin.html (localStorage, same origin) and
   appends them to the property grid. New cards go to the RIGHT (end of list). */
(function () {
  var KEY = "ocp_properties_v1";
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; }
  }
  var props = load();
  if (!props.length) return;

  var list = document.querySelector(".properties-list");
  if (!list) return;
  var tmpl = list.querySelector(".property-item");
  if (!tmpl) return;

  function money(price) {
    if (!price) return null;
    var p = String(price).trim();
    if (p.charAt(0) === "$") p = p.slice(1).trim();
    return p;
  }

  props.forEach(function (p, idx) {
    var node = tmpl.cloneNode(true);
    // not a template link anymore
    var a = node.querySelector(".property");
    if (a) { a.setAttribute("href", "#property"); a.classList.add("ocp-added"); }

    var img = node.querySelector(".property-image-wrap img");
    if (img) {
      if (p.photos && p.photos.length) {
        img.setAttribute("src", p.photos[0]);
        img.removeAttribute("srcset");
        img.removeAttribute("sizes");
        img.style.transform = "";
      } else {
        img.style.display = "none";
      }
    }

    var cat = node.querySelector(".property-category");
    if (cat && p.tag) cat.textContent = p.tag;

    var loc = node.querySelector(".property-location .small-text, .property-location .basic-text");
    if (loc) {
      var cityState = [p.city, p.state].filter(Boolean).join(", ");
      loc.textContent = [p.street, cityState].filter(Boolean).join(", ");
    }

    var name = node.querySelector(".property-name .basic-text");
    if (name) name.textContent = p.title || p.street;

    var amt = money(p.price);
    if (amt !== null) {
      var priceNodes = node.querySelectorAll(".property-price .basic-text");
      if (priceNodes.length >= 2) priceNodes[1].textContent = amt;
      else if (priceNodes.length === 1) priceNodes[0].textContent = "$" + amt;
    }

    if (p.desc) {
      var wrap = node.querySelector(".property-info-wrap");
      var note = document.createElement("div");
      note.className = "small-text color-grey-400 nomral linehigh-small ocp-desc";
      note.style.cssText = "margin-top:8px;";
      note.textContent = p.desc;
      if (wrap) wrap.appendChild(note);
    }

    list.appendChild(node); // append -> new card goes to the right
  });
})();
