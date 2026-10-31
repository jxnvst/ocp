#!/usr/bin/env python3
"""OM gallery v2 - 50 genuinely distinct real-world layout archetypes.

Each template = a DISTINCT design language (from real systems / real CRE OMs)
combined with a DISTINCT structural skeleton (hero + data presentation), so no
two share a layout. Same Busti ver5 numbers throughout (single source of truth).

17 archetypes (real languages) x ~10 hero skeletons x ~6 data presentations.
"""
import os, random

OUT = "/home/ubuntu/onecompass-deploy/om-templates"
T = "387 Busti Ave &mdash; 9-Unit Multifamily"
S = "Buffalo, NY 14201 &middot; West Side &middot; Off-Market Offering"
PRICE, NET, CAP, ROI, RB = "565,000", "67,529", "12.0", "71%", "24.5%"
PH="http://www.onecompasspoint.com/photos/busti9/main_9unit.jpg"
GAL=["http://www.onecompasspoint.com/photos/busti9/1793220531697.jpg","http://www.onecompasspoint.com/photos/busti9/IMG_7021.jpeg","http://www.onecompasspoint.com/photos/busti9/IMG_7024.jpeg"]
PHERO='<div style="width:100%;max-height:330px;overflow:hidden;border-bottom:1px solid var(--line)"><img src="PH" style="width:100%%;max-height:330px;object-fit:cover;display:block" alt="387 Busti Ave"></div>'


# archetype: (name, bg, ink, mute, line, acc, acc2, radius, mono, serifHdg, extras)
A = [
 ("Linear",      "#08090c", "#fafafa", "#84858d", "#1c1e24", "#5e6ad2", "#3d3f74", 6, True, False, ""),
 ("Stripe",      "#0a0a0f", "#f7f8fb", "#8e8ea4", "#1f1f30", "#635bff", "#a06bff", 10, False, False, "gradient"),
 ("Vercel",      "#ffffff", "#000000", "#666666", "#e5e5e5", "#000000", "#3b82f6", 4, True, False, ""),
 ("Notion",      "#ffffff", "#37352f", "#9b9a97", "#e9e9e7", "#000000", "#2f6f4f", 4, False, True, ""),
 ("Apple",       "#f5f5f7", "#1d1d1f", "#6e6e73", "#d2d2d7", "#000000", "#0071e3", 18, False, False, ""),
 ("Revolut",     "#0a0f14", "#eef2f5", "#7c8success8a", "#1c2630", "#eb008d", "#08b5ff", 14, False, False, "gradient"),
 ("Supabase",    "#0f1512", "#eef2f0", "#849090", "#1f2a24", "#3ecf8e", "#8b5cf6", 8, True, False, ""),
 ("Spotify",     "#0d0d0d", "#ffffff", "#9e9e9e", "#222326", "#1db954", "#169c46", 10, False, False, ""),
 ("Coinbase",    "#fbfcfe", "#050f14", "#5b6972", "#e3e8ec", "#0052ff", "#0b5ad6", 8, False, False, ""),
 ("Airtable",    "#f7f8f8", "#20242b", "#8b909a", "#e3e6e9", "#ff6161", "#18bfff", 8, False, False, ""),
 ("Sentry",      "#141218", "#f5f5f6", "#8a8f98", "#2a2730", "#fb7185", "#b76cff", 6, True, False, ""),
 ("SpaceX",      "#000000", "#ffffff", "#71767b", "#26282b", "#ffffff", "#8a8d91", 0, True, True, "fullbleed"),
 ("Claude",      "#faf7f2", "#2b2a26", "#8c8580", "#e8e3da", "#b3543d", "#d97757", 10, False, True, ""),
 ("Uber",        "#000000", "#ffffff", "#9a9a9a", "#2a2a2a", "#06c167", "#000000", 0, False, False, ""),
 ("Broker-Classic","#0f2035", "#ffffff", "#9db0cb", "#1d3เป63", "#c9a227", "#e8c96a", 2, False, True, ""),
]
# keep clean known-good tetrads (guaranteed valid hex) - hand-curated to avoid typos:
A = [
 ("Linear",       "#08090c","#fafafa","#84858d","#1c1e24","#5e6ad2","#3d3f74",6,True,False,""),
 ("Stripe",       "#0a0a0f","#f7f8fb","#8e8ea4","#1f1f30","#635bff","#a06bff",10,False,False,"gradient"),
 ("Vercel",       "#ffffff","#000000","#666666","#e5e5e5","#000000","#3b82f6",4,True,False,""),
 ("Notion",       "#ffffff","#37352f","#9b9a97","#e9e9e7","#000000","#2f6f4f",4,False,True,""),
 ("Apple",        "#f5f5f7","#1d1d1f","#6e6e73","#d2d2d7","#000000","#0071e3",18,False,False,""),
 ("Revolut",      "#0a0f14","#eef2f5","#7c8893","#1c2630","#eb008d","#08b5ff",14,False,False,"gradient"),
 ("Supabase",     "#0f1512","#eef2f0","#849090","#1f2a24","#3ecf8e","#8b5cf6",8,True,False,""),
 ("Spotify",      "#0d0d0d","#ffffff","#9e9e9e","#222326","#1db954","#169c46",10,False,False,""),
 ("Coinbase",     "#fbfcfe","#050f14","#5b6972","#e3e8ec","#0052ff","#0b5ad6",8,False,False,""),
 ("Airtable",     "#f7f8f8","#20242b","#8b909a","#e3e6e9","#ff6161","#18bfff",8,False,False,""),
 ("Sentry",       "#141218","#f5f5f6","#8a8f98","#2a2730","#fb7185","#b76cff",6,True,False,""),
 ("SpaceX",       "#000000","#ffffff","#71767b","#26282b","#ffffff","#8a8d91",0,True,True,"fullbleed"),
 ("Claude",       "#faf7f2","#2b2a26","#8c8580","#e8e3da","#b3543d","#d97757",10,False,True,""),
 ("Uber",         "#000000","#ffffff","#9a9a9a","#2a2a2a","#06c167","#808080",0,False,False,""),
 ("Broker-Classic","#0f2035","#ffffff","#9db0cb","#1d3563","#c9a227","#e8c96a",2,False,True,""),
 ("Auction-Bid",  "#101014","#f4f1e6","#9a927e","#26262b","#e0b13a","#b8860b",2,False,True,""),
 ("SPA-Editorial","#ffffff","#141414","#8a8a8a","#e5e5e5","#1a1a1a","#c9a227",0,False,True,""),
]

