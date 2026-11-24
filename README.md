# SAFECLICK

> Protéger les internautes contre les arnaques numériques, le phishing et les liens malveillants — avec des explications compréhensibles par tous.

**Statut : PHASES 1 à 8 terminées et vérifiées. PHASE 9 — commercialisation à venir.**  
Le site web et l'application Expo utilisent la même API. Le moteur reste passif : aucun lien n'est visité par le serveur. Le moteur de règles explicites reste la base ; un modèle local Naive Bayes ajoute un signal faible et explicable, avec des métriques mesurées sur un jeu synthétique uniquement ([détails](docs/PHASE7.md)). La revue de sécurité est décrite dans [`docs/SECURITE.md`](docs/SECURITE.md), limites comprises.

---

## Mission

SAFECLICK détecte et explique les menaces numériques :

- analyse d'URL (structure, domaine, homoglyphes, raccourcisseurs, sous-domaines) ;
- analyse de SMS / messages WhatsApp (urgence, demande d'argent, codes, usurpation) ;
- signalement de contacts suspects avec modération et **aucune accusation automatique** ;
- classification **vert / orange / rouge** avec score indicatif, raisons, recommandations et limites.

Un risque faible **n'est jamais une garantie de sécurité**.

---

## Environnement vérifié

| Outil | Version | État |
|---|---|---|
| Windows | 11 Pro, build 26300 | ✅ |
| Node.js | v26.13.1 | ✅ compatible Expo 58 / Next 16 |
| npm | 11.20.0 | ✅ workspaces natifs |
| Python | 3.15.2 | ✅ wheels vérifiés (numpy, scipy, pydantic-core) |
| Git | 2.56.0.windows.4 | ✅ identité configurée |
| Docker | absent | ⚠️ PostgreSQL local remplacé par SQLite en dev |
| pnpm / yarn | absents | ✅ non nécessaires |
| VS Code | non détecté dans le PATH | ⚠️ à vérifier côté utilisateur |

Détails : [`docs/ENVIRONNEMENT.md`](docs/ENVIRONNEMENT.md).

---

## Démarrage rapide (PowerShell)

```powershell
cd "C:\Users\HP\OneDrive\Documents\Projet par défaut"

# 1. Configuration locale
Copy-Item .env.example .env

# 2. Dépendances JavaScript
npm install

# 3. Environnement Python (les scripts npm utilisent directement ce venv)
python -m venv .venv
.\.venv\Scripts\python -m pip install -r services\api\requirements-dev.txt

# 4. Migration de la base (une fois avant le premier lancement API)
npm run api:migrate

# 5. Lancements (dans des terminaux séparés)
npm run web:dev
npm run api:dev

# Tests API, réentraînement et sauvegarde locale
npm run api:test
npm run ml:train
npm run db:backup
```

> Les commandes ci-dessus ont été exécutées sur l'environnement Windows décrit plus haut. `npm run api:test` utilise directement le venv `.venv`, sans activation manuelle.

---

## Structure cible

```text
SAFECLICK/
├── apps/
│   ├── web/          # Next.js 16 + TypeScript + Tailwind 4 + shadcn/ui
│   └── mobile/       # Expo 58 + React Native 0.88 + TypeScript
├── services/
│   └── api/
│       ├── app/{api,core,models,schemas,services,detectors,workers}/
│       └── tests/
├── packages/shared/  # types et contrats communs
├── infrastructure/   # Docker, déploiement
├── docs/             # architecture, décisions, roadmap
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## Principes de sécurité (non négociables)

- Aucun secret dans le code ; uniquement des variables d'environnement.
- Aucune URL utilisateur ouverte directement depuis le serveur sans protections SSRF.
- Validation stricte des entrées, mots de passe hachés (Argon2), permissions vérifiées côté serveur.
- Aucune exécution de contenu utilisateur.
- Aucune statistique de précision inventée, aucune promesse de protection absolue.
- Signalements non vérifiés distincts des informations confirmées.

---

## Documentation

- [Architecture définitive](docs/ARCHITECTURE.md)
- [Décisions techniques (ADR)](docs/DECISIONS.md)
- [Feuille de route](docs/ROADMAP.md)
- [Environnement vérifié](docs/ENVIRONNEMENT.md)
- [Sécurité et limites connues](docs/SECURITE.md)
- [Checklist phase 1](docs/PHASE1.md)
