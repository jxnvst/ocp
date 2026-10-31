#!/usr/bin/env python3
"""OM template gallery generator (ver0) - 50 unique offering-memorandum
layouts + 3 Onyx (dark gray + shimmering metal) signatures.

All layouts carry the same Busti ver5 data (single source of truth) so the
gallery compares LAYOUTS, not numbers. Deterministic combos: 12 palettes x
5 hero layouts x 3 stat styles x 3 type moods -> 50 unique files (om-01..50),
plus onyx-gold / onyx-silver / onyx-bronze.
"""
import os

OUT = "/home/ubuntu/onecompass-deploy/om-templates"

TITLE = "387 Busti Ave &mdash; 9-Unit Multifamily"
SUB = "Buffalo, NY 14201 &middot; West Side &middot; Off-Market Offering"
PRICE = "565,000"
NET = "67,529"
CAP = "12.0"
ROI = "71%"
ROI_BANK = "24.5%"

# ── 12 palettes: (name, bg, ink, mute, line, accent, accent2, band) ─────────
PALETTES = [
    ("Graphite &amp; Gold",      "#14171c", "#f5f2ea", "#9aa0ab", "#262b33", "#c9a227", "#8a6d1f", "#1c2027"),
    ("Midnight &amp; Platinum",  "#0d1420", "#eef2f8", "#8b96a5", "#1c2634", "#c8ccd5", "#8f9aa8", "#131c28"),
    ("Forest &amp; Cream",       "#14231c", "#f6f1e6", "#9aa79e", "#223128", "#d9b46a", "#a8853f", "#1a2a21"),
    ("Oxblood &amp; Ivory",     "#2a1215", "#f7efe6", "#b09a97", "#3d1f22", "#d4a85c", "#a97d37", "#341a1d"),
    ("Navy &amp; Copper",        "#101b2e", "#eef2f9", "#8d99ac", "#1d293f", "#c07a43", "#92572c", "#16233a"),
    ("Charcoal &amp; Coral",     "#1a1a1d", "#f5f2ef", "#a39fa0", "#2a2a2e", "#e0684a", "#b34c33", "#212124"),
    ("Umber &amp; Bronze",       "#231a10", "#f4ead9", "#a6916f", "#352818", "#b3793a", "#7f5423", "#2a1f12"),
    ("Slate &amp; Teal",         "#132029", "#eef4f6", "#8fa2ab", "#1e3039", "#2f9e8f", "#1f7468", "#182b34"),
    ("Ebony &amp; Silver",       "#16161a", "#edeef1", "#9b9da3", "#26262c", "#b9bcc4", "#83868f", "#1e1e23"),
    ("Wine &amp; Champagne",     "#2b1521", "#f6ece6", "#ab94a0", "#3e2233", "#dcc48e", "#b39154", "#35202b"),
    ("Iron &amp; Amber",         "#191a1e", "#f3e9da", "#a39b8d", "#26272c", "#e09b3e", "#b46f1e", "#202127"),
    ("Pine &amp; Pewter",        "#12201c", "#eef4f0", "#93a39c", "#1e2f28", "#9aa5a8", "#6b787c", "#182822"),
]
# ── 5 hero layouts ───────────────────────────────────────────────────────
HEROES = [
    "banner",     # full-width dark band, title + stat chips on the band
    "centered",   # centered title over subtle gradient, stats below
    "split",      # left brand + title, right big price number
    "left",       # left-aligned title, stat band under, quiet
    "topline",    # thin accent rule + smallcaps title, big header block
]
# ── 3 stat styles ─────────────────────────────────────────────────────────
STATS = ["cards", "band", "big"]
# ── 3 type moods ──────────────────────────────────────────────────────────
TYPES = ["serif", "sans", "editorial"]