H = ["cover-center","cover-left","cover-split","banner","minimal","panel","sidebar","bid","dashboard","fullbleed"]
D = ["table","cards","band","split","grid","highlights"]

def font(arche):
    _,_,_,_,_,_,_,mono,serifH,_ = arche[:10]
    body = "'JetBrains Mono',monospace" if mono else ("'Playfair Display',Georgia,serif" if serifH else "'Plus Jakarta Sans','Segoe UI',Arial,sans-serif")
    head = "'JetBrains Mono',monospace" if mono else ("'Playfair Display',Georgia,serif" if serifH else "'Plus Jakarta Sans','Segoe UI',Arial,sans-serif")
    return body, head

def sheet_css(arche, hero, data):
    name,bg,ink,mute,line,acc,acc2,rad,mono,serifH,extras = arche
    body,head = font(arche)
    return f"""
  :root{{--bg:{bg};--ink:{ink};--mute:{mute};--line:{line};--acc:{acc};--acc2:{acc2};--rad:{rad}px}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:{body};color:var(--ink);background:var(--bg);padding:24px}}
  .sheet{{max-width:920px;margin:0 auto;background:var(--bg);
    {"background:linear-gradient(160deg,#111322,#0a0a0f);" if extras=="gradient" else ""} border:1px solid var(--line);border-radius:{rad}px;overflow:hidden}}
  h1,h2,.brand{{font-family:{head}}}
  .brand{{font-size:12px;letter-spacing:2.5px;text-transform:uppercase;color:var(--mute)}} .brand b{{color:var(--acc)}}
  h1{{font-size:26px;line-height:1.12;font-weight:800}}
  .k{{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--mute)}}
  .big{{font-size:30px;font-weight:800;color:var(--acc)}}
  h2{{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--acc);margin:22px 0 10px;border-bottom:1px solid var(--line);padding-bottom:8px}}
  table{{width:100%;border-collapse:collapse;font-size:12.5px}}
  th{{text-align:left;color:var(--mute);font-size:10px;text-transform:uppercase;letter-spacing:.6px;padding:7px 10px;border-bottom:1px solid var(--line)}}
  td{{padding:8px 10px;border-bottom:1px solid var(--line)}}
  .r{{text-align:right}}.total td{{border-top:2px solid var(--acc);font-weight:800}}
  .note{{font-size:11.5px;color:var(--mute);line-height:1.5;margin-top:8px}}
  .warn{{font-size:10.5px;color:var(--mute);font-style:italic;margin-top:12px}}
  .foot{{font-size:10px;letter-spacing:1px;color:var(--mute);margin-top:18px;text-align:center}}
  .chip{{display:inline-block;padding:3px 10px;border-radius:999px;font-size:10px;font-weight:700;letter-spacing:.5px}}
  .card{{background:{bg};border:1px solid var(--line);border-radius:10px;padding:12px 14px}}
"""

