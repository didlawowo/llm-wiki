# LLM Wiki — la base de connaissances de Chris

Base de connaissances markdown, maintenue par Hermes et **consultable par toi** :
navigation, recherche GitHub, ou lecture directe. Inspiré du [LLM Wiki de Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) :
un savoir qui s'accumule et se relie, au lieu de documents jetables.

## Comment trouver l'info

1. **La carte** : commence par [wiki/index.md](wiki/index.md) — tout part de là.
2. **Recherche GitHub** : la barre de recherche en haut de page cherche dans tout le repo (contenu markdown inclus).
3. **En local** : `git clone` puis `grep -ri "sujet" .` — tout est du texte brut.
4. **Demande à Hermes** : « où est l'info sur X ? » → je te réponds avec le lien.

## Arborescence

```
llm-wiki/
├── wiki/          → la connaissance (une page par sujet, à jour)
│   ├── index.md   → carte des topics
│   ├── finance/   → msUSD, portefeuille, screener
│   ├── energie/   → solaire, conso, voiture
│   ├── maison/    → jardin, arrosage, Home Assistant
│   ├── dev/       → homelab, RKE2, GitOps, projets
│   ├── recherche/ → veille, analyses
│   └── gumpy/     → photobooth, prospection mairies
├── data/          → données brutes par projet (backup cluster)
│   └── gumpy-prospection/
└── sources/       → matière externe (articles, exports) — immuable
```

## Règles

- **Pages wiki** : à jour, le versioning vit dans git.
- **Données** (`data/`) : brutes, on n'écrase pas, on ajoute.
- **Rapports ponctuels** : datés `YYYY-MM-DD_sujet.ext`, dans `wiki/<topic>/` ou à la racine d'un projet.
- **Push** : exception accordée par Chris — Hermes pousse directement sur `main` pour ce repo.
- **Confidentialité** : repo privé, pas d'info perso sensible en clair au-delà de ce que Chris valide.
