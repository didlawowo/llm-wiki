"""Étape 2 (v2) : fetch annuaire-mairie + extraction contacts avec décodage Cloudflare data-cfemail."""
import json
import re
import time
import urllib.request
from bs4 import BeautifulSoup

DATA = json.load(open("/opt/data/prospecting_mairies/communes_clean.json"))
for c in DATA:
    if c["commune"] == "Eteaux":
        c["url_annuaire"] = "/mairie-etaux.html"

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
BASE = "https://www.annuaire-mairie.fr"

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Referer": "https://www.annuaire-mairie.fr/",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception:
        return None

def decode_cfemail(hexstr):
    """Décode un data-cfemail Cloudflare."""
    try:
        data = bytes.fromhex(hexstr)
    except ValueError:
        return None
    if len(data) < 2:
        return None
    key = data[0]
    return "".join(chr(b ^ key) for b in data[1:])

def clean_phone(t):
    return re.sub(r"\s+", " ", t).strip()

results, errors = [], []
for i, c in enumerate(DATA):
    slug = c["url_annuaire"]
    url = BASE + slug
    html = fetch(url)
    if not html:
        alt = slug.replace("/mairie-", "/ville-") if "/mairie-" in slug else slug.replace("/ville-", "/mairie-")
        html = fetch(BASE + alt)
        if html:
            slug = alt
        else:
            errors.append((c["commune"], "fetch failed"))
            results.append({**c, "email": None, "tel": None, "site": None})
            time.sleep(0.4)
            continue
    soup = BeautifulSoup(html, "lxml")

    # EMAIL : data-cfemail d'abord, puis mailto:, puis texte @
    email = None
    for el in soup.find_all(attrs={"data-cfemail": True}):
        dec = decode_cfemail(el["data-cfemail"])
        if dec and "@" in dec:
            email = dec
            break
    if not email:
        for a in soup.find_all("a", href=True):
            if "mailto:" in a["href"]:
                email = a["href"].replace("mailto:", "").split("?")[0].strip()
                break
    if not email:
        txt = soup.get_text(" ", strip=True)
        m = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", txt)
        if m:
            email = m.group(0)

    # TELEPHONE
    tel = None
    text = soup.get_text(" ", strip=True)
    m = re.search(r"((?:0\d(?:[\s.]\d{2}){4})|(?:\+33[\s.]?\d(?:[\s.]\d{2}){4}))", text)
    if m:
        tel = clean_phone(m.group(1))

    # SITE WEB mairie
    site = None
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if h.startswith("http") and "annuaire-mairie.fr" not in h \
           and not any(x in h for x in ["facebook.com", "instagram.com", "twitter.com", "linkedin.com", "google.", "goo.gl"]):
            site = h
            break

    results.append({**c, "email": email, "tel": tel, "site": site})
    if (i + 1) % 10 == 0:
        print(f"  ... {i+1}/{len(DATA)}")
    time.sleep(0.35)

print(f"\nTerminé. Erreurs : {len(errors)}")
for e in errors:
    print("  ERR:", e)
json.dump(results, open("/opt/data/prospecting_mairies/contacts.json", "w"), ensure_ascii=False, indent=1)
emails = sum(1 for r in results if r["email"])
tels = sum(1 for r in results if r["tel"])
sites = sum(1 for r in results if r["site"])
print(f"Emails : {emails}/{len(results)} | Tél : {tels}/{len(results)} | Sites : {sites}/{len(results)}")
