# Checklist — Phase 3 : moteur de détection

## Étape 1 — Règles URL et message `[x]`

- [x] `app/detectors/indicators.py`, `scoring.py` (seuils 30 / 60 documentés)
- [x] `app/detectors/url.py` : analyse passive, aucun fetch réseau
- [x] Signaux : scheme http, Unicode, homoglyphes, punycode, sous-domaines, marques, raccourcisseurs, IP, requêtes sensibles
- [x] `app/detectors/message.py` : urgence, argent, codes, usurpation, menace, lien, contact privé, majuscules
- [x] Tests unitaires : URL bénigne/suspecte/punycode, message bénin/phishing

## Étape 2 — API d'analyse `[x]`

- [x] Schémas Pydantic stricts (2048 / 4000, `extra="forbid"`)
- [x] Persistance `analyses` : `input_hash` HMAC et extrait limité, jamais le contenu complet
- [x] `POST /api/v1/analyze/url` et `POST /api/v1/analyze/message`
- [x] Réponse camelCase alignée sur `packages/shared` (`riskLevel`, `createdAt`)
- [x] Tests HTTP : contrat, explications, validation, persistance

## Vérification `[x]`

- [x] `npm run api:test` → **27 passed**
- [x] Aucune métrique de précision inventée ; limites obligatoires dans chaque réponse
- [x] Commit

> Seuils indicatifs : 0-29 = faible, 30-59 = moyen, 60-100 = élevé.  
> Ce ne sont pas des probabilités validées.
