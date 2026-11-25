# Déploiement Render — API et site web

Ce document décrit le déploiement gratuit de SAFECLICK sur Render, sans domaine payant. La base reste sur Neon. Aucun secret n’est écrit dans le dépôt.

## 1. Ce que contient le blueprint

Le fichier `render.yaml` à la racine définit deux services :

| Service | URL prévue | Rôle |
|---|---|---|
| `safeclick-api` | `https://safeclick-api.onrender.com` | API FastAPI, migrations au démarrage |
| `safeclick-web` | `https://safeclick-web.onrender.com` | Site Next.js standalone |

Les deux services utilisent le plan gratuit `free` et la région `ohio`, proche de la base Neon. Le plan gratuit met le service en sommeil après 15 minutes sans trafic ; la première requête suivante prend environ une minute.

## 2. Conditions à vérifier

- Compte Render gratuit, sans carte bancaire selon les conditions affichées au moment de la création.
- Projet Neon déjà créé et migré, avec sa chaîne de connexion disponible.
- Dépôt GitHub connecté à Render : `abogourinfayad07/safeclick`.
- Aucun domaine personnalisé pour l’instant : on utilise les sous-domaines `onrender.com`.

Si l’un des deux noms est déjà pris, Render ajoutera un suffixe. Dans ce cas, mets à jour `SITE_URL` côté API et `NEXT_PUBLIC_API_URL` / `EXPO_PUBLIC_API_URL` côté web dans le dashboard, puis redéploie le web.

## 3. Déployer

1. Ouvre `https://dashboard.render.com`.
2. Clique sur **New** puis **Blueprint**.
3. Connecte le dépôt GitHub `abogourinfayad07/safeclick`.
4. Sélectionne la branche `main`.
5. Render détecte `render.yaml` et affiche les deux services.
6. Quand Render demande la valeur de `DATABASE_URL`, colle la chaîne Neon. Elle est masquée dans l’interface et dans les logs.
7. Laisse `SECRET_KEY` être générée automatiquement par Render.
8. Clique sur **Apply**.

Le premier déploiement peut prendre 10 à 15 minutes : image Python, image Node, build Next.js puis migrations.

## 4. Vérifications après déploiement

Ouvre successivement :

```text
https://safeclick-api.onrender.com/health
https://safeclick-api.onrender.com/api/v1/info
https://safeclick-api.onrender.com/api/v1/billing/plans
https://safeclick-web.onrender.com/
https://safeclick-web.onrender.com/offres
```

Attendu :

- `/health` renvoie un JSON avec un statut sain ;
- `/api/v1/info` répond sans erreur ;
- `/api/v1/billing/plans` indique `paymentActive: false` ;
- le site web charge avec ses en-têtes de sécurité ;
- la page `/offres` affiche FREE, PRO et BUSINESS sans paiement actif.

Si une URL est encore froide, recharge après une minute : c’est le réveil du plan gratuit.

## 5. Variables sensibles

| Variable | Où la mettre |
|---|---|
| `DATABASE_URL` | Dashboard Render, quand le blueprint le demande |
| `SECRET_KEY` | Générée par Render (`generateValue: true`) |
| `SITE_URL` | Déjà fixée sur l’URL web prévue dans `render.yaml` |
| `NEXT_PUBLIC_API_URL` | Déjà fixée sur l’URL API prévue dans `render.yaml` |

Ne jamais remplacer `sync: false` par une valeur réelle dans `render.yaml`.

## 6. Limites connues

- Plan gratuit : sommeil après inactivité et 750 heures par mois partagées entre les services.
- Une seule réplique API : le limiteur d’abus reste en mémoire.
- Aucun SMTP configuré : l’inscription avec vérification e-mail n’est pas encore utilisable en production. Le reste de l’application, notamment l’analyse publique, fonctionne.
- Aucun domaine personnalisé ni certificate manuel : Render fournit HTTPS sur les sous-domaines.
- Les fichiers locaux sont perdus au redéploy : Neon reste la seule source de données persistante.

La procédure générale est dans [`docs/DEPLOYMENT.md`](DEPLOYMENT.md).
