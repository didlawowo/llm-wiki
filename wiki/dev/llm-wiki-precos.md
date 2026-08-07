# Précos du LLM Wiki de Karpathy — et où on en est

Source : [gist de Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (04/2026), lu le 07/08/2026.

## L'idée centrale

La plupart des usages LLM + documents = **RAG** : on uploade des fichiers, le LLM récupère des bouts à chaque question, et **redécouvre la connaissance à zéro à chaque fois**. Rien ne s'accumule.

L'idée Karpathy : le LLM **construit et maintient incrémentalement un wiki persistant** — une collection structurée et liée de fichiers markdown, entre toi et les sources brutes. La connaissance est **compilée une fois puis tenue à jour**, pas re-dérivée à chaque requête. Le wiki est un **artefact persistant qui compose** (compounding) : chaque source ajoutée, chaque question posée l'enrichit.

> Obsidian est l'IDE, le LLM est le programmeur, le wiki est le codebase.
> Toi (l'humain) : sourcer, explorer, poser les bonnes questions, réfléchir. Le LLM : tout le reste (résumés, cross-réfs, classement, bookkeeping).

## Architecture — 3 couches

| Couche | Rôle | Règle |
|---|---|---|
| **Raw sources** | ta collection de documents source (articles, papers, données) | **Immuables** — le LLM lit mais ne modifie JAMAIS. C'est la source de vérité |
| **The wiki** | répertoire de markdown généré par le LLM (résumés, pages entités/concepts, comparaisons, synthèse) | Le LLM **possède** cette couche : crée, met à jour, maintient les liens, garde la cohérence. Toi tu lis |
| **The schema** | un document (CLAUDE.md / AGENTS.md) qui dit au LLM la structure, les conventions, les workflows | **Le fichier clé** — c'est ce qui fait de l'agent un mainteneur discipliné plutôt qu'un chatbot générique. À co-évoluer |

## Operations

### Ingest (intégration d'une source)
Déposer une nouvelle source dans raw → dire au LLM de la traiter :
1. Lire la source
2. Discuter des takeaways avec toi
3. Écrire une page résumé
4. Mettre à jour l'index
5. Mettre à jour les pages entités/concepts concernées
6. Ajouter une entrée au log
> Une seule source peut toucher **10-15 pages**. Préférer l'ingestion **une à une** avec supervision.

### Query (question)
- Le LLM cherche les pages pertinentes (l'index d'abord), les lit, synthétise **avec citations**
- **Les bonnes réponses se re-filent dans le wiki** : une comparaison, une analyse, une connexion découverte → nouvelle page. Tes explorations composent comme les sources.

### Lint (health-check périodique)
Demander au LLM de vérifier :
- Contradictions entre pages
- Claims périmés (dépassés par des sources plus récentes)
- Pages orphelines (aucun lien entrant)
- Concepts importants mentionnés mais sans page dédiée
- Cross-références manquantes
- Data gaps comblables par une recherche web
> Le LLM est bon pour suggérer de nouvelles questions et sources.

## Indexing & logging — 2 fichiers spéciaux

### index.md (orienté contenu)
Catalogue de tout le wiki : chaque page avec **lien + résumé 1 ligne + métadonnées** (date, nombre de sources), organisé par catégorie. Mis à jour à **chaque ingest**. Pour répondre : lire l'index d'abord, puis creuser. À échelle moyenne (~100 sources, centaines de pages), ça **évite d'avoir besoin d'un RAG par embeddings**.

### log.md (orienté chronologie)
Journal **append-only** : ingests, queries, lint. Astuce : préfixe constant `## [2026-04-02] ingest | Titre` → parseable avec `grep "^## \[" log.md | tail -5`. Donne la timeline de l'évolution.

## Tips & outils

- **Obsidian Web Clipper** — convertit un article web en markdown directement dans raw/
- **Images locales** — télécharger les images d'un article dans `raw/assets/` (le LLM peut les voir ; un LLM ne lit pas les images inline en un seul passage → lire le texte puis les images séparément)
- **Graph view d'Obsidian** — la meilleure vue de la forme du wiki (hubs, orphelines)
- **Marp** — slides markdown générées depuis le wiki
- **Dataview** — requêtes sur le frontmatter YAML (tags, dates, counts)
- **Le wiki = un repo git de markdown** → versioning, branches, collaboration gratuits
- **qmd** — moteur de recherche local markdown (BM25/vectoriel + re-rank LLM), CLI + MCP server — utile quand l'index ne suffit plus

## Pourquoi ça marche

Le coût de maintenance (bookkeeping) tombe à ~zéro pour un LLM : mettre à jour une cross-ref, garder un résumé à jour, noter qu'une donnée contredit une ancienne, toucher 15 fichiers en un passage. **Les humains abandonnent les wikis parce que la maintenance pousse plus vite que la valeur.** Les LLM ne s'ennuient pas.

## Note finale de Karpathy

Tout est **optionnel et modulaire** — pick what's useful, ignore what isn't. Le document ne fait que communiquer le pattern ; c'est l'agent + l'humain qui instancient une version adaptée à leur domaine.

---

## Audit de notre implémentation (07/08/2026)

### ✅ En place
- **Repo git de markdown** (llm-wiki sur GitHub) — versioning gratuit
- **3 couches** : `data/` + `sources/` (raw immuables) / `wiki/` (pages) / `AGENTS.md` (schema, créé aujourd'hui)
- **index.md** (wiki/index.md) — enrichi avec résumés 1 ligne + métadonnées
- **Sources obligatoires** : chaque page a une section `## Sources` (lien + date) — au-delà de Karpathy, exigence de Chris
- **Ingest une à une** avec supervision (on le fait naturellement)

### ❌ Manquant → corrigé aujourd'hui
1. ~~Le schema~~ → **AGENTS.md** créé à la racine
2. ~~log.md~~ → **log.md** créé (append-only, préfixe `## [date] type | titre`)
3. ~~index enrichi~~ → **wiki/index.md** à jour avec résumés + métadonnées

### ⏳ Reste à faire
- **Lint périodique** — health-check du wiki (contradictions, orphelines, gaps). Idée : cron mensuel
- **Re-filer les bonnes réponses** — quand une réponse de chat est bonne, en faire une page
- **Frontmatter YAML** (tags, dates, source counts) sur les pages — utile si on passe sous Obsidian/Dataview
- **Obsidian côté Chris** — le meilleur navigateur du wiki (graph view)

## Liens

- → [Dev](index.md) · [Index](../index.md)
