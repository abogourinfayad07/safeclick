# SAFECLICK

> Protéger les internautes contre les arnaques numériques, le phishing et les liens malveillants — avec des explications compréhensibles par tous.

**Statut : PHASE 1 — initialisation du monorepo (en cours).**  
Ce dépôt contient aujourd'hui le squelette et la documentation. Les applications ne sont pas encore fonctionnelles : elles seront ajoutées étape par étape, avec des commandes de vérification à chaque fois.

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

# 2. Dépendances JavaScript (une fois les apps créées)
npm install

# 3. Environnement Python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r services\api\requirements.txt

# 4. Lancements (dans des terminaux séparés)
npm run web:dev
npm run api:dev
```

> Les fichiers `services\api\requirements.txt`, `apps\web` et `apps\mobile` sont créés aux étapes suivantes de la phase 1. Aucune commande n'est présentée comme déjà réussie tant qu'elle n'a pas été exécutée.

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
- [Checklist phase 1](docs/PHASE1.md)
