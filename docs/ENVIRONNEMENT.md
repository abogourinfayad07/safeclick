# Environnement vérifié — 24 novembre 2026

Toutes les valeurs ci-dessous ont été **obtenues par commande**, pas supposées.

## Système

| Élément | Résultat | Commande utilisée |
|---|---|---|
| OS | Microsoft Windows 11 Professionnel, 10.0.26300, 64 bits | `Get-CimInstance Win32_OperatingSystem` |
| Disque C: | ~191 Go libres / ~319 Go utilisés | `Get-PSDrive C` |
| Dossier de travail | `C:\Users\HP\OneDrive\Documents\Projet par défaut` (vide au départ) | `Get-ChildItem -Force` |

## Outils présents

| Outil | Version | Chemin |
|---|---|---|
| node.exe | v26.13.1 | `C:\Program Files\nodejs\node.exe` |
| npm.ps1 | 11.20.0 | `C:\Program Files\nodejs\npm.ps1` |
| python.exe | 3.15.2 | `C:\Users\HP\AppData\Local\Programs\Python\Python315\python.exe` |
| py.exe | Launcher | `C:\Users\HP\AppData\Local\Programs\Python\Launcher\py.exe` |
| pip.exe | 26.2.2 | `...\Python315\Scripts\pip.exe` |
| git.exe | 2.56.0.windows.4 | `C:\Program Files\Git\cmd\git.exe` |

Identité Git globale : `Fayad <abogourinfayad07@gmail.com>`.

## Outils absents du PATH

| Outil | Conséquence | Décision |
|---|---|---|
| Docker / Docker Desktop | `docker compose up` indisponible localement | SQLite en développement, `docker-compose.yml` fourni pour la prod mais **non testé ici** |
| pnpm, yarn | — | npm workspaces suffisent |
| VS Code (`Code.exe`) | non détecté au chemin standard | à confirmer par l'utilisateur ; les commandes restent valables dans n'importe quel terminal |

## Compatibilités vérifiées

### JavaScript (registre npm)

| Paquet | Version retenue | Vérification |
|---|---|---|
| next | 16.4.6 | peer React `^19.0.0` ✅ |
| react / react-dom | 19.3.1 | cohérent avec Next 16 et RN 0.88 ✅ |
| react-native | 0.88.1 | peer `react ^19.3.0` ✅ |
| expo | 58.0.26 | `engines.node` accepte `^26.0.0` ✅ |
| tailwindcss / @tailwindcss/postcss | 4.3.5 | versions alignées ✅ |
| typescript | 5.9.3 | volontairement **pas TypeScript 7** (outillage Next/shadcn non garanti) |
| @types/node | 26.6.6 | aligné Node 26 |
| lucide-react | 1.79.0 | icônes |

### Python (`python -m pip install --dry-run`)

Résolution réussie sur CPython 3.15 (des wheels `cp315` existent) :

- fastapi 0.165.0, pydantic 2.14.4, pydantic-core 2.50.5 (cp315), SQLAlchemy 2.1.9
- scikit-learn 1.9.1, numpy 2.5.5, scipy 1.18.1
- uvicorn 0.54.0, alembic 1.20.1, argon2-cffi 25.1.0, PyJWT 2.15.1
- psycopg[binary] 3.3.9, redis 8.2.0, pytest 9.2.0, httpx 0.28.1

> `pip` affiche des notices sur `stderr` sous PowerShell ; la ligne `Would install ...` confirme que la résolution est valide. Rien n'a été installé définitivement (`--dry-run`).

## Contraintes qui en découlent

1. **Pas de PostgreSQL local** tant que Docker n'est pas installé → `DATABASE_URL=sqlite:///./data/safeclick.db` en dev. Le code SQLAlchemy doit rester agnostique (Pas d'SQL spécifique Postgres dans les requêtes).
2. **Pas d'API de réputation payante** → adaptateurs optionnels avec clés vides = désactivés. Aucune donnée de réputation inventée.
3. **Pas d'émulateur Android** → tests via Expo Go sur téléphone physique + `npx expo-doctor` sur PC.
4. **Node 26 / Python 3.15 sont récents** → versions épinglées dans les manifests ; toute mise à jour majeure sera testée séparément.