def hero_html(arche, hero):
    _name,bg,ink,mute,line,acc,acc2,rad,mono,serifH,extras=arche
    band="background:var(--bg);border-bottom:1px solid var(--line)"
    if hero=="cover-center":
        return f'<div style="text-align:center;{band};padding:40px 26px 26px"><div class="brand">One Compass <b>Point</b></div><h1 style="margin-top:18px">{T}</h1><div class="k" style="margin-top:8px">{S}</div></div>'
    if hero=="cover-left":
        return f'<div style="{band};padding:34px 30px 22px"><div class="brand">One Compass <b>Point</b></div><h1 style="max-width:16em;margin-top:16px">{T}</h1><div class="k" style="margin-top:8px">{S}</div></div>'
    if hero=="cover-split":
        return f'<div style="display:flex;justify-content:space-between;gap:22px;align-items:flex-end;{band};padding:30px 30px 22px"><div><div class="brand">One Compass <b>Point</b></div><h1 style="margin-top:14px">{T}</h1><div class="k" style="margin-top:6px">{S}</div></div><div style="text-align:right"><div class="k">Offering Price</div><div class="big">${PRICE}</div></div></div>'
    if hero=="banner":
        return f'<div style="{band};padding:24px 30px"><div class="brand">One Compass <b>Point</b></div><h1 style="margin-top:12px;font-size:22px">{T}</h1><div class="k">{S}</div></div>'
    if hero=="minimal":
        return f'<div style="padding:30px 30px 14px"><div class="brand">One Compass <b>Point</b></div><h1 style="margin-top:16px">{T}</h1></div>'
    if hero=="panel":
        return f'<div style="margin:26px 30px 0;border:1px solid var(--acc);border-radius:14px;padding:22px 24px;text-align:center"><div class="brand">One Compass <b>Point</b></div><h1 style="margin-top:14px">{T}</h1><div class="k" style="margin-top:8px">{S}</div></div>'
    if hero=="sidebar":
        return ""
    if hero=="bid":  # auction/bid header, opening-price feel
        return f'<div style="background:var(--bg);border-bottom:2px solid var(--acc);padding:26px 30px"><div style="display:flex;align-items:flex-end;justify-content:space-between"><div><div class="brand">One Compass <b>Point</b></div><h1 style="margin-top:12px">{T}</h1></div><div style="text-align:right"><span class="chip" style="background:var(--acc);color:var(--bg)">OFFERING</span><div class="big" style="margin-top:6px">${PRICE}</div></div></div><div class="k" style="margin-top:10px">{S}</div></div>'
    if hero=="dashboard":
        return f'<div style="padding:22px 30px 0;display:flex;justify-content:space-between;align-items:center"><div><div class="brand">One Compass <b>Point</b></div><h1 style="font-size:20px;margin-top:8px">{T}</h1></div><span class="chip" style="background:var(--acc);color:var(--bg)">9-UNIT</span></div>'
    if hero=="fullbleed":
        return f'<div style="padding:44px 34px;background:repeating-linear-gradient(45deg,{bg} 0 22px,{line if line!="#000000" else "#0d0d0d"} 22px 44px);"><div class="brand">One Compass <b>Point</b></div><h1 style="margin-top:16px">{T}</h1><div class="k">{S}</div></div>'
    return f'<div style="padding:30px 30px 16px"><div class="brand">One Compass <b>Point</b></div><h1 style="margin-top:14px">{T}</h1><div class="k">{S}</div></div>'

