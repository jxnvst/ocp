#!/usr/bin/env python3
"""One Compass Point - signed-deal auto-publisher (ver0)
Polls the PN kanban for Jaison's (Orion HQ) opportunities in status='signed',
writes them to properties.json newest-first, and commits to the repo so the
site updates passively whenever something is marked signed.
Run by cron; also run manually. Idempotent (no commit if unchanged)."""
import json, os, subprocess, sys, urllib.request

ENV = "/home/ubuntu/.hermes/.env"
SUPABASE_URL = "https://tooambsacmhrlgpwgwsv.supabase.co/rest/v1"
ORION = "f2614863-5b4d-411e-a828-e9fa574c27de"
REPO = "/home/ubuntu/onecompass-deploy"
NINE_UNIT_PHOTOS = "photos/busti9"       # 9-unit (387 Busti Ave) gallery
NINE_UNIT_COVER = "1793220531697.jpg"   # the 2nd photo = main photo

def svc_key():
    for line in open(ENV):
        if line.startswith("SUPABASE_SERVICE_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("no service key")

def fetch(url):
    key = svc_key()
    req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
    return json.load(urllib.request.urlopen(req, timeout=40))

def main():
    rows = fetch(f"{SUPABASE_URL}/opportunities?select=id,address,city,state,zip,title,property_type,units,beds,baths,sqft,photo_url,purchase_price,listing_price,manual_sell_price,arv,property_tax,status,created_at,closed_at,county&agency_id=eq.{ORION}&status=eq.signed&order=closed_at.desc")
    listings = []
    for r in rows:
        price = r.get("purchase_price") or r.get("listing_price") or r.get("manual_sell_price")
        closed = r.get("closed_at") or r.get("created_at") or ""
        units = r.get("units")
        ptype = r.get("property_type") or (f"{units}-Unit" if units else "")
        photos = []
        cover = 0
        # 9-unit (387 Busti): attach its gallery, 2nd photo is the main/hero
        if "Busti" in (r.get("address") or ""):
            base = "/" + NINE_UNIT_PHOTOS + "/"
            names = sorted(os.listdir(os.path.join(REPO, NINE_UNIT_PHOTOS)))
            photos = [base + n for n in names]
            if NINE_UNIT_COVER in names:
                cover = names.index(NINE_UNIT_COVER)
        elif r.get("photo_url"):
            photos = [r["photo_url"]]
        listings.append({
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
        })
    path = os.path.join(REPO, "properties.json")
    old = ""
    if os.path.exists(path):
        old = open(path, encoding="utf-8").read()
    new = json.dumps(listings, indent=2)
    open(path, "w", encoding="utf-8").write(new)
    print(f"signed listings: {len(listings)}  (newest first)")
    if old == new:
        print("properties.json unchanged - nothing to publish")
        return
    # commit + push
    subprocess.run(["git", "-C", REPO, "add", "properties.json", "photos/busti9"], check=False)
    env = dict(os.environ, GIT_AUTHOR_NAME="OCP Auto", GIT_AUTHOR_EMAIL="jxnvst@users.noreply.github.com",
               GIT_COMMITTER_NAME="OCP Auto", GIT_COMMITTER_EMAIL="jxnvst@users.noreply.github.com")
    subprocess.run(["git", "-C", REPO, "commit", "-q", "-m", f"auto-publish: {len(listings)} signed deal(s)"], env=env, check=False)
    p = subprocess.run(["git", "-C", REPO, "push", "-q", "origin", "main"], env=env, capture_output=True, text=True)
    print("pushed" if p.returncode == 0 else "push issue: " + p.stderr[-200:])

if __name__ == "__main__":
    main()