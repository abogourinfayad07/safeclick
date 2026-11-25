# Checklist — Phase 10 : déploiement

La procédure complète est dans [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Étape 1 — Intégration continue `[x]`

- [x] Workflow `.github/workflows/ci.yml` sur `push` et `pull_request` vers `main` — runs #1 à #5 verts
- [x] Un seul job de vérifications reproductibles : tests API, typecheck, build web, audit npm, Expo Doctor, export Android
- [x] Job séparé de validation Docker : `docker compose config` puis build des deux images
- [x] Permissions GitHub limitées à `contents: read`
- [x] Aucun secret stocké dans le workflow ; `SECRET_KEY` factice uniquement pour la validation du compose

## Étape 2 — Conteneurs `[x]`

- [x] `services/api/Dockerfile` : Python 3.15 slim, utilisateur non root, healthcheck
- [x] `apps/web/Dockerfile` : build Next standalone, étape d'exécution sans dépendances de développement
- [x] `docker-compose.yml` : PostgreSQL, API, web, Redis optionnel (`profiles: ["cache"]`)
- [x] Volume PostgreSQL nommé, démarrage de l'API après le healthcheck de la base
- [x] Migrations Alembic exécutées au démarrage de l'API
- [x] `.dockerignore` exclut `.env`, bases locales, caches et artefacts natives
- [x] Validation du compose et build des deux images réussis dans le job CI `Validation Docker`

## Étape 3 — Pré-vérification `[x]`

- [x] `scripts/preflight.py` : mode `local` et mode `deploy`
- [x] Détection des motifs de secrets dans les fichiers suivis
- [x] Refus de `.env` suivi par Git
- [x] Contrôle des variables de production : HTTPS, PostgreSQL, SECRET_KEY, e-mail, limitation d'abus
- [x] Script npm `deploy:preflight`

## Étape 4 — Préparation opérationnelle `[x]`

- [x] Documentation des variables et des commandes PowerShell
- [x] Documentation des étapes encore manuelles et des procédures de rollback
- [x] Base Neon préparée : URL normalisée, TLS forcé, `db:check` et migration manuelle via GitHub
- [x] Blueprint Render préparé puis déployé manuellement : API + web en plan gratuit, `DATABASE_URL` secret, HTTPS fourni
- [x] Aucun compte, domaine, certificat, abonnement ou publication Android créé automatiquement par l'assistant

## Étape 5 — Déploiement réel `[~]`

- [x] Secrets GitHub `DATABASE_URL` ajoutés et migration Neon exécutée (run `45569575125`)
- [x] Services Render créés : API `safeclick` et web `safeclick-web`, plan gratuit, région Oregon
- [x] `/health`, `/api/v1/info`, `/api/v1/billing/plans`, site web et `/offres` vérifiés
- [x] CORS et en-têtes de sécurité vérifiés (`docs/RENDER.md`)
- [ ] Domaine personnalisé — non requis, aucun achat
- [ ] Surveillance externe et alertes
- [ ] Sauvegardes Neon vérifiées ou automatisées
- [ ] Signature et publication de l'APK/AAB Android

## Vérification locale `[x]`

- [x] `npm run api:test` → 59 tests, dont le test du blueprint Render
- [x] `npm run typecheck` → web + mobile + shared OK
- [x] `npm run web:build` → build standalone généré
- [x] `npm run mobile:doctor` → 20/20
- [x] `npm run mobile:export` → bundle Android généré
- [x] `python scripts/preflight.py --mode local` → OK
- [x] `npm audit --audit-level=moderate` → 0 vulnérabilité
- [x] CI GitHub run #1 → **success** : `Tests, typecheck, build et audit` et `Validation Docker` verts

> Docker est absent de la machine locale, mais le job CI `Validation Docker` a validé le compose et construit les deux images avec succès. Le déploiement réel a ensuite été effectué manuellement sur Render par le propriétaire, sans abonnement payant ni domaine personnalisé.
