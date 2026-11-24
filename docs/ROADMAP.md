# Feuille de route SAFECLICK

Légende : `[x]` vérifié, `[~]` en cours, `[ ]` à faire.

## Phase 1 — Initialisation `[~]`

- [x] Analyse du cahier des charges et identification des risques
- [x] Vérification réelle de l'environnement Windows
- [x] Définition de l'architecture et des versions compatibles
- [x] Création du monorepo et des fichiers racine
- [x] Configuration Git (branche `main`, identité, commit initial)
- [x] Documentation initiale
- [x] Initialisation `apps/web` (Next.js 16 + TypeScript + Tailwind 4 + composants UI de base)
- [x] Initialisation `apps/mobile` (Expo 58 + React Native 0.88)
- [ ] Initialisation `services/api` (FastAPI + SQLAlchemy + requirements + tests smoke)
- [ ] Vérification : `npm run typecheck`, `npm run api:test`, commit

## Phase 2 — Backend `[ ]`

Modèles, migrations Alembic, validation Pydantic, gestion d'erreurs, endpoints `/health`, `/api/v1/...`, tests.

## Phase 3 — Moteur d'analyse `[ ]`

Analyse URL passive, heuristiques homoglyphes/sous-domaines/raccourcisseurs, analyse de messages, classification à 3 niveaux, explications et limites.

## Phase 4 — Authentification `[ ]`

Inscription, connexion, vérification e-mail (mode `console` en dev), réinitialisation, profil, sessions, historique, suppression de compte, confidentialité.

## Phase 5 — Interface web `[ ]`

15 pages, tableau de bord, graphiques, espace admin, i18n FR prêt pour l'anglais.

## Phase 6 — Application Android `[ ]`

Navigation Expo, auth, analyse, historique, notifications, profil, paramètres, connexion à la même API.

## Phase 7 — Intelligence artificielle `[ ]`

Jeu de données étiqueté et vérifié, entraînement scikit-learn, évaluation mesurée, réduction des faux positifs/négatifs. Aucune performance annoncée sans mesure.

## Phase 8 — Sécurité `[ ]`

Audit des entrées, SSRF, abus API, permissions, journalisation sécurisée, sauvegardes, tests.

## Phase 9 — Commercialisation `[ ]`

Offres FREE / PRO / BUSINESS, quotas, clés API, documentation publique, préparation paiements (sans engagement financier).

## Phase 10 — Déploiement `[ ]`

Hébergement, domaine, HTTPS, CI/CD, monitoring, sauvegardes, publication Android.

---

## Règles de progression

1. Une étape = des fichiers créés + une commande de vérification + un commit.
2. Aucune fonctionnalité n'est déclarée terminée sans exécution de la commande correspondante.
3. Aucune dépense ni abonnement sans accord explicite.
