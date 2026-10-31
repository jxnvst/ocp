#!/usr/bin/env python3
"""OM gallery v3 - 50 bento-box offering-memorandum layouts.

Asymmetric modular (bento) grids: one big hero tile + stat/photo/map/finance
tiles of different sizes per bento grid template. 8 bento grid compositions x
~7 real-arch skin (palette+font+radius) -> 50 unique combos. Real Busti photos
(one of 4 heroes) + Leaflet location map in every template. Data is the same
honest ver5 numbers. Onyx trio (onyx-*.html) is kept untouched at the top.
"""
import os

OUT = "/home/ubuntu/onecompass-deploy/om-templates"
T = "387 Busti Ave"
S = "Buffalo, NY 14201 &middot; West Side"
PRICE, NET, CAP, ROI, RB = "565,000", "67,529", "12.0", "71%", "24.5%"
BASE = "http://www.onecompasspoint.com/photos/busti9/"
PHOTOS = ["main_9unit.jpg", "1793220541343.jpg", "IMG_7021.jpeg", "1793220531697.jpg"]

# 7 skins: (name, bg, ink, mute, line, acc, acc2, rad, mono)
SKINS = [
    ("OnyxLite",  "#121418", "#f2efe6", "#9aa0ab", "#26282e", "#c9a227", "#8a6d1f", 12, False),
    ("Stripe",    "#0a0a10", "#f7f8fb", "#8e8ea4", "#1e1e2e", "#635bff", "#a06bff", 14, False),
    ("Linear",    "#08090c", "#fafafa", "#84858d", "#1c1e24", "#5e6ad2", "#3d3f74", 10, True),
    ("Notion",    "#fbfbf9", "#37352f", "#9b9a97", "#e9e9e7", "#2f6f4f", "#111111", 10, False),
    ("Pastel",    "#fef6ec", "#2b2b2b", "#8b8176", "#f0e3d3", "#ff7a59", "#ffb020", 16, False),
    ("Mono",      "#ffffff", "#0a0a0a", "#777777", "#e6e6e6", "#000000", "#555555", 6, True),
    ("LuxDark",   "#0d1321", "#eef2fa", "#96a2b8", "#1a2438", "#d4a249", "#9a7327", 8, False),
]
# 4 hdrs/fonts set implicitly by mono + serif toggle set below per combo
SERIF = [True, False, False, True, False, False, True]

# 8 bento grid templates: each is a distinct asymmetric grid-template + tile layout
BENTO = [
    ("hero-top",   "\"a a b c\" / \"a a d d\" / \"e f g h\"", ["a:hero 2x", "b:net", "c:cap", "d:photo2x", "e:roi", "f:price", "g:banksmall", "h:cta"]),
    ("hero-left",  "\"a b b c\" / \"a d e f\" / \"g g h h\"", ["a:hero2h", "b:net", "c:cap", "d:roi", "e:price", "f:map", "g:photo2x", "h:fin"]),
    ("mosaic",     "\"a a a b\" / \"c c d d\" / \"e f g g\"", ["a:herobig", "b:net", "c:roi", "d:cap", "e:map", "f:price", "g:photo2x"]),
    ("asym-row",   "\"a b c c\" / \"a d d e\" / \"f f g h\"", ["a:hero2h", "b:net", "c:cap", "d:photo2x", "e:roi", "f:fin", "g:price", "h:banksmall"]),
    ("tall-hero",  "\"a a b b\" / \"a a c d\" / \"e f g h\"", ["a:hero2x", "b:net", "c:roi", "d:price", "e:map", "f:cap", "g:banksmall", "h:cta"]),
    ("wide-net",   "\"a b b b\" / \"c c d d\" / \"e e e f\"", ["a:herobig", "b:netbig", "c:roi", "d:cap", "e:photo2x", "f:map"]),
    ("photo-col",  "\"a a a b\" / \"c d e b\" / \"f f f g\"", ["a:herobig", "b:photoCol", "c:net", "d:roi", "e:cap", "f:fin", "g:map"]),
    ("edge-to-edge","\"a a b c\" / \"d d d d\" / \"e f g h\"",["a:hero2x", "b:net", "c:banksmall", "d:finfull", "e:roi", "f:price", "g:map", "h:cta"]),
]