def css_base(palette, hero, stat, typ):
    bg, ink, mute, line, acc, acc2, band = palette[1:]
    fam = {"serif": "'Playfair Display', Georgia, serif",
           "sans": "'Plus Jakarta Sans','Segoe UI',Arial,sans-serif",
           "editorial": "'Source Serif Pro', Georgia, serif"}[typ]
    hfam = {"serif": "'Playfair Display', Georgia, serif",
            "sans": "'Plus Jakarta Sans','Segoe UI',Arial,sans-serif",
            "editorial": "'Libre Franklin','Segoe UI',Arial,sans-serif"}[typ]
    return f"""
  :root {{ --bg:{bg}; --ink:{ink}; --mute:{mute}; --line:{line}; --acc:{acc}; --acc2:{acc2}; --band:{band}; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:{fam}; color:var(--ink); background:var(--bg); padding:26px; }}
  .sheet {{ max-width:920px; margin:0 auto; background:var(--bg); border:1px solid var(--line); border-radius:16px; overflow:hidden; }}
  h1,h2,.brand {{ font-family:{hfam}; }}
  .brand {{ font-size:19px; font-weight:800; letter-spacing:-.3px; }} .brand b {{ color:var(--acc); }}
  .mute {{ color:var(--mute); }}
  h2 {{ font-size:15px; font-weight:800; color:var(--acc); margin:22px 0 10px; border-bottom:1px solid var(--line); padding-bottom:6px; letter-spacing:.2px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th {{ text-align:left; color:var(--mute); font-size:11px; text-transform:uppercase; letter-spacing:.5px; padding:8px 10px; border-bottom:1px solid var(--line); }}
  td {{ padding:9px 10px; border-bottom:1px solid var(--line); }}
  .r {{ text-align:right; }} .total td {{ border-top:2px solid var(--acc); font-weight:800; }}
  .note {{ font-size:12px; color:var(--mute); margin-top:8px; line-height:1.5; }}
  .cta {{ margin-top:22px; background:var(--band); border:1px solid var(--line); border-radius:10px; padding:15px 18px; }}
  .btn {{ display:inline-block; background:var(--acc); color:var(--bg); font-weight:800; padding:10px 20px; border-radius:9px; margin-top:10px; text-decoration:none; }}
  .warn {{ font-size:11px; color:var(--mute); margin-top:12px; font-style:italic; }}
  .foot {{ font-size:11px; color:var(--mute); margin-top:18px; text-align:center; opacity:.7; }}
"""


def hero_html(hero, palette):
    bg, ink, mute, line, acc, acc2, band = palette[1:]
    if hero == "banner":
        return f"""
  <div style="background:var(--band);border-bottom:1px solid var(--line);padding:26px 30px;">
    <div class="brand">One Compass <b>Point</b></div>
    <div class="mute" style="font-size:11px;letter-spacing:.6px;">INVESTOR PRICED REAL ESTATE</div>
    <h1 style="font-size:26px;margin-top:16px;">{TITLE}</h1>
    <div class="mute" style="font-size:13px;margin-top:4px;">{SUB}</div>
  </div>"""
    if hero == "centered":
        return f"""
  <div style="text-align:center;padding:34px 26px 20px;background:linear-gradient(180deg,var(--band),transparent);">
    <div class="brand">One Compass <b>Point</b></div>
    <h1 style="font-size:28px;margin-top:18px;">{TITLE}</h1>
    <div class="mute" style="font-size:13px;margin-top:6px;">{SUB}</div>
  </div>"""
    if hero == "split":
        return f"""
  <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;padding:28px 30px;background:var(--band);border-bottom:1px solid var(--line);">
    <div><div class="brand">One Compass <b>Point</b></div>
      <h1 style="font-size:24px;margin-top:14px;">{TITLE}</h1>
      <div class="mute" style="font-size:12px;margin-top:4px;">{SUB}</div></div>
    <div style="text-align:right;"><div class="mute" style="font-size:11px;">OFFERING PRICE</div>
      <div style="font-size:30px;font-weight:800;color:var(--acc);">${PRICE}</div></div>
  </div>"""
    if hero == "left":
        return f"""
  <div style="padding:30px 30px 18px;">
    <div class="brand">One Compass <b>Point</b></div>
    <h1 style="font-size:25px;margin-top:14px;">{TITLE}</h1>
    <div class="mute" style="font-size:13px;margin-top:4px;">{SUB}</div>
  </div>"""
    # topline
    return f"""
  <div style="padding:28px 30px 16px;border-top:4px solid var(--acc);">
    <div class="brand" style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--mute);">One Compass <b>Point</b></div>
    <h1 style="font-size:27px;margin-top:12px;">{TITLE}</h1>
    <div class="mute" style="font-size:13px;margin-top:4px;">{SUB}</div>
  </div>"""


