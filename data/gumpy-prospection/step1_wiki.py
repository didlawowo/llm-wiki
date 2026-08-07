"""Étape 1 : liste des communes 73 + 74 avec population (Wikipedia / INSEE)."""
import pandas as pd
import re
import unicodedata
import json

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
pages = {
    "73": "/opt/data/prospecting_mairies/wiki_73.html",
    "74": "/opt/data/prospecting_mairies/wiki_74.html",
}

def slugify(name: str) -> str:
    """Transforme un nom de commune en slug annuaire-mairie."""
    s = name.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")  # enlève accents
    s = s.replace("'", "-").replace(" ", "-")
    s = re.sub(r"-+", "-", s)
    return s

rows = []
for dept, url in pages.items():
    try:
        tables = pd.read_html(url, header=0)
    except Exception as e:
        print(f"ERREUR {dept}: {e}")
        continue
    print(f"--- {dept}: {len(tables)} tables")
    for i, t in enumerate(tables):
        cols = [str(c).strip() for c in t.columns]
        pop_col = None
        for c in cols:
            if re.search(r"pop", c, re.I):
                pop_col = c
                break
        name_col = None
        for c in cols:
            if re.search(r"commune|nom", c, re.I):
                name_col = c
                break
        if pop_col and name_col:
            print(f"  table {i}: cols={cols}")
            for _, r in t.iterrows():
                name = str(r[name_col])
                name = re.sub(r"\[.*?\]", "", name).strip()
                if not name or name == "nan":
                    continue
                pop_raw = str(r[pop_col])
                m = re.search(r"([\d\s\u00a0]+)", pop_raw.replace("\u202f", " "))
                if not m:
                    continue
                pop = int(m.group(1).replace(" ", "").replace("\u00a0", ""))
                if pop >= 2000:
                    rows.append({"dept": dept, "commune": name, "population": pop, "slug": slugify(name)})
            break

df = pd.DataFrame(rows).drop_duplicates(subset=["dept", "commune"]).sort_values(["dept", "population"], ascending=[True, False])
print(f"\nTotal communes >= 2000 hab : {len(df)}")
print(df.to_string(index=False))
df.to_json("/opt/data/prospecting_mairies/communes_2000.json", orient="records", force_ascii=False)
