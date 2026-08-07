"""Step A : communes ≥2000 hab dans un rayon de 50 km autour de Belleville-sur-Saône (46.1089, 4.7489).
Source population+coordonnées : geo.api.gouv.fr (populations INSEE). Distance : haversine.
"""
import json
import math
import re
import unicodedata
import urllib.request

CENTER = (46.1089, 4.7489)  # lat, lon Belleville
RADIUS = 50_000  # m
MIN_POP = 2000
DEPTS = ["69", "01", "71", "42", "38"]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def slugify(name: str) -> str:
    s = unicodedata.normalize("NFD", name.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("'", "-").replace(" ", "-")
    return re.sub(r"-+", "-", s)

def norm(name: str) -> str:
    s = name.lower()
    s = s.replace("'", " ").replace("-", " ").replace("’", " ")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"\s+", " ", s).strip()

communes = []
for d in DEPTS:
    url = f"https://geo.api.gouv.fr/communes?codeDepartement={d}&fields=nom,code,population,centre&limit=500"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research)"})
    data = json.load(urllib.request.urlopen(req, timeout=60))
    print(f"Dept {d}: {len(data)} communes récupérées")
    for c in data:
        if not c.get("centre") or c.get("population") is None:
            continue
        lat, lon = c["centre"]["coordinates"][1], c["centre"]["coordinates"][0]
        dist = haversine(CENTER[0], CENTER[1], lat, lon)
        if dist <= RADIUS and c["population"] >= MIN_POP:
            communes.append({
                "commune": c["nom"], "dept": d, "code_insee": c["code"],
                "population": c["population"], "distance_km": round(dist / 1000, 1),
                "slug": slugify(c["nom"]), "norm": norm(c["nom"]),
            })

communes.sort(key=lambda x: x["distance_km"])
print(f"\nCommunes >= {MIN_POP} hab dans {RADIUS/1000:.0f} km : {len(communes)}")

# --- URL map annuaire-mairie depuis les pages département ---
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
from bs4 import BeautifulSoup
url_map = {}
for d in sorted(set(c["dept"] for c in communes)):
    dept_names = {"69": "rhone", "01": "ain", "71": "saone-et-loire", "42": "loire", "38": "isere"}
    page = f"https://www.annuaire-mairie.fr/departement-{dept_names[d]}.html"
    req = urllib.request.Request(page, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    open(f"/opt/data/prospecting_mairies/annuaire_dept_{d}.html", "w").write(html)
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a", href=re.compile(r"/(mairie|ville)-[a-z0-9-]+\.html")):
        name = a.get_text(strip=True)
        if name:
            url_map[norm(name)] = a["href"]
    print(f"Dept {d}: page téléchargée, {len([k for k in url_map])} entrées cumulées")

missing = []
for c in communes:
    c["url_annuaire"] = url_map.get(c["norm"])
    if not c["url_annuaire"]:
        missing.append(c["commune"])
print("Sans URL :", missing if missing else "aucune")

json.dump(communes, open("/opt/data/prospecting_mairies/belleville_communes.json", "w"), ensure_ascii=False, indent=1)
print("\nExemples (plus proches) :")
for c in communes[:12]:
    print(f"  {c['distance_km']:>5} km | {c['commune']} ({c['dept']}) | {c['population']} hab | {c['url_annuaire']}")
