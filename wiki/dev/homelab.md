# Homelab — inventaire & architecture

Inventaire du cluster RKE2 de Chris, issu des repos de config (sources réelles, pas de mémoire).

## Architecture matérielle (192.168.1.0/24)

Source : repo `raspberry-cluster` (README, 08/2026).

```
VIP .200 (Keepalived VRRP)
├── HAProxy :6443/:9345 — HAOS Pi (.35, LB Master) + Pi 4 (.24, LB Backup)

Control plane RKE2 (etcd) :
├── master — Pi 5, .21
├── pi3    — Pi 4, .23
└── um870  — MiniPC, .27

Workers :
├── pi4     — Pi 4, .24 (worker + LB backup)
├── zima    — MiniPC, .26
├── ryzen   — Desktop, .28 (GPU AMD)
└── nvidia  — Jetson, .30 (GPU)

CNI : Cilium (kube-proxy désactivé)
```

- RKE2 avec etcd sur 3 control planes (quorum 2/3)
- Le dossier `scripts/k3s/` du repo = legacy (installation initiale), l'actuel est RKE2
- Stockage : **Longhorn** (+ local-path-provisioner + NFS pour les modèles)
- `hosts/cluster.txt` : les 7 nœuds (cluster@192.168.1.{21,23,24,26,27,28,30})

## GitOps — ArgoCD (repo `continuous-delivery`)

Apps racine (namespace `kube-infra`), toutes pointent vers `infrastructure-crds/` :

| App ArgoCD | Source path | Contenu |
|---|---|---|
| rke2-apps | `infrastructure-crds/rke2-apps` | applications métier |
| rke2-infra | `infrastructure-crds/rke2-infra` | infra : CNPG, Longhorn, VictoriaMetrics, Keycloak, Tailscale, ARC… |
| rke2-addons | `infrastructure-crds/rke2-addons` | add-ons |
| mlops-stack | `infrastructure-crds/rke2-mlops` | stack IA/ML (exclut toolhive, llama-embedder) |
| monitoring-crds | `infrastructure-crds/rke2-monitoring` | monitoring (récursif) |
| nvidia-infra | `infrastructure-crds/rke2-nvidia` | stack GPU NVIDIA (namespace nvidia-infra) |
| external-secrets | `infrastructure-crds/external-secrets` | secrets externes |
| rke2-infra (finalizers) | — | Longhorn + VictoriaMetrics ont des pre-delete hooks → ignoreDifferences sur les finalizers |

`deployed-charts/` : base-cluster, cnpg-operator, kyverno, oci-storage, portal-checker, tailscale, vector, victorialogs.
`charts/` : hermes, llama-cpp-multi, victoria-metrics-stack, guardrails, gha-runner-scale-set-controller, promptfoo, protonmail-bridge, …

## Applications métier (rke2-apps)

| App | Namespace | Source repo |
|---|---|---|
| proton-reader | invoices-automation | invoices-automation (helm/proton-reader) |
| invoices-automation | invoices-automation | invoices-automation |
| crypto-monitoring | crypto-monitoring | finance-monitoring (helm/crypto-monitoring) |
| dc-finance | dc-finance | dc-finance |
| solar-monitoring | solar-monitoring | solar-monitoring |
| atuin | — | shell history sync |
| sonarqube | — | qualité code |
| unleash | — | feature flags |

## Infra (rke2-infra)

- **CNPG clusters** : code-search, dc-finance, finance-monitoring, genai-benchmark, odoo, solar, sonarqube, unleash (dans cnpg-system)
- **Longhorn** — stockage persistant · **local-path-provisioner** · **NFS** (nfs-arc-runner, nfs-model-server)
- **VictoriaMetrics** (métriques) · **Keycloak** (SSO) · **Tailscale** (tailscale-expose + monitoring) · **ARC** (GitHub Actions runners, arc-runner-sets + nfs)
- **argocd-image-updater** / headroom-imageupdater — auto-update images
- Cronjobs de ménage : cleanup-failed-backups, cleanup-old-volumesnapshots
- Sysctls : inotify (daemonset), kernel-module-blacklist

## Stack MLOps (rke2-mlops)

- **hermes** (namespace hermes — l'assistant, chart `charts/hermes` de continuous-delivery)
- **ai-gateway** / headroom — gateway LLM · **code-search** · **qdrant** (vecteurs) · **llama-embedder**
- **whisper-stream** / whisper-ptt-ui / **speaches** (STT) · **k8s-pypiserver** (pypi interne)
- **amd-device-plugin** + amd-smi-exporter (GPU AMD du nœud ryzen)
- **cloudflare-tunnel**

## GPU NVIDIA (rke2-nvidia, namespace nvidia-infra)

- **nvidia-gpu-operator** (node nvidia .30, Jetson)
- **llama-cpp** / **llama-cpp-manager** (imageupdater) / llama-cpp-diffusion · **genai-benchmark-tool**
- nfs-model-server · nvidia-power-limit-daemonset · nvidia-cm-dcgmexport
- Note : ResourceClaimTemplate → ignoreDifferences (drift connu), node taint `add-node-nvidia-taint.sh`

## Monitoring (rke2-monitoring)

- **VictoriaLogs** + **vector** (logs) · **victorialogs-mcp** (MCP pour Hermes)
- **Jaeger** (traces) · **opentelemetry-collector** · **node-problem-detector** (+ scrape)
- Dashboards, podscrapes (etcd, rke2-control-plane, whisper, tailscale, sgrep), netconsole-receiver
- Alertes CNPG backups

## Secrets (external-secrets)

- github-token, huggingface-token, tailscale, keycloak-clients, forgejo (+db), sonarqube (+OIDC), claude-api-key, dashboard-auth, grafana-oauth, langfuse-salt, cnpg-*

## Repos associés (code source)

`continuous-delivery` (GitOps) · `raspberry-cluster` (infra/hardware) · `proton-service` (succ. proton-reader) · `invoices-automation` · `finance-monitoring` (crypto-monitoring) · `solar-monitoring` · `dc-finance` · `stock-analysis` (stock-analyzer) · `garden-keeper` · `ev-charge-tracker` · `ha-config` (Home Assistant) · `genai-benchmark-tool` · `code-search` · `llm-router` / `ai-gateway` / `mcp-collection`

## Incidents & pièges connus

- **CNPG 1.27 bug #9301** : PVC Postgres plein → l'opérateur refuse d'agrandir (deadlock). Fix : patch manuel du PVC (`spec.resources.requests.storage`) après avoir mis le manifest Git à jour — le FS se resize seul, l'opérateur reprend la main.
- **Pas de kubectl dans le pod Hermes** : accès API K8s via le token service account (`/var/run/secrets/kubernetes.io/serviceaccount/token`) pour diagnostiquer.
- **MCP config** (config.yaml, .env) = GitOps aussi : PR sur continuous-delivery → ArgoCD.

## Sources

- Repo `raspberry-cluster` — README + hosts (branche main, consulté 07/08/2026)
- Repo `continuous-delivery` — cluster-*.yaml + infrastructure-crds/* + charts + deployed-charts (07/08/2026)
- Expérience sessions Hermes (incidents CNPG, config MCP)

## Liens

- → [Dev](index.md) · [Index](../index.md)
