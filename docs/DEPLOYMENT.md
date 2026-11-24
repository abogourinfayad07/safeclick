# Déploiement SAFECLICK — préparation sans publication

Ce document décrit ce qui est **prêt dans le dépôt** et ce qui reste à faire par le propriétaire. Aucun compte, domaine, certificat, abonnement ou publication n'a été créé automatiquement.

## 1. Ce qui est prêt

| Élément | Fichier | État |
|---|---|---|
| Tests, typecheck, build, audit | `.github/workflows/ci.yml` | Prêt à s'exécuter au premier push |
| Vérification Expo + export Android | `.github/workflows/ci.yml` | Prête |
| Validation et build Docker | `.github/workflows/ci.yml` | Prête ; non exécutée localement (Docker absent) |
| Image API | `services/api/Dockerfile` | Prête |
| Image web | `apps/web/Dockerfile` | Prête, sortie Next standalone |
| Composition des services | `docker-compose.yml` | Prête ; PostgreSQL + API + web, Redis optionnel |
| Pré-vérification | `scripts/preflight.py`, `npm run deploy:preflight` | Prête |
| Limites de sécurité | `docs/SECURITE.md` | Documentées |

Le workflow CI ne contient **aucun job de déploiement** : il ne publie rien et ne touche pas à la production.

## 2. Variables à fournir

Toutes les valeurs sont lues depuis l'environnement du processus ou d'un `.env` local non suivi par Git. Les exemples ci-dessous sont fictifs.

| Variable | Production attendue | Remarque |
|---|---|---|
| `ENVIRONMENT` | `production` | Active notamment HSTS côté API |
| `SECRET_KEY` | valeur aléatoire d'au moins 32 caractères | Jamais dans le dépôt |
| `SITE_URL` | `https://<votre-domaine>` | Doit correspondre exactement à l'origine web pour le CORS |
| `NEXT_PUBLIC_API_URL` | `https://api.<votre-domaine>` | Valeur publique intégrée au build web |
| `EXPO_PUBLIC_API_URL` | `https://api.<votre-domaine>` | Valeur publique intégrée au bundle mobile |
| `DATABASE_URL` | `postgresql+psycopg://...` | SQLite refusé en production par la pré-vérification |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | valeurs choisies | Le mot de passe par défaut du compose est un placeholder |
| `EMAIL_BACKEND` | `smtp` | `console` interdit en production par la pré-vérification |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM` | fournis par l'hébergeur d'e-mail | Aucun service payant imposé |
| `RATE_LIMIT_ENABLED` | `true` | Une seule réplique API tant qu'un limiteur partagé n'est pas ajouté |
| `RATE_LIMIT_PER_MINUTE` | `60` ou valeur choisie | Par IP et par groupe de routes |

Génération locale d'une clé, sans l'écrire dans un fichier suivi :

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## 3. Pré-vérification

```powershell
cd "C:\Users\HP\OneDrive\Documents\Projet par défaut"

# Vérifications reproductibles, sans exigence de production
python scripts\preflight.py --mode local

# Contrôle des variables de production (à exporter d'abord dans la session)
python scripts\preflight.py --mode deploy
```

Le mode `deploy` refuse notamment : `ENVIRONMENT` absent, `SECRET_KEY` faible ou placeholder, URL non HTTPS, SQLite, `EMAIL_BACKEND=console`, limitation d'abus désactivée, `.env` suivi par Git ou motif de clé privée dans un fichier suivi.

## 4. Démarrage Docker sur le serveur

```powershell
$env:ENVIRONMENT = "production"
$env:SECRET_KEY = "<valeur generee>"
$env:SITE_URL = "https://safeclick.example"
$env:NEXT_PUBLIC_API_URL = "https://api.safeclick.example"
$env:EXPO_PUBLIC_API_URL = "https://api.safeclick.example"
$env:POSTGRES_USER = "safeclick"
$env:POSTGRES_PASSWORD = "<mot-de-passe-aleatoire>"
$env:POSTGRES_DB = "safeclick"
$env:DATABASE_URL = "postgresql+psycopg://safeclick:<mot-de-passe-aleatoire>@postgres:5432/safeclick"
$env:EMAIL_BACKEND = "smtp"
$env:SMTP_HOST = "<fourni-par-l-hebergeur>"
$env:SMTP_USER = "<fourni-par-l-hebergeur>"
$env:SMTP_PASSWORD = "<fourni-par-l-hebergeur>"
$env:EMAIL_FROM = "ne-pas-repondre@safeclick.example"

