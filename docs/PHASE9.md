# Checklist — Phase 9 : commercialisation

## Étape 1 — Offres et source unique `[x]`

- [x] `packages/shared/plans.json` : FREE 50 analyses/jour et 1 clé, PRO 2 000/jour et 5 clés, BUSINESS 20 000/jour et 20 clés
- [x] Types TS alignés dans `packages/shared/src/index.ts`
- [x] API Python lisant le même fichier (`services/api/app/core/plans.py`)
- [x] Aucun tarif inventé : PRO et BUSINESS affichés « Sur devis »
- [x] `paymentActive = false` dans le catalogue et dans l'abonnement

## Étape 2 — Quotas et clés API réels `[x]`

- [x] Table `api_keys` + colonne `users.plan` (migration `0002_billing_api_keys`)
- [x] Clé affichée une seule fois, stockée uniquement en HMAC-SHA256 sensible à la casse
- [x] En-tête `X-API-Key` accepté sur `/analyze/url` et `/analyze/message`
- [x] Quota journalier par clé, remis à minuit UTC, erreur `quota_exceeded` (429)
- [x] Révocation immédiate, limite du nombre de clés selon l'offre
- [x] Aucun paiement, facturation ou abonnement actif

## Étape 3 — Interface et documentation publique `[x]`

- [x] `/offres` : trois offres lues depuis la source partagée
- [x] `/cles-api` : création, liste et révocation réelles
- [x] `/documentation` : endpoints, base URL, exemple `curl`, format d'erreur et limites
- [x] Liens dans l'en-tête, le pied de page et le profil
- [x] Clés fictives uniquement dans les exemples

## Vérification `[x]`

- [x] `npm run api:test` → **51 passed**
- [x] `npm run api:migrate` → migration 0002 appliquée à la base locale
- [x] `npm run typecheck` → web + mobile + shared OK
- [x] `npm run web:build` → 21 routes générées (dont `/offres`, `/cles-api`, `/documentation`)
- [x] Commit

> Aucun prix PRO/BUSINESS n'est annoncé sans accord explicite. Aucun encaissement n'est possible dans cette version.
