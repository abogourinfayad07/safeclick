# Checklist — Phase 5 : interface web

## Étape 1 — Contrats et client API `[x]`

- [x] `apps/web/lib/api.ts` : client typé basé sur `fetch`, erreurs uniformes (`ApiClientError`)
- [x] URL lue depuis `NEXT_PUBLIC_API_URL` (aucun secret dans le code)
- [x] `apps/web/lib/auth.ts` : jeton conservé côté navigateur, effaçable
- [x] Types alignés sur `packages/shared` (`AnalysisResult`, `API_PREFIX`, limites)

## Étape 2 — Pages connectées `[x]`

- [x] `/analyse` : URL et message, résultat réel, indicateurs, recommandations, limites
- [x] `/signalement` : contact haché côté API, accusation désactivée, doublon géré
- [x] `/connexion`, `/inscription`, `/verification` : flux réel Argon2id + JWT
- [x] `/dashboard`, `/historique`, `/profil` : données réelles de l'API
- [x] `/admin` : modération réelle (confirmer/écarter) réservée aux administrateurs

## Étape 3 — Information et i18n `[x]`

- [x] 17 routes Next.js au total, dont les pages `/a-propos`, `/confidentialite`,
      `/mentions-legales`, `/aide`, `/securite`, `/contact`
- [x] `apps/web/lib/i18n.tsx` : dictionnaire FR complet, dictionnaire EN complet,
      provider React et clés typées
- [x] Graphiques de répartition simples construits à partir des comptages réels de la base
      (`apps/web/components/dashboard/stats-bars.tsx`)
- [x] Aucune métrique de précision inventée, aucune accusation automatique

## Vérification `[x]`

- [x] Endpoints ajoutés : `GET /api/v1/analyses`, `GET /api/v1/admin/reports`,
      `POST /api/v1/admin/reports/{id}/review`, `GET /api/v1/admin/stats`
- [x] `npm run api:test` → **36 passed**
- [x] `npm run typecheck` → web + mobile + shared OK
- [x] `npm run web:build` → 18 pages générées, build production OK
- [x] Commit

> Le jeton d'accès est conservé dans `localStorage` : c'est une limite connue et documentée.
> Le passage à un cookie HttpOnly sera traité dans la phase 8 (sécurité).
