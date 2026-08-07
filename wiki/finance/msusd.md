# msUSD — suivi stratégie

Page vivante du suivi msUSD de Chris (LP Aerodrome + lending AAVE, rewards en AERO).

## Contexte

- **msUSD** = stablecoin synthétique Metronome (dérivé d'ETH, comme msETH), principalement sur Aerodrome (Base)
- Chris fournit des positions (pools Aerodrome + lending AAVE) → rewards **AERO**
- **Crash juillet 2026** → depeg → stratégie de récupération (encaisser les fees, surveiller le plancher)

## Timeline du crash

| Date | Événement |
|---|---|
| ≤ 23/07/2026 | Peg stable ~$0.99 (vérifié CoinGecko) |
| 24/07/2026 | Premier craquement (~0.98) |
| 31/07 → 01/08/2026 | Chute majeure : 0.81 → 0.74 → ~0.71 |
| 31/07/2026 18:00 | Baseline wallet figée (`~/.peg_pending_state.json`) — perte de référence **$28,726** |
| Début 08/2026 | Post-mortem officiel Metronome : underbacking ~6 367 msETH + 4.57M msUSD (latence oracle Chainlink sur le swap module) |

## État actuel (07/08/2026)

Source : `python3 ~/scripts/peg_pending.py` (rapport horaire, cron 56aac0da2733).

- **msUSD : $0.7039** (70.4 % du peg) · **msETH : $1,339** (70.5 % ETH) · ETH : $1,900 · AERO : $0.4302
- **TVL pools msUSD : $7.63M** (vs ~$34.7M le 20/07 → exode massif)
- **Wallet total : $79,537** (delta **-2,535 $** vs baseline)
- **Restant à compenser : $31,261** sur $28,726 → **-8.8 %** (la perte s'aggrave légèrement)
- Positions lending : WETH-msETH-V3 $23.7k · AAVE-EURC $20.2k · AAVE-USDC $18.1k · msUSD-USDC-V3 $17.6k
- Pending rewards : ~$192 (≈ 447 AERO)

## Stratégie (règles de Chris)

1. **Encaisser les fees tant que le depeg stagne (~0.70)**
2. **Sortir les pools msUSD-USDC si le plancher casse (< $0.70)** — zone de déclenchement du plan trésor
3. **Re-peg > $0.95** → attention aux positions serrées qui sortent de range (100 % USDC)
4. **Burn de supply** (>1 %) = le trésor rachète → le plan s'exécute, on reste
5. Le seul vrai retour des émissions AERO = **re-peg msUSD**

## Rewards & Predictive Allocation

- Le **vote gauge hebdomadaire a été remplacé** (annonce officielle 26/07/2026) par la **Predictive Allocation** : un modèle temps réel alloue les émissions selon la demande prédite de liquidité
- Conséquence : les pools msUSD sont délaissées tant que le depeg dure (demande prédite faible)
- Rythme observé : **~178 AERO/h** (pic 04/08) → **~32 AERO/h** (~$340/jour, APR ~155 % sur ~$80k) — chute libre stoppée mais -80 % sous le pic
- Upgrade officiel complet listé pour **septembre 2026** — rappel cron le 01/09 à 9h

## Outils de suivi

| Outil | Usage |
|---|---|
| `peg_pending.py` | Rapport complet horaire (prix, TVL, wallet vs baseline, positions, pending) |
| `msusd_strategy_watch.py` | Watchdog silencieux : plancher <0.70, nouveau low, burn, re-peg |
| `aero_alert.py` | Alerte prix AERO (seuil 0.35) |
| MCP `crypto-monitoring` | positions, rewards_pending, compute_apr (structuré) |
| CoinGecko / GeckoTerminal / DeFiLlama | Prix, TVL pools, historique APY par pool |

## Interprétation des signaux

| Signal | Lecture |
|---|---|
| msUSD < $0.70 | Plancher trésor cassé → sortir les pools msUSD-USDC |
| Nouveau plus bas >1.5 % | Depeg continue → réduire l'exposition |
| Supply en baisse >1 % | Burn = plan s'exécute → on reste |
| Retour > $0.95 | Re-peg → attention positions serrées (100 % USDC) |
| Pending = $0.00 | Souvent normal : reset au harvest — vérifier l'historique |
| Rythme AERO/h en baisse partout | Predictive Allocation (pas un vote) — structurel tant que le depeg dure |
| APR affiché (ex. 235 %) | Moyenne 7 j, pas le taux instantané |

## Pièges connus

- `history[].rewards` = **AERO, pas USD** (`rewards.value` = USD, `rewards.amount` = AERO)
- Pending rewards **reset au harvest** → un 0 n'est pas une baisse
- API positions 500/hang si Postgres down (CNPG bug #9301, PVC plein) → **ce n'est pas une perte de rewards**
- **Ne pas confondre** msUSD Metronome avec Main Street USD (même ticker, crashé ~$0.25 mi-2026, oracles Redstone) — filtrer les recherches par Metronome/Aerodrome
- Exode TVL massif pendant peg stable = signal leading (slipstream MSUSD-USDC : $25.3M le 20/07 → $2.6M le 31/07)

## Sources

- Rapport `peg_pending.py` — 07/08/2026 (cron horaire)
- Post-mortem officiel Metronome : [Post-Mortem: msETH/msUSD Underbacking](https://paragraph.com/@metronomedao/post-mortem-msethmsusd-underbacking) (début 08/2026)
- Timeline prix : CoinGecko (`metronome-synth-usd`) — vérifiée en session 08/2026
- Announce Predictive Allocation Aerodrome : 26/07/2026 (recherche web, sessions 08/2026)
- Skill `msusd-strategy-tracking` — procédure complète

## Liens

- → [Finance](index.md) · [Index](../index.md)