docker compose up -d --build
docker compose ps
```

L'API applique les migrations Alembic au démarrage puis expose `/health`. Le web attend que l'API soit saine. Redis n'est démarré que si vous utilisez le profil :

```powershell
docker compose --profile cache up -d
```

**Important :** `NEXT_PUBLIC_API_URL` est intégré au build web. Le changer après coup exige `docker compose up -d --build web`. La limitation d'abus étant en mémoire, ne pas lancer plusieurs répliques API tant qu'un limiteur partagé n'est pas implémenté.

## 5. HTTPS et domaine

Le compose expose HTTP en interne. La terminaison TLS doit être faite par un reverse proxy ou par l'hébergeur. Exemple indicatif avec Caddy, à adapter avec le domaine réel :

```text
safeclick.example {
    reverse_proxy web:3000
}

api.safeclick.example {
    reverse_proxy api:8000
}
```

Caddy peut obtenir des certificats Let's Encrypt gratuitement. Aucun certificat ni DNS n'a été configuré ici. L'en-tête HSTS est émis par l'API dès `ENVIRONMENT=production`, mais il ne remplace pas TLS.

Le CORS n'autorise que `SITE_URL` et les en-têtes `Authorization`, `Content-Type` et `X-API-Key`. Si le domaine change, mettre à jour `SITE_URL` et reconstruire le web.

## 6. Sauvegardes

`npm run db:backup` ne fonctionne qu'avec SQLite et refuse explicitement PostgreSQL. En production, utiliser l'outil de l'hébergeur ou `pg_dump` :

```powershell
New-Item -ItemType Directory -Force -Path backups | Out-Null
docker compose exec -T postgres pg_dump -U safeclick safeclick | Out-File -Encoding utf8 "backups\safeclick-$(Get-Date -Format yyyyMMdd-HHmmss).sql"
```

Restoration, à utiliser uniquement après vérification de la cible :

```powershell
Get-Content "backups\le-fichier.sql" | docker compose exec -T postgres psql -U safeclick safeclick
```

Le dossier `backups\` est ignoré par Git.

## 7. Rollback

```powershell
git log --oneline -5
git checkout <commit-stable>
docker compose up -d --build
docker compose ps
docker compose logs --tail=100 api
```

Le volume PostgreSQL n'est pas supprimé par `docker compose down`. Ne jamais le supprimer sans sauvegarde vérifiée.

## 8. Android

Le bundle Metro est vérifié par `npm run mobile:export`. La publication réelle nécessite un compte développeur, une signature et l'accord explicite du propriétaire. Aucun APK/AAB n'a été publié.

## 9. Étapes encore manuelles

1. Créer le dépôt distant et pousser `main` pour exécuter le CI.
2. Définir les secrets GitHub si un job de déploiement est ajouté plus tard ; aucun n'est requis aujourd'hui.
3. Choisir l'hébergeur avec Docker et PostgreSQL, puis configurer le serveur.
4. Acheter/configurer le domaine et les DNS.
5. Mettre en place le reverse proxy HTTPS et les sauvegardes automatiques.
6. Activer une surveillance externe simple (healthcheck + alertes).
7. Décider de la publication Android et des tarifs PRO/BUSINESS.

Aucune de ces étapes n'a été exécutée automatiquement et aucune dépense n'a été engagée.
