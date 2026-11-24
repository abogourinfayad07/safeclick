# Checklist — Phase 7 : intelligence artificielle

## Étape 1 — Jeu de données `[x]`

- [x] `services/api/datasets/messages.jsonl` : 60 exemples synthétiques français, 30 `phishing` / 30 `legitimate`
- [x] `services/api/datasets/README.md` : origine synthétique, limites et commande de réentraînement
- [x] Aucune donnée personnelle ni message réel

## Étape 2 — Entraînement sans dépendance native `[x]`

- [x] `services/api/app/ml/dataset.py` : chargement validé et split stratifié reproductible (graine 42)
- [x] `services/api/app/ml/naive_bayes.py` : Naive Bayes multinomial, lissage de Laplace, Python pur
- [x] `services/api/app/ml/train.py` : CLI reproductible via `npm run ml:train`
- [x] `services/api/app/ml/model.json` : artefact versionné `nb-fr-v1`
- [x] `services/api/datasets/metrics.json` : métriques calculées, jamais estimées

`scikit-learn` n'a pas pu être installé ici (Python 3.15 sans roue NumPy précompilée et aucun compilateur C). Le modèle Python pur évite une dépendance native et reste exécutable sur la machine vérifiée.

## Étape 3 — Évaluation mesurée `[x]`

Split 48 entraînement / 12 test, exécuté le 2026-11-24 :

| Métrique | Valeur mesurée |
|---|---:|
| TP | 6 |
| FP | 0 |
| TN | 6 |
| FN | 0 |
| accuracy | 1.0 |
| precision | 1.0 |
| recall | 1.0 |
| f1 | 1.0 |

Ces valeurs concernent **uniquement le jeu synthétique de 12 messages de test**. Elles ne constituent pas une performance en production et ne doivent jamais être présentées comme telle.

## Étape 4 — Intégration non accusatoire `[x]`

- [x] Signal `ml_statistical_signal` ajouté seulement si l'écart du modèle dépasse 1.0
- [x] Poids faible (5/100) : les règles explicites restent la source principale du score
- [x] Explication spécifique et limitation supplémentaire renvoyées au client
- [x] Version moteur persistée : `rules-v1+nb-fr-v1` pour les messages, `rules-v1` pour les URL
- [x] Aucun lien n'est visité, aucune accusation automatique

## Vérification `[x]`

- [x] `npm run ml:train` → artefacts régénérés et métriques affichées
- [x] `npm run api:test` → **41 passed**
- [x] `npm run typecheck` → web + mobile + shared OK
- [x] Commit
