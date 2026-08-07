# Catalogue de cours vacataire (data / devops / IA / agilité)

Source : skill `vacataire-enseignement-superieur` (août 2026). Version wiki = archive lisible.

## Cadre légal (public)

- Décret n° 87-889 du 29/10/1987 — condition d'activité principale : ≥ 900 h/an OU moyens d'existence réguliers (cas indépendant → DC Consulting ✅)
- Plafond : **300 h éq-TD max par an**
- Écoles privées : pas de formalisme — CV + dispo + module crédible

## Règle d'or

Ne jamais proposer 8 cours séparés → **packager en offres** (voir plus bas). Un projet fil rouge par cours, évalué en continu.

## BLOC 1 — Socle (porte d'entrée, gros volume horaire)

1. **Python pour l'ingénierie moderne** — BUT1-2, BTS SIO, bachelor 1-2 · 30-40h · zéro prérequis. Fil rouge : CLI livré + tests + CI verte. uv/venv/pyproject/ruff, POO utile, pytest + GitHub Actions, API/CLI, packaging.
2. **Conteneurisation Docker → Kubernetes** — BUT2-3, licence pro, bachelor 3 · 24-30h. Fil rouge : déployer l'appli du cours 1 sur cluster local (k3d/kind). Dockerfile multi-stage, compose, sécurité image, K8s (pods/deployments/services/ingress/secrets/probes), Helm **ou** Kustomize (un seul).
3. **DevOps, CI/CD & IaC** — BUT3, licence pro, M1, cycle ingé · 24-30h. Fil rouge : pipeline complet jusqu'au déploiement auto. DORA metrics, Git avancé/trunk-based, pipelines build→test→scan→deploy, Terraform **ou** Ansible, GitOps (ArgoCD), observabilité.
4. **Gestion de projet & agilité (socle)** — BUT, BTS SIO, bachelors, écoles non-info (GEA, commerce) · 24-30h. Cadrage, V vs itératif, Scrum, backlog & user stories, estimation + dérives, Kanban, simulation de 2 sprints (Chris en SM), rétro, restitution. Éval : backlog + soutenance.
4bis. **Rôle Product Owner & posture Scrum Master** — bachelor 3, M1/M2, MSc management · 16-20h. Vécu réel (missions SM + coaching PO). Servant leader, 5 erreurs récurrentes du PO, priorisation (MoSCoW, WSJF), Scrum-but, métriques saines (DORA, flow), SAFe/LeSS. Éval : mise en situation jouée/filmée + auto-analyse.

## BLOC 2 — Différenciation (courts, forte valeur, peu d'intervenants)

5. **LLMOps : LLM en production** — M1/M2, cycle ingé 4-5, MSc · 20h. API vs self-hosted, gateway & routing (REX bancaire), RAG (chunking/embeddings/hybrid search), évaluation (golden set), observabilité/coûts/multi-tenant. Réutilise assets code-search et arxiv-watchdog.
6. **Agents IA & protocole MCP** — M2, cycle ingé 5, MSc · 12-16h. Agent vs chaîne vs workflow, tool calling/ReAct, MCP (architecture, serveurs, RBAC), human-in-the-loop. Matériel existant : slides, deep-engine, pydanticai-deep-agents.
7. **Sécurité des systèmes IA** — M2, spécialité cyber, cycle ingé · 12-16h. OWASP Top 10 LLM, prompt injection, guardrails, isolation multi-tenant. Éval : red team d'une appli LLM + rapport de remédiation.
8. **Inférence & dimensionnement GPU** — M2, cycle ingé 5, séminaire · 8-12h. KV cache, batching, quantization, serveurs d'inférence, benchmark/sizing mesuré. TP clé en main : genai-benchmark-tool.

## BLOC 2 bis — proposé (à valider)

9. **IA & transformation du travail** — 12-16h, zéro prérequis technique · écoles de management, IAE, MSc, formation continue. Panorama IA générative, cas d'usage par métier (marketing, finance, RH, juridique), limites (hallucinations, biais, confidentialité), AI Act, impact emploi/compétences, conduite du changement. Format 50% apports + 50% ateliers (prompt engineering appliqué, détection d'erreurs). Différenciateur : vécu réel (LLM en prod, agents MCP, RAG).

## BLOC 3 — À ne pas viser en premier

- ML/deep learning théorique en Master IA (Lyon 1, INSA) : chasse gardée des titulaires, entrée par cooptation seulement.

## Packaging (offres à proposer)

1. **Socle infra** : cours 2 + 3
2. **Socle dev/projet** : cours 1 + 4
3. **Spécialisation IA** : cours 5 + 6 (+ 7 option)
4. **Projet & agilité** : cours 4 + 4bis ← meilleur ticket d'entrée (marché hors info : écoles de commerce, IAE, GEA, MSc management ; formation continue = 2-4× la vacation)

## Stratégie

- **Bloc 1 pour entrer et faire du volume ; bloc 2 comme argument de recrutement** (« je peux aussi ouvrir un module IA que personne ne couvre »). L'inverse ne marche pas.
- **Faire UN cours d'abord** — la 1ère année valide le format et génère les recommandations internes. Les vacations se renouvellent par bouche-à-oreille.
- Certification PSM I/II/PSPO seulement si un dossier administratif bloque (pas avant).
- Tradeoff : bloc 1 = volume/stabilité mais correction chronophage ; bloc 2 = valorisant, peu de volume, mais ouvre formation continue/entreprises mieux payées.
- Saison : candidatures spontanées idéalement **mai-juin** (maquettes de rentrée).

## Sources

- Skill `vacataire-enseignement-superieur` (catalogue + cadre légal), août 2026
- Décret n° 87-889 du 29/10/1987 — legifrance.gouv.fr
- « IA & transformation du travail » : proposition discutée en session 08/2026 (à valider)

## Liens

- → [Reconversion](index.md) · [Établissements](vacataire-etablissements.md) · [Index](../index.md)
