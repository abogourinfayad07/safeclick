# Base PostgreSQL en ligne — Neon

L’API est préparée pour accepter une URL Neon sans modifier le code. Le mot de passe ne doit jamais être collé dans le chat, un commit ou un log.

## 1. Créer la base côté Neon

1. Va sur `https://neon.tech` et connecte-toi avec ton compte.
2. Crée un projet, par exemple `safeclick`.
3. Garde la base par défaut, souvent nommée `neondb`.
4. Dans **Connection details**, copie la chaîne de connexion. Elle ressemble à :

```text
postgresql://utilisateur:motdepasse@ep-xxxx.eu-west-2.aws.neon.tech/neondb?sslmode=require
```

Ne la colle pas ici. Les conditions de l’offre gratuite sont à vérifier directement chez Neon au moment de la création.

## 2. Ce que fait le code automatiquement

`services/api/app/core/config.py` normalise l’URL :

- `postgres://...` et `postgresql://...` deviennent `postgresql+psycopg://...` ;
- le pilote installé est `psycopg` 3, déjà présent dans `requirements.txt` ;
- si `sslmode` est absent ou trop faible, `sslmode=require` est ajouté ;
- un `sslmode` explicite valide (`require`, `verify-ca`, `verify-full`) est conservé ;
- en `ENVIRONMENT=production`, une URL SQLite est refusée au démarrage.

Aucune valeur secrète n’est écrite dans le dépôt.

## 3. Tester la connexion depuis ta machine

Si tu veux que ton environnement local pointe vers Neon, remplace temporairement dans `.env` :

```env
DATABASE_URL=<chaîne copiée depuis Neon>
```

Puis :

```powershell
npm run db:check
npm run api:migrate
```

`db:check` affiche uniquement le backend, l’hôte, la base, le résultat de `SELECT 1` et la version PostgreSQL. Il n’affiche jamais le mot de passe ni l’URL complète.

`api:migrate` est la première opération qui écrit réellement les tables dans la base en ligne. Ne lance cette commande qu’une fois par base, sauf migration supplémentaire.

Si tu veux garder ton développement local sur SQLite, ne modifie pas `.env` : mets seulement la variable dans l’environnement de production.

## 4. Déclarer le secret dans GitHub

Pour une utilisation en CI ou en déploiement :

1. Ouvre `https://github.com/abogourinfayad07/safeclick/settings/secrets/actions`
2. Clique sur **New repository secret**
3. Nom : `DATABASE_URL`
4. Valeur : la chaîne copiée depuis Neon
5. Enregistre

Ajoute de la même manière les autres secrets nécessaires plus tard :

- `SECRET_KEY`
- `SITE_URL`
- `NEXT_PUBLIC_API_URL`
- `EXPO_PUBLIC_API_URL`
- `EMAIL_BACKEND` et les variables SMTP si tu utilises l’e-mail réel

Le workflow CI actuel ne déploie pas et n’a pas besoin de ces secrets pour les tests.

### Appliquer les migrations depuis GitHub

Le fichier `.github/workflows/database.yml` permet de créer les tables dans Neon sans coller le mot de passe dans le chat :

1. Ajoute le secret `DATABASE_URL` comme indiqué ci-dessus.
2. Ouvre l’onglet **Actions** du dépôt, puis **Base de données Neon**.
3. Clique sur **Run workflow**, choisis la branche `main` et tape `MIGRER` dans le champ de confirmation.
4. Le job vérifie `SELECT 1`, puis exécute `alembic upgrade head`.

GitHub masque la valeur du secret dans les logs. La commande `db_check` n’affiche que l’hôte et la base, jamais l’URL complète ni le mot de passe. Le job est manuel : aucun déclenchement automatique n’est prévu.

## 5. Vérification de production

Avec les variables exportées dans la session PowerShell :

```powershell
python scripts\preflight.py --mode deploy
npm run db:check
npm run api:migrate
```

Le mode `deploy` refuse déjà : URL non HTTPS, SQLite, `SECRET_KEY` faible, `EMAIL_BACKEND=console` et limitation d’abus désactivée.

## 6. Sauvegardes

Neon propose ses propres sauvegardes et restauration dans son tableau de bord. `npm run db:backup` reste réservé à SQLite local et refuse explicitement PostgreSQL.

La procédure complète de déploiement est dans [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).
