"""Ajoute l'arrondissement depuis Wikipedia pour segmentation secteur."""
import pandas as pd
import json
import re

df73 = pd.read_html("/opt/data/prospecting_mairies/wiki_73.html", header=0)[1]
df74 = pd.read_html("/opt/data/prospecting_mairies/wiki_74.html", header=0)[1]

def norm(name: str) -> str:
    s = name.lower()
    s = s.replace("'", " ").replace("-", " ").replace("’", " ")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"\s+", " ", s).strip()

arr = {}
for df in (df73, df74):
    for _, r in df.iterrows():
        name = re.sub(r"\[.*?\]", "", str(r["Nom"])).strip()
        arr[norm(name)] = str(r["Arrondissement"])

contacts = json.load(open("/opt/data/prospecting_mairies/contacts.json"))
for c in contacts:
    c["arrondissement"] = arr.get(norm(c["commune"]), "")

# fix Aix-les-Bains email (officiel : ville@mairie-aixlesbains.fr — confirmé par recherche web)
for c in contacts:
    if c["commune"] == "Aix-les-Bains":
        c["email"] = "ville@mairie-aixlesbains.fr"
        c["tel"] = "04 79 88 09 99"

json.dump(contacts, open("/opt/data/prospecting_mairies/contacts.json", "w"), ensure_ascii=False, indent=1)
print("Arrondissements ajoutés. Exemples :")
for c in contacts[:6]:
    print(" ", c["commune"], "→", c["arrondissement"])