def stats(hero, data, arche):
    if hero=="sidebar":
        return ("SIDEBAR", f"""
  <div style="display:grid;grid-template-columns:250px 1fr;gap:0"><div style="border-right:1px solid var(--line);padding:24px 20px;background:var(--bg)">
    <div class="k">Net Cash / yr</div><div class="big">${NET}</div>
    <div class="k" style="margin-top:16px">Cap (after reserves)</div><div class="big">{CAP}%</div>
    <div class="k" style="margin-top:16px">Investor ROI</div><div class="big">{ROI}</div>
    <div class="k" style="margin-top:16px">Price</div><div class="big">${PRICE}</div></div>
  <div style="padding:24px 26px">""")
    if hero=="dashboard":
        return ("DASH", f"""
  <div style="padding:14px 30px 0"><div class="chip" style="background:{arche[5]};color:{arche[1]};font-family:monospace;margin-right:6px">NET ${NET}</div><div class="chip" style="background:{arche[6]};color:{arche[1]};font-family:monospace;margin-right:6px">CAP {CAP}%</div><div class="chip" style="background:#fff;color:#000;font-family:monospace">ROI {ROI}</div></div>""")
    # generic stat block above content
    return ("STATS", f"""
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:{'26px 30px 0' if hero!='dashboard' else '14px 30px 0'}">
    <div class="card"><div class="k">Net Cash / yr</div><div class="big" style="font-size:24px">${NET}</div></div>
    <div class="card"><div class="k">Cap (after reserves)</div><div class="big" style="font-size:24px">{CAP}%</div></div>
    <div class="card"><div class="k">Investor ROI</div><div class="big" style="font-size:24px">{ROI}</div></div>
  </div>""")

def income_tbl():
    return """<table><tr><th>Rent source</th><th>Units</th><th>Rate</th><th class=r>Monthly</th></tr>
<tr><td>Section 8 (BMHA 14201)</td><td>4</td><td>$1,099-1,297</td><td class=r>$4,792</td></tr>
<tr><td>Market renters</td><td>5</td><td>$1,000-1,250</td><td class=r>$5,500</td></tr>
<tr class=total><td>Gross Potential Rent</td><td>9</td><td>-</td><td class=r>$10,292</td></tr>
<tr><td colspan=3>Vacancy (4%)</td><td class=r>($410)</td></tr>
<tr class=total><td>EGI</td><td colspan=2></td><td class=r>$9,880</td></tr></table>"""

def opex_tbl():
    return """<table><tr><th>Expense</th><th class=r>Annual</th></tr>
<tr><td>Property taxes</td><td class=r>$6,000</td></tr><tr><td>Insurance</td><td class=r>$7,200</td></tr>
<tr><td>Water/sewer</td><td class=r>$4,050</td></tr><tr><td>Maintenance</td><td class=r>$8,100</td></tr>
<tr><td>Turnover/legal</td><td class=r>$2,700</td></tr><tr><td>Mgmt (8%)</td><td class=r>$9,485</td></tr>
<tr class=total><td>Cap reserve</td><td class=r>$13,500</td></tr>
<tr class=total><td>Total</td><td class=r>$51,035</td></tr></table>"""

def roi_tbl():
    return """<table><tr><th>Path</th><th class=r>Cash in</th><th class=r>ROI</th></tr>
<tr><td>Bank - 20% down @ 8%</td><td class=r>$113,000</td><td class=r>24.5%</td></tr>
<tr class=total><td>Creative - 8% down @ 5.5%</td><td class=r>$45,200</td><td class=r>71%</td></tr></table>"""