def skin_css(sk, hero_id):
    name, bg, ink, mute, line, acc, acc2, rad, mono = sk
    body = "'JetBrains Mono',monospace" if mono else "'Plus Jakarta Sans','Segoe UI',Arial,sans-serif"
    head = "'JetBrains Mono',monospace" if mono else ("'Playfair Display',Georgia,serif" if SERIF[SKINS.index(sk)] else "'Plus Jakarta Sans','Segoe UI',Arial,sans-serif")
    return f"""
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:{body};color:var(--ink);background:var(--bg);padding:20px}}
  :root{{--bg:{bg};--ink:{ink};--mute:{mute};--line:{line};--acc:{acc};--acc2:{acc2};--rad:{rad}px}}
  .sheet{{max-width:980px;margin:0 auto;background:var(--bg);border:1px solid var(--line);border-radius:{rad}px;overflow:hidden}}
  .brand{{font-family:{head};font-size:12px;letter-spacing:2.5px;text-transform:uppercase;color:var(--mute)}} .brand b{{color:var(--acc)}}
  h1{{font-family:{head};font-size:26px;line-height:1.1;font-weight:800}}
  .k{{font-size:10px;text-transform:uppercase;letter-spacing:1.2px;color:var(--mute)}}
  .tile{{background:var(--bg);border:1px solid var(--line);border-radius:var(--rad);padding:16px;overflow:hidden}}
  .tile.acc{{background:linear-gradient(150deg,var(--acc),var(--acc2))}}
  .tile img{{width:100%;height:100%;object-fit:cover;border-radius:var(--rad)}}
  .gg{{display:grid;gap:12px;grid-template-columns:repeat(4,1fr);grid-template-areas:var(--ga);padding:14px}}
  .n{{font-size:26px;font-weight:800;color:var(--acc)}} .n.acc{{color:#fff}}
  table{{width:100%;border-collapse:collapse;font-size:11.5px}}
  th{{text-align:left;color:var(--mute);font-size:9.5px;text-transform:uppercase;letter-spacing:.6px;padding:5px 8px;border-bottom:1px solid var(--line)}}
  td{{padding:6px 8px;border-bottom:1px solid var(--line)}}
  .r{{text-align:right}}.total td{{border-top:2px solid var(--acc);font-weight:800}}
  .note{{font-size:11px;color:var(--mute);line-height:1.5;margin-top:6px}}
  .warn{{font-size:10px;color:var(--mute);font-style:italic;margin-top:10px}}
  .foot{{font-size:10px;letter-spacing:1px;color:var(--mute);text-align:center;padding:12px 0 16px}}
  a.btn{{display:inline-block;background:var(--acc);color:var(--bg);font-weight:800;text-decoration:none;padding:9px 16px;border-radius:999px}}
  #mapbox{{width:100%;height:100%;min-height:170px;border:0}}
"""

def head_html(sk, hero_url):
    bg = sk[1]; ink = sk[2]
    return f'<div style="padding:20px 22px 6px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid {sk[4]}"><div><div class="brand">One Compass <b>Point</b></div><h1 style="font-size:20px;margin-top:6px">{T}</h1><div class="k">{S}</div></div><span class="tile acc" style="color:#fff;padding:8px 14px;border:0"><div class="k" style="color:#fff">OFFERING</div><b style="font-size:18px">${PRICE}</b></span></div>'

def income():
    return "<table><tr><th>Rent</th><th>Units</th><th class=r>Mo</th></tr><tr><td>Section 8</td><td>4</td><td class=r>$4,792</td></tr><tr><td>Market</td><td>5</td><td class=r>$5,500</td></tr><tr class=total><td>Gross</td><td>9</td><td class=r>$10,292</td></tr><tr><td>Vacancy 4%</td><td></td><td class=r>($410)</td></tr><tr class=total><td>EGI</td><td></td><td class=r>$9,880</td></tr></table>"

def opex():
    return "<table><tr><th>Expense</th><th class=r>Yr</th></tr><tr><td>Taxes</td><td class=r>$6,000</td></tr><tr><td>Insurance</td><td class=r>$7,200</td></tr><tr><td>Water/sewer</td><td class=r>$4,050</td></tr><tr><td>Maintenance</td><td class=r>$8,100</td></tr><tr><td>Turnover/legal</td><td class=r>$2,700</td></tr><tr><td>Mgmt 8%</td><td class=r>$9,485</td></tr><tr class=total><td>Cap reserve</td><td class=r>$13,500</td></tr><tr class=total><td>Total</td><td class=r>$51,035</td></tr></table>"

