# Jeu de données SAFECLICK — messages

`messages.jsonl` contient 60 exemples synthétiques en français : 30 messages de phishing et 30 messages légitimes. Chaque ligne est un objet JSON avec `text`, `label` (`phishing` ou `legitimate`) et `note`.

Aucun message réel, aucune donnée personnelle et aucun secret n'est inclus. Les exemples ont été écrits pour couvrir les motifs expliqués par le moteur de règles : urgence, demande de code, virement, usurpation, lien raccourci, promesse financière et menace de blocage.

## Limites connues

- Jeu **synthétique et réduit** : il ne mesure pas la qualité en production.
- Les métriques de `metrics.json` sont calculées sur un split deterministe (20 % test, graine 42), jamais estimées ni annoncées à l'avance.
- Le modèle est un auxiliaire explicable ; les règles restent la source principale du score.
- Aucun résultat ne doit être présenté comme une preuve ou une garantie.

## Réentraînement

Depuis la racine du dépôt :

```powershell
npm run ml:train
```

Le script réécrit `services/api/app/ml/model.json` et `services/api/datasets/metrics.json`.

## Choix technique

`scikit-learn` n'a pas pu être installé sur cette machine : Python 3.15 n'a pas de roue NumPy précompilée et aucun compilateur C n'est disponible. Le modèle utilisé est donc un Naive Bayes multinomial en Python pur, sans dépendance native, avec lissage de Laplace.
