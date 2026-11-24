# Checklist — Phase 8 : sécurité

La revue détaillée est dans [`docs/SECURITE.md`](docs/SECURITE.md).

## Étape 1 — API `[x]`

- [x] En-têtes de sécurité + HSTS hors développement
- [x] CORS restreint (origine, méthodes et en-têtes)
- [x] Limitation d'abus configurable, groups `/auth`, `/analyze`, `/reports`, `/admin`
- [x] Journalisation sans corps, jeton, en-tête ni chaîne de requête
- [x] Jeton de vérification jamais journalisé en test/production
- [x] Aucun fetch serveur d'URL utilisateur (SSRF éliminé par conception)

## Étape 2 — Web et mobile `[x]`

- [x] CSP et en-têtes vérifiés sur un serveur `next start` réel
- [x] `connect-src` construit depuis `NEXT_PUBLIC_API_URL`
- [x] Jeton mobile dans `expo-secure-store`
- [x] Revue du `localStorage` web documentée comme limite non résolue

## Étape 3 — Sauvegarde `[x]`

- [x] `npm run db:backup` : copie SQLite réelle
- [x] Refus explicite de PostgreSQL (aucune sauvegarde simulée)

## Vérification `[x]`

- [x] `npm run api:test` → **46 passed**
- [x] `npm run typecheck` → OK
- [x] `npm run web:build` → OK
- [x] `npm run db:backup` → fichier créé
- [x] `GET /` sur `next start -p 3010` → en-têtes présents
- [x] Commit