def stats_html(stat):
    cards = f"""
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:20px 30px 0;">
    <div style="background:var(--band);border:1px solid var(--line);border-radius:10px;padding:14px 16px;">
      <div class="mute" style="font-size:11px;text-transform:uppercase;letter-spacing:.6px;">Net Cash / yr (after reserves)</div>
      <div style="font-size:23px;font-weight:800;color:var(--acc);margin-top:4px;">${NET}</div></div>
    <div style="background:var(--band);border:1px solid var(--line);border-radius:10px;padding:14px 16px;">
      <div class="mute" style="font-size:11px;text-transform:uppercase;letter-spacing:.6px;">Cap rate (after reserves)</div>
      <div style="font-size:23px;font-weight:800;color:var(--acc);margin-top:4px;">{CAP}%</div></div>
    <div style="background:var(--band);border:1px solid var(--line);border-radius:10px;padding:14px 16px;">
      <div class="mute" style="font-size:11px;text-transform:uppercase;letter-spacing:.6px;">Investor ROI @ asking</div>
      <div style="font-size:23px;font-weight:800;color:var(--acc);margin-top:4px;">{ROI}</div></div>
  </div>"""
    band = f"""
  <div style="display:flex;gap:0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:18px 30px 0;">
    <div style="flex:1;padding:14px;text-align:center;border-right:1px solid var(--line);"><div class="mute" style="font-size:11px;text-transform:uppercase;">Net Cash / yr</div><div style="font-size:22px;font-weight:800;color:var(--acc);">${NET}</div></div>
    <div style="flex:1;padding:14px;text-align:center;border-right:1px solid var(--line);"><div class="mute" style="font-size:11px;text-transform:uppercase;">Cap (after res)</div><div style="font-size:22px;font-weight:800;color:var(--acc);">{CAP}%</div></div>
    <div style="flex:1;padding:14px;text-align:center;"><div class="mute" style="font-size:11px;text-transform:uppercase;">Investor ROI</div><div style="font-size:22px;font-weight:800;color:var(--acc);">{ROI}</div></div>
  </div>"""
    big = f"""
  <div style="padding:22px 30px 0;display:grid;grid-template-columns:2fr 1fr 1fr;gap:14px;align-items:end;">
    <div><div class="mute" style="font-size:11px;text-transform:uppercase;letter-spacing:.6px;">Net Cash / yr (after reserves)</div><div style="font-size:36px;font-weight:800;color:var(--acc);">${NET}</div></div>
    <div><div class="mute" style="font-size:11px;text-transform:uppercase;">Cap</div><div style="font-size:24px;font-weight:800;">{CAP}%</div></div>
    <div><div class="mute" style="font-size:11px;text-transform:uppercase;">ROI</div><div style="font-size:24px;font-weight:800;">{ROI}</div></div>
  </div>"""
    return {"cards": cards, "band": band, "big": big}[stat]


