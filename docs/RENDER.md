# Déploiement Render — API et site web

Ce document décrit le déploiement gratuit de SAFECLICK sur Render, sans domaine payant. La base reste sur Neon. Aucun secret n’est écrit dans le dépôt.

## 1. État réel du déploiement

Le déploiement a été effectué manuellement depuis le dashboard Render, en suivant les mêmes valeurs que `render.yaml`. Le blueprint reste la référence reproductible dans le dépôt.

| Service Render | URL publique | Rôle |
|---|---|---|
| `safeclick` | `https://safeclick-btd6.onrender.com` | API FastAPI, migrations au démarrage |
| `safeclick-web` | `https://safeclick-web.onrender.com` | Site Next.js standalone |

Le nom `safeclick` étant déjà pris sur Render, l’API a reçu le suffixe `-btd6`. Toutes les URLs publiques utilisent donc ce suffixe. Les deux services sont en région `oregon` et en plan gratuit `free`.

Le plan gratuit met le service en sommeil après 15 minutes sans trafic ; la première requête suivante prend environ une minute.

## 2. Vérifications effectuées

Les réponses suivantes ont été contrôlées après déploiement :

```text
https://safeclick-btd6.onrender.com/health
https://safeclick-btd6.onrender.com/api/v1/info
https://safeclick-btd6.onrender.com/api/v1/billing/plans
https://safeclick-web.onrender.com/
https://safeclick-web.onrender.com/offres
```

Résultats :

- `/health` → `{"status":"ok","database":"ok","environment":"production","version":"0.1.0"}` ;
- `/api/v1/info` → OK, contraintes et disclaimer affichés ;
- `/api/v1/billing/plans` → `paymentActive: false`, offres FREE / PRO / BUSINESS ;
- site web → page d’accueil et page `/offres` chargées ;
- CORS → `access-control-allow-origin: https://safeclick-web.onrender.com` ;
- en-têtes web → CSP avec `connect-src 'self' https://safeclick-btd6.onrender.com`, HSTS côté API, `nosniff`, `DENY`, `no-referrer`.

Un risque faible reste toujours indicatif et n’est jamais une garantie de sécurité.

## 3. Configuration des services

### API `safeclick`

| Variable | Valeur |
|---|---|
| `ENVIRONMENT` | `production` |
| `PORT` | `8000` |
| `API_V1_PREFIX` | `/api/v1` |
| `DATABASE_URL` | secret saisi dans le dashboard, jamais dans le dépôt |
| `SECRET_KEY` | générée par Render |
| `SITE_URL` | `https://safeclick-web.onrender.com` |
| `NEXT_PUBLIC_API_URL` | `https://safeclick-btd6.onrender.com` |
| `EXPO_PUBLIC_API_URL` | `https://safeclick-btd6.onrender.com` |
| `EMAIL_BACKEND` | `console` |
| `RATE_LIMIT_ENABLED` | `true` |
| `RATE_LIMIT_PER_MINUTE` | `60` |

**Docker Command** — obligatoire sur le plan gratuit, car `preDeployCommand` est réservé aux plans payants :

```sh
/bin/sh -c "python -m alembic -c services/api/alembic.ini upgrade head && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir services/api"
```

**Health Check Path** : `/health`

### Web `safeclick-web`

| Variable | Valeur |
|---|---|
| `ENVIRONMENT` | `production` |
| `PORT` | `3000` |
| `NEXT_PUBLIC_API_URL` | `https://safeclick-btd6.onrender.com` |
| `EXPO_PUBLIC_API_URL` | `https://safeclick-btd6.onrender.com` |

**Health Check Path** : `/`

`NEXT_PUBLIC_API_URL` est intégré au build Next.js. Toute modification exige un nouveau build du service web. Render transmet automatiquement les variables d’environnement comme arguments de build Docker.

## 4. Redéployer après une modification

1. Dashboard Render → service concerné → **Environment** ou **Settings**.
2. Modifier la valeur.
3. Choisir **Save, rebuild, and deploy**.
4. Vérifier les logs puis les URLs de la section 2.

Si `NEXT_PUBLIC_API_URL` ou `EXPO_PUBLIC_API_URL` change, redéployer aussi le web. Si `SITE_URL` change, redéployer l’API pour que le CORS suive.

## 5. Limites connues

- Plan gratuit : sommeil après inactivité et 750 heures par mois partagées entre les services.
- Une seule réplique API : le limiteur d’abus reste en mémoire.
- Aucun SMTP configuré : l’inscription avec vérification e-mail n’est pas encore utilisable en production. Le reste de l’application, notamment l’analyse publique, fonctionne.
- Aucun domaine personnalisé ni certificat manuel : Render fournit HTTPS sur les sous-domaines `onrender.com`.
- Les fichiers locaux sont perdus au redéploy : Neon reste la seule source de données persistante.
- Aucun abonnement payant ni service Render supplémentaire n’a été souscrit.

La procédure générale est dans [`docs/DEPLOYMENT.md`](DEPLOYMENT.md).
