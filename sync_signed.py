#!/usr/bin/env python3
"""One Compass Point - signed-deal auto-publisher (ver1)
Polls the PN kanban for Jaison's (Orion HQ) opportunities in status='signed',
writes them to properties.json newest-first, adds satellite imagery when a
deal has no photos, pulls Google Drive photo folders queued from the site,
and commits to the repo so the site updates passively.
Run by cron; also run manually. Idempotent (no commit if unchanged)."""
import io, json, math, os, re, subprocess, urllib.request

ENV = "/home/ubuntu/.hermes/.env"
SUPABASE_URL = "https://tooambsacmhrlgpwgwsv.supabase.co/rest/v1"
ORION = "f2614863-5b4d-411e-a828-e9fa574c27de"
REPO = "/home/ubuntu/onecompass-deploy"
NINE_UNIT_PHOTOS = "photos/busti9"       # 9-unit (387 Busti Ave) gallery
NINE_UNIT_COVER = "main_9unit.jpg"      # main/hero photo for the listing
SAT_DIR = "photos/sat"
ESRI_TILE = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"

def svc_key():
    for line in open(ENV):
        if line.startswith("SUPABASE_SERVICE_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("no service key")

def fetch(url):
    key = svc_key()
    req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
    return json.load(urllib.request.urlopen(req, timeout=40))

def patch(url, payload):
    key = svc_key()
    req = urllib.request.Request(url, method="PATCH", data=json.dumps(payload).encode(),
        headers={"apikey": key, "Authorization": "Bearer " + key, "Content-Type": "application/json",
                 "Prefer": "return=minimal"})
    return urllib.request.urlopen(req, timeout=40).status

def pull(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (OCP publisher)"})
    return urllib.request.urlopen(req, timeout=40).read()

def wgs84_to_tile(lat, lng, z):
    lat_r = math.radians(lat)
    n = 2.0 ** z
    x = (lng + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(lat_r)) / math.pi) / 2.0 * n
    return x, y

def satellite_photo(opp_id, lat, lng):
    """Compose an Esri World Imagery satellite crop around the property -> local jpg."""
    try:
        from PIL import Image
    except Exception:
        return None
    if lat is None or lng is None:
        return None
    os.makedirs(os.path.join(REPO, SAT_DIR), exist_ok=True)
    z = 17                      # street-level aerial
    size = 640                  # output px
    tx, ty = wgs84_to_tile(lat, lng, z)
    # center tile + fractional offset
    cx, cy = int(tx), int(ty)
    fx, fy = tx - cx, ty - cy
    span = 3                     # 3x3 tiles to cover the crop
    canvas = Image.new("RGB", (256 * span, 256 * span))
    for dy in range(span):
        for dx in range(span):
            txx, tyy = cx + dx - 1, cy + dy - 1
            if txx < 0 or tyy < 0:
                continue
            try:
                tile = Image.open(io.BytesIO(pull(ESRI_TILE.format(z=z, x=txx, y=tyy)))).convert("RGB")
                canvas.paste(tile, (dx * 256, dy * 256))
            except Exception:
                continue
    # center the exact lat/lng in the crop
    pixel_x = int((fx + 1) * 256) - size // 2
    pixel_y = int((fy + 1) * 256) - size // 2
    pixel_x = max(0, min(canvas.width - size, pixel_x))
    pixel_y = max(0, min(canvas.height - size, pixel_y))
    crop = canvas.crop((pixel_x, pixel_y, pixel_x + size, pixel_y + size))
    out = os.path.join(REPO, SAT_DIR, opp_id + ".jpg")
    crop.save(out, "JPEG", quality=82)
    return "/" + SAT_DIR + "/" + opp_id + ".jpg"

def drive_folder_id(link):
    m = re.search(r"(?:folders|drive/folders)/([\w-]{10,})", link or "")
    return m.group(1) if m else None

def process_drive_links(listings):
    """Pull queued Google Drive photo links posted by the site (page_leads metadata),
    download each folder, host it locally, append photos to the matching listing."""
    try:
        rows = fetch(f"{SUPABASE_URL}/page_leads?select=id,name,message,metadata&limit=100")
    except Exception as e:
        print("drive-link scan failed:", e)
        return
    for row in rows:
        md = row.get("metadata") or {}
        if md.get("kind") != "ocp_drive_link" or md.get("status") == "done":
            continue
        folder = drive_folder_id(md.get("drive_link") or row.get("message") or "")
        if not folder:
            patch(f"{SUPABASE_URL}/page_leads?id=eq.{row['id']}",
                  {"metadata": {**md, "status": "bad_link"}})
            continue
        addr = (md.get("address") or row.get("name") or "").strip().lower()
        target = None
        for L in listings:
            if (L.get("address") or "").strip().lower() == addr:
                target = L
                break
        if not target:
            patch(f"{SUPABASE_URL}/page_leads?id=eq.{row['id']}",
                  {"metadata": {**md, "status": "no_match"}})
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", addr)[:40] or "deal"
        dest = os.path.join(REPO, "photos", slug)
        os.makedirs(dest, exist_ok=True)
        try:
            pull_drive_folder(folder, dest)
        except Exception as e:
            print("gdown failed for", folder, e)
            patch(f"{SUPABASE_URL}/page_leads?id=eq.{row['id']}",
                  {"metadata": {**md, "status": "download_failed"}})
            continue
        names = sorted(n for n in os.listdir(dest) if n.lower().endswith((".jpg", ".jpeg", ".png")))
        if not names:
            patch(f"{SUPABASE_URL}/page_leads?id=eq.{row['id']}",
                  {"metadata": {**md, "status": "no_images"}})
            continue
        base = "/photos/" + slug + "/"
        target["photos"] = [base + n for n in names] + [p for p in target.get("photos", []) if not p.startswith(base)]
        patch(f"{SUPABASE_URL}/page_leads?id=eq.{row['id']}",
              {"metadata": {**md, "status": "done", "added": len(names)}})
        print(f"drive link applied: {len(names)} photos to {target['address']}")

def pull_drive_folder(folder_id, dest):
    import shutil
    gdown = os.path.expanduser("~/.local/bin/gdown")
    try:
        subprocess.run([gdown, "--folder", f"https://drive.google.com/drive/folders/{folder_id}",
                        "--remaining-ok"], cwd=dest, check=True, timeout=300,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # fallback: plain gdown in a temp dir then move
        tmp = dest + "_tmp"
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp, exist_ok=True)
        subprocess.run([gdown, "--folder", f"https://drive.google.com/drive/folders/{folder_id}",
                        "--remaining-ok"], cwd=tmp, check=True, timeout=300,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for f in os.listdir(tmp):
            shutil.move(os.path.join(tmp, f), os.path.join(dest, f))
        shutil.rmtree(tmp, ignore_errors=True)

def main():
    rows = fetch(f"{SUPABASE_URL}/opportunities?select=id,address,city,state,zip,title,property_type,units,beds,baths,sqft,photo_url,purchase_price,listing_price,manual_sell_price,arv,property_tax,status,created_at,closed_at,county,latitude,longitude,data&agency_id=eq.{ORION}&status=eq.signed&order=closed_at.desc")
    listings = []
    for r in rows:
        price = r.get("purchase_price") or r.get("listing_price") or r.get("manual_sell_price")
        closed = r.get("closed_at") or r.get("created_at") or ""
        units = r.get("units")
        ptype = r.get("property_type") or (f"{units}-Unit" if units else "")
        offering = (r.get("data") or {}).get("offering") or None
        photos = []
        cover = 0
        if "Busti" in (r.get("address") or ""):
            base = "/" + NINE_UNIT_PHOTOS + "/"
            names = sorted(os.listdir(os.path.join(REPO, NINE_UNIT_PHOTOS)))
            photos = [base + n for n in names]
            if NINE_UNIT_COVER in names:
                cover = names.index(NINE_UNIT_COVER)
        elif r.get("photo_url"):
            photos = [r["photo_url"]]
        elif r.get("latitude") is not None and r.get("longitude") is not None:
            sat = satellite_photo(r["id"].replace("-", "")[:14], r["latitude"], r["longitude"])
            if sat:
                photos = [sat]
        # google drive links queued from the site
        listings.append({
            "id": r["id"],
            "title": r.get("title") or (ptype if ptype else r.get("address", "")),
            "address": r.get("address"),
            "city": r.get("city"),
            "state": r.get("state"),
            "zip": r.get("zip"),
            "county": r.get("county"),
            "property_type": ptype,
            "units": units,
            "beds": r.get("beds"),
            "baths": r.get("baths"),
            "sqft": r.get("sqft"),
            "price": price,
            "arv": r.get("arv"),
            "property_tax": r.get("property_tax"),
            "closed": (closed or "")[:10],
            "photos": photos,
            "cover": cover,
            "offering": offering,
        })
    process_drive_links(listings)
    # drop the internal id before publishing
    for L in listings:
        L.pop("id", None)
    path = os.path.join(REPO, "properties.json")
    old = ""
    if os.path.exists(path):
        old = open(path, encoding="utf-8").read()
    new = json.dumps(listings, indent=2)
    open(path, "w", encoding="utf-8").write(new)
    # also bake the deals into properties.html so the page renders with no network fetch
    phr = os.path.join(REPO, "properties.html")
    if os.path.exists(phr):
        ph = open(phr, encoding="utf-8").read()
        # always refresh the inline deals (regex, standalone line) - a one-shot
        # marker replaced once left the inline stale on later runs.
        _nb = re.subn(r"window\.OCP_DEALS = \[.*?\];",
                      "window.OCP_DEALS = " + json.dumps(listings, ensure_ascii=False) + ";",
                      ph, count=1, flags=re.S)
        if _nb[1]:
            open(phr, "w", encoding="utf-8").write(_nb[0])
    print(f"signed listings: {len(listings)}  (newest first)")
    if old == new:
        print("properties.json unchanged - nothing to publish")
        return
    subprocess.run(["git", "-C", REPO, "add", "properties.json", "properties.html", "photos"], check=False)
    env = dict(os.environ, GIT_AUTHOR_NAME="OCP Auto", GIT_AUTHOR_EMAIL="jxnvst@users.noreply.github.com",
               GIT_COMMITTER_NAME="OCP Auto", GIT_COMMITTER_EMAIL="jxnvst@users.noreply.github.com")
    subprocess.run(["git", "-C", REPO, "commit", "-q", "-m", f"auto-publish: {len(listings)} deal(s)"], env=env, check=False)
    p = subprocess.run(["git", "-C", REPO, "push", "-q", "origin", "main"], env=env, capture_output=True, text=True)
    print("pushed" if p.returncode == 0 else "push issue: " + p.stderr[-200:])

if __name__ == "__main__":
    main()