# Checklist — Phase 6 : application Android

## Étape 1 — Client et stockage `[x]`

- [x] `apps/mobile/lib/api.ts` : même API que le web, erreurs uniformes, `EXPO_PUBLIC_API_URL`
- [x] `apps/mobile/lib/token.ts` : jeton dans `expo-secure-store` (coffre sécurisé), pas de texte clair
- [x] Ajout de `expo-secure-store` via `npx expo install` (version compatible SDK 58)
- [x] Config plugin ajouté dans `apps/mobile/app.json`

## Étape 2 — Écrans connectés `[x]`

- [x] `/analyze` : appel réel à `/analyze/url` ou `/analyze/message`, résultat et limites affichés
- [x] `/login`, `/register`, `/verify` : flux réel Argon2id + JWT + vérification console
- [x] `/report` : signalement réel, HMAC côté API, accusation désactivée
- [x] `/history`, `/profile`, `/settings` : données réelles, déconnexion, suppression de compte

## Vérification `[x]`

- [x] `npm run typecheck` → web + mobile + shared OK
- [x] `npm run doctor -w @safeclick/mobile` → 20/20
- [x] `npx expo export --platform android --clear` → bundle Android généré
- [x] `npm audit --audit-level=moderate` → 0 vulnérabilité
- [x] Commit

> Vérification réelle sur téléphone toujours en attente : elle nécessite l'appareil de l'utilisateur.
> Aucun émulateur Android n'est installé sur la machine.

### Problème réel rencontré

Le premier `expo export` a échoué juste après `npx expo install` : Metro ne résolvait pas
`@expo/metro-runtime/build/index.js` alors que le fichier existait. Le cache Metro vide
(`--clear`) a résolu le problème. Ce n'était pas une erreur de code applicatif.
