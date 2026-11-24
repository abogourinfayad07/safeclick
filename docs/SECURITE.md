# Revue de sécurité — Phase 8

## Périmètre vérifié

- API FastAPI : `services/api/app/main.py`, `services/api/app/core/middleware.py`
- Web Next.js : `apps/web/next.config.ts`, `apps/web/lib/auth.ts`
- Mobile Expo : `apps/mobile/lib/token.ts`
- Configuration : `.env.example`, `services/api/app/core/config.py`

## Mesures réellement implémentées

### API

- **En-têtes** : `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Permissions-Policy`, `Cache-Control: no-store` sur toutes les réponses. HSTS ajouté dès que `ENVIRONMENT` n'est pas `development`.
- **CORS** : origine unique (`SITE_URL`), méthodes limitées à `GET`, `POST`, `DELETE`, `OPTIONS`, en-têtes limités à `Authorization` et `Content-Type`.
- **Limitation d'abus** : fenêtre glissante d'une minute, par adresse client et par groupe (`/auth`, `/analyze`, `/reports`, `/admin`). Valeurs configurables via `RATE_LIMIT_ENABLED` et `RATE_LIMIT_PER_MINUTE`.
- **Journalisation sécurisée** : seuls la méthode, le chemin sans chaîne de requête, le statut et la durée sont journalisés. Aucun corps, en-tête `Authorization` ou jeton n'est écrit dans les logs.
- **Vérification en console** : le jeton de vérification n'est affiché qu'en développement. En test et en production, aucun jeton n'est journalisé.
- **Permissions** : les routes d'administration restent protégées par `get_current_admin` (rôle vérifié côté serveur).
- **SSRF** : aucun lien soumis n'est visité par le serveur. Il n'existe aucun code de récupération d'URL côté API ; ce risque est donc éliminé par conception et pas seulement filtré.

### Web

- En-têtes de sécurité et CSP envoyés par `next.config.ts`. La valeur `connect-src` est construite depuis `NEXT_PUBLIC_API_URL` (aucune URL secrète).
- Erreurs API uniformes, sans détail technique renvoyé au navigateur.
- Validation stricte des charges utiles côté API ; le client web n'est jamais la seule barrière.

### Mobile

- Jeton stocké dans `expo-secure-store` (coffre sécurisé Android), pas dans un fichier texte.
- `EXPO_PUBLIC_API_URL` doit pointer vers une adresse LAN joignable depuis le téléphone ; `localhost` sur l'appareil désigne le téléphone lui-même.

### Sauvegarde

- `npm run db:backup` crée une copie cohérente de la base SQLite de développement via l'API `backup()` de `sqlite3`.
- La commande refuse explicitement PostgreSQL et renvoie vers l'outil de l'hébergeur : aucune sauvegarde simulée.

## Limites connues et non résolues

1. **Jeton web dans `localStorage`** (`apps/web/lib/auth.ts`). Un script injecté via XSS pourrait le lire. Le passage à un cookie `HttpOnly` + `Secure` + `SameSite` est la bonne cible, mais il nécessite aussi une protection CSRF et un changement de contrat web/API. Ce n'est pas fait et n'est donc pas présenté comme terminé. La CSP réduit le risque sans le supprimer.
2. **Limitation en mémoire**. Elle protège une seule instance de production. Si plusieurs workers sont utilisés, il faudra une limite partagée (Redis) ou un proxy configuré. Redis reste optionnel et non payant en local.
3. **HTTPS/HSTS** réellement appliqué par l'hébergeur au déploiement (phase 10). L'en-tête est émis par l'API mais ne remplace pas TLS.
4. **Aucun test de pénétration externe** n'a été commandé : le budget reste 0 FCFA.

## Commandes de vérification exécutées

```powershell
npm run api:test                      # 46 passed
npm run typecheck                     # web + mobile + shared OK
npm run web:build                     # 18 routes générées
npm run db:backup                     # copie SQLite réelle créée
# Contrôle HTTP réel sur next start -p 3010 :
# GET / -> 200 avec X-Content-Type-Options: nosniff, X-Frame-Options: DENY et CSP
```

## Règle de non-régression

Aucun secret dans le code, aucun fetch serveur d'URL utilisateur, aucune accusation automatique, aucune métrique de précision présentée comme une garantie.
