# Checklist — Phase 1 : initialisation

## Étape 1 — Environnement `[x]`

- [x] OS, Node, npm, Python, Git, espace disque vérifiés
- [x] Versions npm et PyPI vérifiées
- [x] Contraintes documentées (`docs/ENVIRONNEMENT.md`)

## Étape 2 — Socle du monorepo `[x]`

- [x] `package.json` (workspaces npm, engines, scripts)
- [x] `.gitignore`
- [x] `.env.example`
- [x] `.editorconfig`
- [x] `docker-compose.yml` (non exécuté : Docker absent)
- [x] `packages/shared` (types communs)
- [x] `README.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md`
- [x] Git initialisé sur `main` + commit initial

## Étape 3 — Frontend web `[ ]`

À faire : `apps/web/package.json`, `tsconfig.json`, `next.config.ts`, configuration Tailwind 4, `app/layout.tsx`, `app/page.tsx`, composants de base, `npm install -w @safeclick/web`, `npm run web:build`.

## Étape 4 — Application mobile `[ ]`

À faire : `apps/mobile/package.json`, `app.json`, `tsconfig.json`, `App.tsx`, écran d'accueil, `npx expo-doctor`.

## Étape 5 — Backend `[ ]`

À faire : `services/api/requirements.txt`, `pyproject.toml`, `app/main.py`, `app/core/config.py`, `app/api/routes/health.py`, `tests/test_health.py`, venv + pytest.

## Étape 6 — Vérification finale `[ ]`

- [ ] `npm run typecheck`
- [ ] `npm run api:test`
- [ ] `git status --short` propre après commit
