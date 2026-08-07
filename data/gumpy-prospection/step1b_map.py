"""Étape 1b : nettoyage liste + map des URLs annuaire-mairie depuis les pages département."""
import pandas as pd
import re
import unicodedata
import json
from bs4 import BeautifulSoup

def norm(name: str) -> str:
    """Normalise un nom de commune pour matching."""
    s = name.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("'", " ").replace("-", " ").replace("’", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # enlève mentions entre parenthèses
    s = re.sub(r"\(.*?\)", "", s).strip()
    return s

df = pd.read_json("/opt/data/prospecting_mairies/communes_2000.json")
# retirer lignes département
df = df[~df["commune"].str.lower().isin(["savoie", "haute-savoie"])].copy()
# nettoyer nom : retirer "(préfecture)" etc.
df["commune"] = df["commune"].str.replace(r"\s*\(.*?\)\s*", "", regex=True).str.strip()
df["slug"] = df["commune"].apply(
    lambda n: re.sub(r"-+", "-", unicodedata.normalize("NFD", n.lower()).encode("ascii", "ignore").decode().replace("'", "-").replace(" ", "-"))
)
df["norm"] = df["commune"].apply(norm)
df = df.reset_index(drop=True)
print(f"Communes >= 2000 hab (nettoyées) : {len(df)}")

# --- build URL map from dept pages ---
url_map = {}
for dept, f in [("73", "/opt/data/prospecting_mairies/wiki_73.html"), ("74", "/opt/data/prospecting_mairies/wiki_74.html")]:
    pass  # les pages dept ne sont pas encore téléchargées

# Télécharger les pages département annuaire-mairie
import urllib.request
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
for dept, url in [("73", "https://www.annuaire-mairie.fr/departement-savoie.html"),
                  ("74", "https://www.annuaire-mairie.fr/departement-haute-savoie.html")]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    open(f"/opt/data/prospecting_mairies/annuaire_dept_{dept}.html", "w").write(html)
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all("a", href=re.compile(r"/(mairie|ville)-[a-z0-9-]+\.html"))
    for a in links:
        name = a.get_text(strip=True)
        href = a["href"]
        if name:
            url_map[norm(name)] = (name, href)
    print(f"Dept {dept}: {len(links)} liens mairie/ville dans la page")

# assigner URL aux communes
df["url_annuaire"] = df["norm"].map(lambda n: url_map.get(n, (None, None))[1])
df["nom_annuaire"] = df["norm"].map(lambda n: url_map.get(n, (None, None))[0])
missing = df[df["url_annuaire"].isna()]
print(f"\nCommunes sans URL trouvée : {len(missing)}")
for _, r in missing.iterrows():
    print("  MISS:", r["dept"], r["commune"], "| norm:", r["norm"])

df.drop(columns=["norm"]).to_json("/opt/data/prospecting_mairies/communes_clean.json", orient="records", force_ascii=False)
print("\nSauvé communes_clean.json")
