# Feuille de route SAFECLICK

Légende : `[x]` vérifié, `[~]` en cours, `[ ]` à faire.

## Phase 1 — Initialisation `[x]`

- [x] Analyse du cahier des charges et identification des risques
- [x] Vérification réelle de l'environnement Windows
- [x] Définition de l'architecture et des versions compatibles
- [x] Création du monorepo et des fichiers racine
- [x] Configuration Git (branche `main`, identité, commit initial)
- [x] Documentation initiale
- [x] Initialisation `apps/web` (Next.js 16 + TypeScript + Tailwind 4 + composants UI de base)
- [x] Initialisation `apps/mobile` (Expo 58 + React Native 0.88)
- [x] Initialisation `services/api` (FastAPI + SQLAlchemy + requirements + tests smoke)
- [x] Vérification : `npm run typecheck`, `npm run web:build`, `npm run api:test`, `expo-doctor`, `npm audit`, commit

## Phase 2 — Backend `[x]`

Modèles, migrations Alembic, validation Pydantic, gestion d'erreurs, endpoints `/api/v1/...`, tests.  
Checklist détaillée : [`docs/PHASE2.md`](docs/PHASE2.md).

## Phase 3 — Moteur d'analyse `[x]`

Checklist détaillée : [`docs/PHASE3.md`](docs/PHASE3.md).

Analyse URL passive, heuristiques homoglyphes/sous-domaines/raccourcisseurs, analyse de messages, classification à 3 niveaux, explications et limites.

## Phase 4 — Authentification `[x]`

Checklist détaillée : [`docs/PHASE4.md`](docs/PHASE4.md).

Inscription, connexion, vérification e-mail (mode `console` en dev), réinitialisation, profil, sessions, historique, suppression de compte, confidentialité.

## Phase 5 — Interface web `[x]`

Checklist détaillée : [`docs/PHASE5.md`](docs/PHASE5.md).

17 routes Next.js, tableau de bord, graphiques de répartition réels, espace admin de modération, i18n FR avec dictionnaire anglais complet.

## Phase 6 — Application Android `[x]`

Checklist détaillée : [`docs/PHASE6.md`](docs/PHASE6.md).

Navigation Expo, auth, analyse, signalement, historique, profil, paramètres, connexion à la même API, jeton dans le coffre sécurisé.

## Phase 7 — Intelligence artificielle `[x]`

Checklist détaillée : [`docs/PHASE7.md`](docs/PHASE7.md).

Jeu synthétique étiqueté (60 messages), Naive Bayes local en Python pur, évaluation mesurée sur 12 exemples de test, signal statistique faible et explicable intégré au moteur de règles. Aucune performance annoncée sans mesure.

## Phase 8 — Sécurité `[x]`

Checklists détaillées : [`docs/PHASE8.md`](docs/PHASE8.md) et [`docs/SECURITE.md`](docs/SECURITE.md).

En-têtes, CORS, limitation d'abus, journalisation sans secret, revue du stockage du jeton web, sauvegarde SQLite réelle. Limites connues documentées, jamais présentées comme terminées.

## Phase 9 — Commercialisation `[x]`

Checklist détaillée : [`docs/PHASE9.md`](docs/PHASE9.md).

Offres FREE / PRO / BUSINESS depuis une source partagée, quotas journaliers réels, clés API hachées et révocables, documentation publique. Aucun tarif inventé ni paiement actif.

## Phase 10 — Déploiement `[~]`

Checklist détaillée : [`docs/PHASE10.md`](docs/PHASE10.md) et [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

CI, Docker Compose, pré-vérification et documentation prêts. Hébergement, domaine, HTTPS, monitoring et publication Android restent des actions manuelles : aucun déploiement ni abonnement effectué.

---

## Règles de progression

1. Une étape = des fichiers créés + une commande de vérification + un commit.
2. Aucune fonctionnalité n'est déclarée terminée sans exécution de la commande correspondante.
3. Aucune dépense ni abonnement sans accord explicite.
