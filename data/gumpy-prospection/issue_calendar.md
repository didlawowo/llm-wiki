## Contexte

Le micro-service `proton-reader` (Go, `go-proton-api`) gère aujourd'hui la lecture/envoi de mails ProtonMail. Objectif : étendre le service pour intégrer **Proton Calendar** — lire et, à terme, créer des événements — en réutilisant la session Proton existante.

## État des lieux (recherche du 04/08/2026)

- **Lecture** : `go-proton-api` supporte nativement les calendriers et événements, avec déchiffrement E2E (passphrase + keyring du calendrier). La session Proton existante suffit — **zéro nouvelle dépendance**.
- **Écriture** : la lib officielle ne fait **pas** de création d'événements. Seul chemin testé : `cheeseandcereal/proton-cal` (v0.1.2, Go) qui implémente le chiffrement E2E complet + écriture via l'API privée de Proton. Ses packages (`pkg/event`, `pkg/calendar`) sont importables proprement.
- **Contrainte majeure** : `proton-cal` exige **Go 1.26.1**, alors que `proton-reader` build en **Go 1.24** (Dockerfile `golang:1.24-alpine`). Importer cette lib = upgrade du toolchain + alignement de `gopenpgp` (v2.9 → v2.10), avec un risque de régression côté mail à couvrir par les tests existants.

## Options

1. **Intégrer `proton-cal` dans `proton-reader`** : lecture + écriture dans le même container, endpoints HTTP, une seule session Proton (upgrade Go 1.26 requis).
2. **Déployer `proton-cal` en pod séparé (MCP)** : ne touche pas à `proton-reader`, mais session Proton séparée + 2FA à gérer en plus.
3. **Commencer par la lecture seule** (go-proton-api natif, rapide et sans risque), écrire plus tard si besoin.

## Direction retenue

Commencer par la **lecture** (option 3) : sûr et réversible, pas d'upgrade Go. Branche `feat/proton-calendar` en préparation (à partir de `origin/main`).

## À faire

- [ ] Exposer la lecture des calendriers / événements : endpoints HTTP (ex. `/api/v1/calendar/calendars`, `/api/v1/calendar/events`) + outils MCP (`proton_list_calendars`, `proton_list_events`)
- [ ] Décider du périmètre écriture (intégration `proton-cal` vs pod séparé) selon le besoin réel
- [ ] Si écriture retenue : upgrade Go 1.26 + `gopenpgp` v2.10, couvrir la régression mail par les tests existants
- [ ] Tests conformes aux règles du repo (min. 2 tests par fonction : happy path + edge case)
- [ ] Déploiement GitOps : bump des tags image dans `proton-reader/helm/proton-reader/values.yaml`

## Notes

- Session Proton du pod perdue au restart (voir #177) → le re-login + 2FA sera nécessaire pour les tests.
- Issue liée au travail déjà préparé sur la branche `feat/proton-calendar`.
