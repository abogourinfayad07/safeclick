# Décisions techniques (ADR)

Chaque décision indique le contexte, les options avec avantages/inconvénients, et le choix retenu.

## ADR-001 — Monorepo avec npm workspaces

- **Options** : (a) npm workspaces, (b) pnpm workspaces, (c) Turborepo.
- **(a)** intégré à npm 11, zéro outil supplémentaire, mais moins rapide sur gros dépôt. **(b)** excellent cache disque mais pnpm absent. **(c)** CI performant mais complexité additionnelle prématurée.
- **Retenir** : **(a) npm workspaces**. Ajout de Turborepo possible en phase 10 si les temps de build le justifient.

## ADR-002 — SQLite en développement, PostgreSQL en production

- **Options** : (a) PostgreSQL local (Docker), (b) SQLite local + Postgres en prod.
- **(a)** fidèle à la prod mais Docker absent. **(b)** démarrage immédiat, mais différences de types à surveiller.
- **Retenir** : **(b)**, avec SQLAlchemy comme couche d'abstraction et `DATABASE_URL` unique. Aucune requête SQL dialecte-spécifique.

## ADR-003 — SQLAlchemy synchrone d'abord

- **Options** : (a) sync + psycopg 3, (b) async + asyncpg.
- **(a)** plus simple à tester et à déboguer pour un MVP. **(b)** meilleur parallélisme, mais complexité supérieure.
- **Retenir** : **(a)**. Migration async possible sans changer les modèles.

## ADR-004 — Analyse d'URL passive avant toute récupération réseau

- **Options** : (a) analyse de la chaîne seule, (b) fetch serveur des pages.
- **(a)** zéro risque SSRF, fonctionne hors ligne, mais moins d'informations. **(b)** détecte les redirections, mais introduit SSRF, abus et coût réseau.
- **Retenir** : **(a)** pour le MVP. Toute récupération future devra passer par un worker isolé, résolution DNS contrôlée, blocage des plages privées, interdiction de redirections vers l'interne, timeout et audit.

## ADR-005 — Règles + heuristiques avant Machine Learning

- **Options** : (a) moteur de règles explicable, (b) ML immédiat.
- **(a)** résultats immédiatement explicables et testables, mais couverture limitée. **(b)** meilleure généralisation, mais nécessite un jeu de données étiqueté et vérifié (inexistant au départ).
- **Retenir** : **(a)**, puis ajout du ML en phase 7 avec jeu de données versionné. Aucune métrique de précision ne sera annoncée sans évaluation réelle.

## ADR-006 — Expo en flux managé

- **Options** : (a) Expo managed, (b) React Native CLI / bare.
- **(a)** build et mise à jour simplifiés, idéal budget zéro ; dépendance à Expo. **(b)** contrôle natif total ; configuration Android Studio lourde.
- **Retenir** : **(a)** Expo SDK 58, avec architecture permettant un `expo prebuild` ultérieur (et donc iOS).

## ADR-007 — TypeScript 5.9.3 (web) et 6.0.3 (mobile)

- **Options** : (a) TypeScript 7 partout, (b) 5.9.3 partout, (c) version par workspace.
- **(a)** compilateur natif, mais compatibilité non garantie avec Next/shadcn et Expo. **(b)** homogène, mais `expo-doctor` exige `~6.0.3` pour le SDK 58. **(c)** chaque workspace suit l'écosystème de son framework, au prix de deux versions de `tsc` dans le monorepo.
- **Retenir** : **(c)**. Web en 5.9.3 (Next 16), mobile en 6.0.3 (Expo 58). `npm run typecheck` vérifie les deux. Réévaluation après stabilisation de TypeScript 7.

## ADR-008 — Argon2id + JWT pour l'authentification

- **Options** : (a) Argon2id + JWT court, (b) bcrypt + sessions serveur.
- **(a)** résistant aux GPU, stateless, mais révocation à prévoir. **(b)** révocation facile, mais bcrypt plus limité.
- **Retenir** : **(a)** avec `ACCESS_TOKEN_EXPIRE_MINUTES=30`, liste de révocation via `token_version` en base, et rafraîchissement à ajouter en phase 4.

## ADR-009 — Aucune dépendance payante au MVP

- **Options** : (a) API de réputation commerciales, (b) adaptateurs optionnels + règles locales.
- **(a)** meilleure couverture mais coût et engagement hors budget. **(b)** gratuit mais couverture réduite.
- **Retenir** : **(b)**. Les clés sont vides par défaut = fonctionnalité désactivée, jamais simulée.
