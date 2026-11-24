# Checklist — Phase 2 : backend structuré

## Étape 1 — Versionnage et erreurs uniformes `[x]`

- [x] `app/core/version.py`, `app/core/limits.py` (2048 / 4000, alignés sur `packages/shared`)
- [x] `app/schemas/common.py` (contrats d'erreur et d'information API)
- [x] `app/api/errors.py` (gestionnaires FastAPI, aucun détail technique divulgué)
- [x] `GET /api/v1/health` en plus de `/health` (operation IDs distincts)
- [x] `GET /api/v1/info` (limites réelles, langues, types d'analyse, limite explicite)
- [x] Tests : santé versionnée, contrat info, erreur 404 uniforme, OpenAPI
- [x] `npm run api:test` → **7 passed**, sans avertissement

## Étape 2 — Modèles et migrations `[x]`

- [x] Modèles SQLAlchemy : `users`, `analyses`, `reports`
- [x] Énums Python alignées sur les chaînes de `packages/shared` (`low/medium/high`, `url/message`)
- [x] `app/core/hashing.py` : HMAC-SHA256 du contact, jamais de valeur brute
- [x] `app/db/session.py` : `StaticPool` pour SQLite en mémoire (tests HTTP cohérents)
- [x] Alembic : `alembic.ini`, `env.py`, `script.py.mako`, migration `0001_initial_schema`
- [x] Script npm `api:migrate` vérifié depuis la racine sur une base temporaire
- [x] Test : migration appliquée sur SQLite + index unique vérifié
- [x] Tests : valeurs par défaut, unicité e-mail, contrainte de score, énums
- [x] `npm run api:test` → **14 passed**

## Étape 3 — Signalements et validation stricte `[x]`

- [x] `POST /api/v1/reports` : Pydantic strict, `extra="forbid"`, champs `field` explicites
- [x] Hachage HMAC du contact, jamais de contact en clair en base
- [x] Statut initial `unverified`, réponse sans accusation, doublon réutilisé
- [x] Tests : 201, doublon, contact invalide, champ interdit, accusation non reconnue
- [x] `npm run api:test` → **19 passed**

## Vérification finale `[x]`

- [x] `npm run typecheck` → web + mobile + shared OK
- [x] `npm run web:build` → build production OK
- [x] `npm run doctor -w @safeclick/mobile` → 20/20
- [x] `npm audit --audit-level=moderate` → 0 vulnérabilité
- [x] Smoke HTTP réel : migration + uvicorn sur `127.0.0.1:8012` → signalement `unverified`
- [x] `git status` propre après commit

**Phase 2 terminée.** Prochaine étape : phase 3 (moteur de détection, règles et scoring).

> Aucune analyse d'URL ou de message n'est exposée ici : le moteur arrive en phase 3.
