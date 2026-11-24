# Checklist — Phase 4 : authentification

## Étape 1 — Sécurité `[x]`

- [x] `app/core/security.py` : Argon2id (hash + vérification) et JWT HS256
- [x] Jeton d'accès court (30 min par défaut) avec `sub`, `ver`, `purpose`, `jti`
- [x] Jeton de vérification 24 h, finalité distincte (`verify`)
- [x] Hachage factice utilisé quand le compte n'existe pas (atténuation du timing)

## Étape 2 — Routes `[x]`

- [x] `POST /api/v1/auth/register` (mot de passe >= 12, lettre + chiffre)
- [x] `POST /api/v1/auth/verify` (mode `console` : token dans les logs serveur uniquement)
- [x] `POST /api/v1/auth/login` (connexion refusée tant que l'e-mail n'est pas vérifié)
- [x] `GET /api/v1/user/profile`, `DELETE /api/v1/user/profile`
- [x] Analyses associées au compte quand un jeton valide est fourni

## Vérification `[x]`

- [x] `npm run api:test` → **31 passed**, sans avertissement
- [x] Clé de test factice > 32 octets (aucun avertissement PyJWT)
- [x] Aucun secret réel dans le code
- [x] Commit

> L'envoi d'e-mail réel n'est pas configuré : en développement, `EMAIL_BACKEND=console` écrit le lien dans les logs serveur. Aucun service payant n'est utilisé.
