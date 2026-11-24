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

## Étape 3 — Frontend web `[x]`

- [x] `apps/web/package.json` (Next 16.4.6, React 19.3.1, Tailwind 4.3.5, TypeScript 5.9.3)
- [x] `next.config.ts`, `postcss.config.mjs`, `tsconfig.json`
- [x] `app/globals.css` (thème bleu nuit / bleu électrique)
- [x] `app/layout.tsx`, `app/page.tsx` (page d’accueil réelle, liens internes valides)
- [x] Composants `ui/button.tsx`, `analysis/risk-badge.tsx`, `layout/header.tsx`, `layout/footer.tsx`
- [x] `lib/utils.ts` (`cn`) et consommation de `@safeclick/shared`
- [x] `npm install` → 55 paquets, **0 vulnérabilité**
- [x] `npm run web:build` → compilation OK, 3 pages statiques générées
- [x] `npm run typecheck` → web + shared OK
- [ ] shadcn/ui CLI (composants additionnels) — à faire quand les pages dashboard/analyse seront créées

> Next.js a automatiquement ajusté `jsx: react-jsx` et ajouté `.next/dev/types/**/*.ts` au `tsconfig.json` : changement attendu et conservé.

## Étape 4 — Application mobile `[~]`

- [x] `apps/mobile/package.json` minimal (nécessaire aux npm workspaces)
- [ ] `app.json`, `tsconfig.json`, `App.tsx`, écran d’accueil, `npx expo-doctor`

## Étape 5 — Backend `[ ]`

À faire : `services/api/requirements.txt`, `pyproject.toml`, `app/main.py`, `app/core/config.py`, `app/api/routes/health.py`, `tests/test_health.py`, venv + pytest.

## Étape 6 — Vérification finale `[ ]`

- [ ] `npm run typecheck`
- [ ] `npm run api:test`
- [ ] `git status --short` propre après commit