BODY = """
  <div style="padding:6px 30px 26px;">
    <h2>Income &amp; Occupancy</h2>
    <table>
      <tr><th>Rent Source</th><th>Units</th><th>Rate</th><th class="r">Monthly</th></tr>
      <tr><td>Section 8 (BMHA 14201 payment standard)</td><td>4</td><td>$1,099&ndash;$1,297</td><td class="r">$4,792</td></tr>
      <tr><td>Market renters</td><td>5</td><td>$1,000&ndash;$1,250</td><td class="r">$5,500</td></tr>
      <tr class="total"><td>Gross Potential Rent</td><td>9</td><td class="r">&mdash;</td><td class="r">$10,292</td></tr>
      <tr><td colspan="3">Vacancy &amp; collection loss (4% blended)</td><td class="r">($410)</td></tr>
      <tr class="total"><td>Effective Gross Income</td><td colspan="2" class="r">&mdash;</td><td class="r">$9,880</td></tr>
    </table>
    <h2>Operating Expenses (annualized, incl. capital reserve)</h2>
    <table>
      <tr><th>Expense</th><th class="r">Annual</th></tr>
      <tr><td>Property taxes (Erie County)</td><td class="r">$6,000</td></tr>
      <tr><td>Insurance</td><td class="r">$7,200</td></tr>
      <tr><td>Water / sewer</td><td class="r">$4,050</td></tr>
      <tr><td>Maintenance &amp; repairs</td><td class="r">$8,100</td></tr>
      <tr><td>Turnover, legal, marketing</td><td class="r">$2,700</td></tr>
      <tr><td>Property management (8% of EGI)</td><td class="r">$9,485</td></tr>
      <tr><td>Capital reserve (roof / HVAC / appliances / paint)</td><td class="r">$13,500</td></tr>
      <tr class="total"><td>Total Operating Expenses</td><td class="r">$51,035</td></tr>
    </table>
    <h2>Net Operating Income &amp; Cap Rate</h2>
    <table>
      <tr><th>Metric</th><th class="r">Value</th></tr>
      <tr><td>NOI (before reserves)</td><td class="r">$81,029 / yr</td></tr>
      <tr><td>Net cash after reserves (producible)</td><td class="r">$67,529 / yr ($5,627 / mo)</td></tr>
      <tr class="total"><td>Offering Price</td><td class="r">$565,000</td></tr>
      <tr><td>Cap rate (after reserves)</td><td class="r">{CAP}%</td></tr>
      <tr><td>Price per unit (9 units)</td><td class="r">$62,778</td></tr>
    </table>
    <h2>Investor ROI &mdash; the floor is 20%, the standard is 40%</h2>
    <table>
      <tr><th>Path</th><th class="r">Cash in</th><th class="r">ROI (cash-on-cash)</th></tr>
      <tr><td>Conventional bank deal &mdash; 20% down @ 8%, 30yr</td><td class="r">$113,000</td><td class="r">{ROI_BANK}</td></tr>
      <tr class="total"><td>Creative &mdash; 8% down, seller-financed @ 5.5%, 30yr</td><td class="r">$45,200</td><td class="r">{ROI}</td></tr>
    </table>
    <p class="note">Creative structure uses <b>60% less cash</b> ($67,800 saved) and nearly <b>triples the return</b> &mdash; this deal clears the 40% standard.</p>
    <div class="cta"><b>Entry terms</b>: cash, subject-to, or seller financing. Current pricing and full rent roll on request.
      <br><a class="btn" href="mailto:jaison@onecompasspoint.com">Request Pricing &amp; Rent Roll</a></div>
    <p class="warn">Evaluation summary, not an offer. Figures are projections from current market rents (4 Section 8 at BMHA 14201 + 5 market) with a $1,500/unit annual capital reserve; actuals depend on inspection, tax review, and lease conditions.</p>
    <div class="foot">One Compass Point &middot; Investor Priced Real Estate</div>
  </div>
"""


def build(n, palette, hero, stat, typ):
    css = css_base(palette, hero, stat, typ)
    return f"<!doctype html><html lang=en><head><meta charset=utf-8><title>OM-{n:02d} | {TITLE}</title><style>{css}</style></head><body><div class=\"sheet\">{hero_html(hero, palette)}{stats_html(stat)}{BODY}</div></body></html>"


