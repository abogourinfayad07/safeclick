# Checklist — Phase 2 : backend structuré

## Étape 1 — Versionnage et erreurs uniformes `[x]`

- [x] `app/core/version.py`, `app/core/limits.py` (2048 / 4000, alignés sur `packages/shared`)
- [x] `app/schemas/common.py` (contrats d'erreur et d'information API)
- [x] `app/api/errors.py` (gestionnaires FastAPI, aucun détail technique divulgué)
- [x] `GET /api/v1/health` en plus de `/health` (operation IDs distincts)
- [x] `GET /api/v1/info` (limites réelles, langues, types d'analyse, limite explicite)
- [x] Tests : santé versionnée, contrat info, erreur 404 uniforme, OpenAPI
- [x] `npm run api:test` → **7 passed**, sans avertissement

## Étape 2 — Modèles et migrations `[ ]`

- [ ] Modèles SQLAlchemy : `users`, `analyses`, `reports`
- [ ] Énums partagées côté Python alignées sur `packages/shared`
- [ ] Alembic : `alembic.ini`, `env.py`, `script.py.mako`, migration `0001`
- [ ] Script npm `api:migrate`
- [ ] Test : migration appliquée sur une base SQLite temporaire
- [ ] Test : contraintes et valeurs par défaut des modèles

## Étape 3 — Signalements et validation stricte `[ ]`

- [ ] `POST /api/v1/reports` : Pydantic strict, `extra="forbid"`
- [ ] Hachage HMAC du contact, jamais de contact en clair en base
- [ ] Statut initial `unverified`, réponse sans accusation
- [ ] Tests : 201, doublon, 422 uniforme, absence du contact brut
- [ ] Vérification finale phase 2 + commit

> Aucune analyse d'URL ou de message n'est exposée ici : le moteur arrive en phase 3.
