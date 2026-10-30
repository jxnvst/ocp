/* OCP lead capture -> PN Landing Pages leads (page_leads), disposed buyer/seller (ver0) */
(function () {
  var URL = "https://tooambsacmhrlgpwgwsv.supabase.co";
  var KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRvb2FtYnNhY21ocmxncHdnd3N2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE3MTU4NjksImV4cCI6MjA5NzI5MTg2OX0.2votR41Hj8cww9fJgjjQHtdGZkFRYVTwbXYAk_6kkuo";
  var LP = "358e74d4-570f-47e8-bafb-00e604fc80b6";
  function postLead(fields) {
    var payload = {
      landing_page_id: LP,
      name: fields.name || "",
      email: fields.email || "",
      phone: fields.phone || "",
      message: fields.message || fields.address || "",
      source: "onecompasspoint.com",
      metadata: fields.metadata || {}
    };
    return fetch(URL + "/rest/v1/page_leads", {
      method: "POST",
      headers: { "apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json", "Prefer": "return=minimal" },
      body: JSON.stringify(payload)
    });
  }
  document.querySelectorAll("form[data-capture]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var disp = f.getAttribute("data-disposition") || "buyer";
      var fd = new FormData(f);
      var fields = { metadata: { disposition: disp, page: location.pathname, at: new Date().toISOString() } };
      ["name","email","phone","message","address"].forEach(function (k) { var v=fd.get(k); if (v) fields[k]=String(v).trim(); });
      var btn = f.querySelector("[type=submit]");
      if (btn) { btn.disabled = true; btn.textContent = "Sending..."; }
      postLead(fields).then(function (r) {
        var ok = r.ok || r.status === 201;
        var msg = f.querySelector("[data-capture-msg]");
        if (msg) msg.textContent = ok ? "Got it - we'll be in touch within one business day." : "Something went wrong sending. Please try again.";
        if (btn) { btn.disabled = false; btn.textContent = "Submit"; }
        if (ok) f.reset();
      }).catch(function () {
        var msg = f.querySelector("[data-capture-msg]");
        if (msg) msg.textContent = "Network error - please try again.";
        if (btn) { btn.disabled = false; btn.textContent = "Submit"; }
      });
    });
  });
})();