def onyx(metal, acc, acc2, shine):
    """Dark gray paper + shimmering metallic signature."""
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><title>Onyx {metal} | {TITLE}</title><style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Playfair Display', Georgia, serif; background:#191b1f; color:#e9e6de; padding:22px; }}
  .sheet {{ max-width:920px; margin:0 auto; background:
      radial-gradient(1200px 500px at 20% -10%, #25272d 0%, #191b1f 55%);
      border:1px solid #2c2e34; border-radius:18px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.55); }}
  .metallic {{ background:linear-gradient(100deg, {acc2} 0%, {acc} 30%, #f5ecdc 50%, {acc} 70%, {acc2} 100%);
    -webkit-background-clip:text; background-clip:text; color:transparent; }}
  .shine {{ position:relative; overflow:hidden; }}
  .shine::after {{ content:""; position:absolute; top:-40%; bottom:-40%; left:-60%; width:45%;
    background:linear-gradient(100deg, transparent 0%, rgba(255,255,255,.16) 50%, transparent 100%);
    transform:skewX(-18deg); animation:shimmer 5.5s infinite; }}
  @keyframes shimmer {{ 0% {{ left:-60%; }} 60% {{ left:130%; }} 100% {{ left:130%; }} }}
  .head {{ position:relative; padding:30px 34px; background:linear-gradient(180deg, #1f2126, transparent); border-bottom:1px solid #2c2e34; }}
  .brand {{ font-size:13px; letter-spacing:3px; text-transform:uppercase; color:#8f939b; }}
  .brand b {{ color:{acc}; }}
  h1 {{ font-size:27px; margin-top:16px; color:#f4f1e8; }}
  .sub {{ color:#9ba0a8; font-size:13px; margin-top:5px; }}
  .price {{ text-align:right; }}
  .massive {{ font-size:40px; font-weight:800; line-height:1; }}
  .grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; padding:20px 34px 0; }}
  .stat {{ background:linear-gradient(180deg,#23252b,#1c1e23); border:1px solid #34373e; border-radius:12px; padding:14px 16px; }}
  .stat .k {{ font-size:10px; letter-spacing:1.4px; text-transform:uppercase; color:#8f939b; }}
  .stat .v {{ font-size:24px; font-weight:800; margin-top:5px; }}
  .body {{ padding:8px 34px 28px; }}
  h2 {{ font-size:15px; color:{acc}; margin:22px 0 10px; border-bottom:1px solid #33353c; padding-bottom:7px; letter-spacing:.3px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; color:#dcdcd4; }}
  th {{ text-align:left; color:#8f939b; font-size:10px; text-transform:uppercase; letter-spacing:1px; padding:8px 10px; border-bottom:1px solid #33353c; }}
  td {{ padding:9px 10px; border-bottom:1px solid #27292e; }}
  .r {{ text-align:right; }} .total td {{ border-top:2px solid {acc2}; font-weight:800; color:#f2efe6; }}
  .note {{ font-size:12px; color:#9ba0a8; margin-top:8px; line-height:1.5; }}
  .cta {{ margin-top:22px; background:linear-gradient(180deg,#23252b,#1b1d22); border:1px solid #3a3d45; border-radius:12px; padding:16px 18px; }}
  .btn {{ display:inline-block; background:linear-gradient(100deg,{acc2},{acc}); color:#14161a; font-weight:900; padding:11px 22px; border-radius:9px; margin-top:10px; text-decoration:none; }}
  .warn {{ font-size:11px; color:#7d828b; margin-top:12px; font-style:italic; }}
  .foot {{ font-size:11px; color:#6f747d; margin-top:20px; text-align:center; letter-spacing:1px; }}
  @media print {{ body{{background:#191b1f;padding:0;}} .shine::after{{display:none;}} }}
</style></head><body><div class="sheet">
  <div class="head shine">
    <div class="brand">One Compass <b>Point</b> &middot; Investor Priced Real Estate</div>
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin-top:10px;">
      <div><h1>{TITLE}</h1><div class="sub">{SUB}</div></div>
      <div class="price"><div class="mute" style="font-size:10px;letter-spacing:1.5px;color:#8f939b;">OFFERING PRICE</div><div class="massive metallic">${PRICE}</div></div>
    </div>
  </div>
  <div class="grid">
    <div class="stat"><div class="k">Net Cash / Yr (after reserves)</div><div class="v metallic">${NET}</div></div>
    <div class="stat"><div class="k">Cap Rate</div><div class="v metallic">{CAP}%</div></div>
    <div class="stat"><div class="k">Investor ROI @ Asking</div><div class="v metallic">{ROI}</div></div>
  </div>
  <div class="body">{BODY.replace('<div class="cta">', '').replace('</div>', '</div>', 1)}</div>
  <div class="foot" style="padding-bottom:20px;">ONE COMPASS POINT &mdash; DIAMOND IN THE ROUGH</div>
</div></body></html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    written = []
    combos = 0
    for i in range(50):
        pal = PALETTES[i % 12]
        hero = HEROES[(i // 12) % 5]
        stat = STATS[(i // 60) % 3]
        typ = TYPES[(i // 180) % 3]
        fn = f"om-{i+1:02d}.html"
        open(os.path.join(OUT, fn), "w").write(build(i + 1, pal, hero, stat, typ))
        written.append(fn)
    # Onyx signatures: (metal, light, dark, accent2)
    onyx_variants = [
        ("Gold",   "#d8b256", "#8a6d1f", "#f2e6c2"),
        ("Silver", "#c9cdd4", "#7d828b", "#eceff3"),
        ("Bronze", "#c0834a", "#7a4a24", "#ecdcc3"),
    ]
    for metal, a1, a2, sh in onyx_variants:
        fn = f"onyx-{metal.lower()}.html"
        open(os.path.join(OUT, fn), "w").write(onyx(metal, a1, a2, sh))
        written.append(fn)
    print("wrote", len(written), "templates ->", OUT)


if __name__ == "__main__":
    main()