def roi():
    return "<table><tr><th>Path</th><th class=r>Cash</th><th class=r>ROI</th></tr><tr><td>Bank 20% down</td><td class=r>$113k</td><td class=r>24.5%</td></tr><tr class=total><td>Creative 8% down</td><td class=r>$45k</td><td class=r>71%</td></tr></table>"

def tile(area_html_id, label, inner):
    return f'<div id="{area_html_id}" class="tile"><div class="k">{label}</div><div style="margin-top:6px">{inner}</div></div>'

def build(i, sk, bento, hero_photo):
    areas, plan = bento
    grid_areas = "grid-template-areas:" + areas + ";"
    hero_url = BASE + hero_photo
    # tile contents
    def finfull():
        return income() + opex()
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><title>OM-{i:02d} | {T}</title>
<link rel=stylesheet href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>{skin_css(sk, i)}</style></head><body><div class="sheet">
{head_html(sk, hero_url)}
<div class="gg" style="{grid_areas}">
  <!-- hero (area a) -->
  <div class="tile" style="grid-area:a;padding:0"><img src="{hero_url}" alt=""></div>
  <!-- net -->
  <div class="tile" style="grid-area:b"><div class="k">Net cash / yr</div><div class="n">${NET}</div></div>
  <!-- cap -->
  <div class="tile" style="grid-area:c"><div class="k">Cap (after reserves)</div><div class="n">{CAP}%</div></div>
  <!-- roi -->
  <div class="tile" style="grid-area:d"><div class="k">Investor ROI</div><div class="n">{ROI}</div></div>
  <!-- price -->
  <div class="tile" style="grid-area:e"><div class="k">Price · per unit</div><div class="n">$565k · $62.8k</div></div>
  <!-- photo2x -->
  <div class="tile" style="grid-area:f;padding:0"><img src="{BASE}1793220541343.jpg" alt=""></div>
  <!-- photo strip span -->
  <div class="tile" style="grid-area:g;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:4px">
     <img src="{BASE}IMG_7021.jpeg"><img src="{BASE}1793220531697.jpg"><img src="{BASE}IMG_7024.jpeg"></div>
  <!-- bank small -->
  <div class="tile" style="grid-area:h"><div class="k">Bank vs Creative</div>{roi()}</div>
  <!-- finance -->
  <div class="tile" style="grid-area:i"><div class="k">Income &amp; expenses</div>{finfull()}</div>
  <!-- map -->
  <div class="tile" style="grid-area:j;padding:0"><iframe id="mapbox" loading="lazy"
    src="https://www.openstreetmap.org/export/embed.html?bbox=-78.925%2C42.882%2C-78.845%2C42.920&amp;layer=mapnik&amp;marker=42.90264%2C-78.89503"></iframe></div>
  <!-- cta -->
  <div class="tile acc" style="grid-area:k;color:#fff"><div class="k" style="color:#fff">Creative terms — cash, subject-to, or seller financing</div>
    <a class="btn" style="background:#fff;color:var(--acc);margin-top:8px;display:inline-block" href="mailto:jaison@onecompasspoint.com">Request Pricing &amp; Rent Roll</a></div>
</div>
<p class="warn" style="padding:0 22px">Evaluation summary, not an offer. Projections incl. $1,500/unit annual capital reserve; actuals depend on inspection, tax &amp; leases.</p>
<div class="foot">One Compass Point &middot; Investor Priced Real Estate</div>
</div></body></html>"""

def main():
    os.makedirs(OUT, exist_ok=True)
    for i in range(50):
        sk = SKINS[i % len(SKINS)]
        bento = BENTO[(i * 5) % len(BENTO)]
        ph = PHOTOS[i % len(PHOTOS)]
        open(os.path.join(OUT, f"om-{i+1:02d}.html"), "w").write(build(i + 1, sk, bento, ph))
    print("wrote 50 om-* bento templates")

if __name__ == "__main__":
    main()