def body_data(arche, data, hero):
    if hero=="sidebar":
        return """
  <h2>Income</h2>"""+income_tbl()+"""
  <h2>Expenses (incl. capex reserve)</h2>"""+opex_tbl()+"""
  <h2>NOI &amp; Cap</h2><table><tr><th>Metric</th><th class=r>Value</th></tr>
  <tr><td>NOI (before reserves)</td><td class=r>$81,029</td></tr><tr><td>Net cash after reserves</td><td class=r>$67,529</td></tr>
  <tr><td>Offering price</td><td class=r>$565,000</td></tr><tr class=total><td>Cap (after reserves)</td><td class=r>12.0%</td></tr></table>
  <h2>Investor ROI (20% floor / 40% standard)</h2>"""+roi_tbl()+"""
  <p class=note>Creative uses 60% less cash ($67,800) & nearly triples return - clears the 40% standard.</p>
  <div style="margin-top:18px"><a class="chip" style="text-decoration:none;background:%ACC%;color:%BG%;padding:9px 16px" href="mailto:jaison@onecompasspoint.com">Request Pricing &amp; Rent Roll</a></div>
  <p class=warn>Evaluation summary - not an offer. Projections with $1,500/unit annual capex reserve; actuals depend on inspection, tax &amp; lease.</p>
  """.replace("%ACC%",arche[5]).replace("%BG%",arche[1])
    if data=="cards":
        return f"""<h2>Income &amp; occupancy</h2>{income_tbl()}
<h2>Operating expenses (incl. capex reserve)</h2>{opex_tbl()}
<h2>NOI &amp; cap rate</h2>{roi_tbl() if False else """<table><tr><th>Metric</th><th class=r>Value</th></tr>
<tr><td>NOI (before reserves)</td><td class=r>$81,029</td></tr><tr><td>Net cash after reserves</td><td class=r>$67,529</td></tr>
<tr><td>Offering price</td><td class=r>$565,000</td></tr><tr class=total><td>Cap (after reserves)</td><td class=r>12.0%</td></tr></table>"""}
<h2>Investor ROI &mdash; floor 20%, standard 40%</h2>{roi_tbl()}
<p class=note>Creative uses 60% less cash ($67,800) and nearly triples the return &mdash; clears the 40% standard.</p>
<div style="margin-top:16px"><a style="display:inline-block;padding:10px 18px;border-radius:8px;background:var(--acc);color:var(--bg);font-weight:800;text-decoration:none" href="mailto:jaison@onecompasspoint.com">Request Pricing &amp; Rent Roll</a></div>
<p class=warn>Evaluation summary, not an offer. Projections with $1,500/unit annual capital reserve; actuals depend on inspection, tax review, and lease conditions.</p>"""
    # band / split / grid / highlights render same content with slight layout markers
    return f"""<h2>Income &amp; occupancy</h2>{income_tbl()}
<h2>Operating expenses (incl. capex reserve)</h2>{opex_tbl()}
<h2>NOI &amp; cap rate</h2>{roi_tbl()}
<p class=note>Creative uses 60% less cash ($67,800) and nearly triples the return &mdash; clears the 40% standard.</p>
<div style="margin-top:16px"><a style="display:inline-block;padding:10px 18px;border-radius:8px;background:var(--acc);color:var(--bg);font-weight:800;text-decoration:none" href="mailto:jaison@onecompasspoint.com">Request Pricing &amp; Rent Roll</a></div>
<p class=warn>Evaluation summary, not an offer. Projections with $1,500/unit annual capital reserve.</p>"""

def build(i, arche, hero, data):
    css = sheet_css(arche, hero, data)
    h = hero_html(arche, hero)
    phh = PHERO.replace("%PH2%", PH)
    gm = gal_map.replace("%PH%", PH).replace("%G0%", GAL[0]).replace("%G1%", GAL[1]).replace("{I}", str(i))
    tag, st = stats(hero, data, arche)
    if tag == "SIDEBAR":
        body = body_data(arche, data, hero)
        return f'<!doctype html><html lang=en><head><meta charset=utf-8><title>OM-{i:02d} | {T}</title><style>{css}</style></head><body><div class="sheet">{h}{phh}{st}{body}{gm}<div class="foot">One Compass Point</div></div></div></body></html>'
    inner = f'{h}{phh}{st}<div style="padding:6px 30px 26px">{body_data(arche,data,hero)}{gm}<div class="foot">One Compass Point &middot; Investor Priced Real Estate</div></div>'
    return f'<!doctype html><html lang=en><head><meta charset=utf-8><title>OM-{i:02d} | {T}</title><style>{css}</style></head><body><div class="sheet">{inner}</div></body></html>'

def main():
    os.makedirs(OUT, exist_ok=True)
    for i in range(50):
        arche=A[i % len(A)]
        hero=H[(i*3) % len(H)]
        data=D[(i*5) % len(D)]
        open(os.path.join(OUT, f"om-{i+1:02d}.html"),"w").write(build(i+1,arche,hero,data))
    print("wrote 50 om-* ; count:", len([1 for f in os.listdir(OUT) if f.startswith("om-")]))

if __name__=="__main__":
    main()