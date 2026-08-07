# Prospection mairies — Gumpy

État du démarchage des communes pour proposer le photobooth Gumpy / PhotoCall.

## Le produit

- **Gumpy** : fabricant de photobooths basé en Rhône-Alpes (Chambéry / Lyon)
- **PhotoCall** : fond de scène personnalisé aux couleurs de la commune — les habitants repartent avec un souvenir photo à l'effigie du village
- Partage instantané par QR code (réseaux sociaux de l'événement)
- Installation < 30 min ; formules collectivités dès **500 € HT**

## Preuve sociale

Saint-Jean-de-Maurienne (73) : Père Noël, fête des aînés, fête du pain. → à citer dans chaque mail.

## Cible & données

| Secteur | Communes | Fichier |
|---------|----------|---------|
| Savoie + Haute-Savoie (> 2000 hab) | **145** | [`data/gumpy-prospection/contacts.json`](../../data/gumpy-prospection/contacts.json) |
| Secteur Belleville (71) | **161** | [`data/gumpy-prospection/belleville_contacts.json`](../../data/gumpy-prospection/belleville_contacts.json) |

Fichier de travail principal : [`mairies_73_74_prospection.xlsx`](../../data/gumpy-prospection/mairies_73_74_prospection.xlsx)
(contient la colonne « Événements connus » pour personnaliser chaque mail).

## Pipeline de prospection

1. **Scrapping** des annuaires de communes (départements 01, 38, 42, 69, 71, 73, 74) → `annuaire_dept_*.html`
2. **Enrichissement** contacts (email, tel, site) → `contacts.json` / `belleville_contacts.json`
3. **XLSX** de travail → `mairies_73_74_prospection.xlsx` (script `step3_xlsx.py`)
4. **Envoi mail** : [`mail_template_gumpy.md`](../../data/gumpy-prospection/mail_template_gumpy.md) — personnaliser le 1er paragraphe avec un événement réel de la commune, mentionner Saint-Jean-de-Maurienne
5. **Relance téléphonique J+7** : [`relance_telephonique.md`](../../data/gumpy-prospection/relance_telephonique.md) — script complet, gestion des objections, horaires (9h-12h / 14h-17h, éviter lundi matin + vendredi après-midi)

## Saisonnalité

- **Noël** → prospection sept–oct
- **Fêtes d'été** → prospection mars–avril
- **Fête des aînés** → sept–oct (événement souvent en novembre)

## Supports

- Logos : [`gumpy_logo.svg`](../../data/gumpy-prospection/gumpy_logo.svg), `.png`, zoom bois/alu
- Rollups alu & bois : scripts `compose_rollup.py` / `render_rollup.py`, aperçus PNG
- Email HTML : [`gumpy_email_template.html`](../../data/gumpy-prospection/gumpy_email_template.html)
- QR code : [`gumpy_qr.png`](../../data/gumpy-prospection/gumpy_qr.png)

## Sources

- Données brutes : `data/gumpy-prospection/` (scrap annuaires 08/2026, templates, contacts)
- Templates mail & relance : fichiers du même dossier

## Liens

- → [Gumpy](index.md) · [Index](../index.md)
