# AGENTS.md — schema du wiki (pour Hermes et tout agent futur)

Ce fichier est le **schema** du wiki (cf. précos LLM Wiki de Karpathy). Il définit comment
le wiki est structuré, les conventions et les workflows. Le lire AVANT toute modification.

## Structure

```
llm-wiki/
├── AGENTS.md      ← ce fichier (le schema)
├── README.md      ← accueil + mode d'emploi pour Chris
├── log.md         ← journal chronologique append-only
├── wiki/          ← les pages (couche possédée par l'agent)
│   ├── index.md   ← catalogue : lien + résumé 1 ligne + métadonnées, à jour à CHAQUE modification
│   └── <topic>/   ← finance, energie, maison, dev, recherche, reconversion, mecanique, gumpy
├── data/          ← données brutes par projet (immuables, backup)
└── sources/       ← sources externes (immuables)
```

## Règles d'or

1. **Sources obligatoires** : toute page a une section `## Sources` (lien + date).
   Aucun fait sans source. On ne devine pas, on ne recopie pas sans vérifier.
2. **Wiki = couche agent** : l'agent crée/met à jour les pages ; Chris lit et guide.
3. **data/ et sources/ sont immuables** : on lit, on ne modifie jamais. On ajoute.
4. **Langue** : français (les titres techniques peuvent rester en anglais).
5. **Push direct main autorisé** (dérogation explicite de Chris pour CE repo).
6. **Pages vivantes** : une page par sujet, à jour — PAS d'empilement par date dans wiki/
   (l'historique vit dans git). Les livrables ponctuels datés vont dans `rapports/` ou `data/`.

## Workflow Ingest (nouvelle source / nouveau sujet)

1. Lire la source (web, fichier, session, skill) — ne jamais inventer
2. Si pertinent : copier la donnée brute dans `data/<projet>/` (immuable)
3. Créer/mettre à jour la page dans `wiki/<topic>/`
4. Mettre à jour `wiki/index.md` (résumé 1 ligne + métadonnées)
5. Ajouter une entrée dans `log.md` : `## [AAAA-MM-JJ] ingest | Titre`
6. Commit + push

## Workflow Query (Chris demande une info)

1. Lire `wiki/index.md` pour repérer les pages pertinentes
2. Lire les pages, synthétiser AVEC citations (liens vers les pages/sources)
3. Si la réponse est bonne et durable → en faire une page (workflow ingest)

## Workflow Lint (health-check)

Vérifier périodiquement : contradictions entre pages, claims périmés, pages orphelines,
concepts sans page, cross-réfs manquantes, data gaps. Corriger + logger.
