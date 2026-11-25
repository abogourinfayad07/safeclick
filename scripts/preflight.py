#!/usr/bin/env python3
"""Pré-vérification SAFECLICK avant déploiement.

Mode `local` : exécute les vérifications reproductibles sur la machine courante.
Mode `deploy` : contrôle en plus les variables d'environnement de production.
Aucun secret n'est écrit dans ce fichier et aucun service n'est contacté.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMANDS = [
    ["npm", "run", "api:test"],
    ["npm", "run", "typecheck"],
    ["npm", "run", "web:build"],
    ["npm", "audit", "--audit-level=moderate"],
]

FORBIDDEN_PATTERNS = [
    r"BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY",
    r"AKIA[0-9A-Z]{16}",
    r"sk-[A-Za-z0-9]{24,}",
]


def _valid_secret(value: str) -> bool:
    lowered = value.lower()
    return len(value) >= 32 and "remplacez" not in lowered and "dev-only" not in lowered


def _valid_https(value: str) -> bool:
    return value.startswith("https://") and "localhost" not in value and "127.0.0.1" not in value


def _valid_database_url(value: str) -> bool:
    # Neon fournit souvent postgres://... ; l'API ajoute automatiquement le pilote.
    return value.strip().startswith(
        ("postgresql+psycopg://", "postgresql://", "postgres://")
    )


REQUIRED_DEPLOY_ENV = {
    "ENVIRONMENT": lambda value: value == "production",
    "SECRET_KEY": _valid_secret,
    "SITE_URL": _valid_https,
    "NEXT_PUBLIC_API_URL": _valid_https,
    "DATABASE_URL": _valid_database_url,
    "EMAIL_BACKEND": lambda value: bool(value) and value != "console",
    "RATE_LIMIT_ENABLED": lambda value: value.lower() in {"1", "true", "yes"},
}


def load_env_file(path: Path) -> dict[str, str]:
    """Lecture minimale de KEY=VALUE, sans dépendance externe."""
    if not path.is_file():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def environment_values(env_file: Path) -> dict[str, str]:
    """L'environnement du processus prévaut sur le fichier .env."""
    return {**load_env_file(env_file), **dict(os.environ)}


def check_repository() -> list[str]:
    problems: list[str] = []
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        return ["Impossible de lister les fichiers suivis par Git."]

    tracked = result.stdout.splitlines()
    if ".env" in tracked:
        problems.append("Le fichier .env est suivi par Git : retirez-le de l'index.")

    for name in tracked:
        path = ROOT / name
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, content):
                problems.append(f"Motif de secret potentiel détecté dans {name}.")
                break

    return problems


def check_deploy_env(values: dict[str, str]) -> list[str]:
    problems: list[str] = []
    for key, validator in REQUIRED_DEPLOY_ENV.items():
        value = values.get(key, "")
        if not validator(value):
            problems.append(f"{key} absent ou invalide pour la production.")
    return problems


def run_command(command: list[str]) -> None:
    executable = shutil.which(command[0]) or command[0]
    printable = " ".join(command)
    print(f"\n> {printable}", flush=True)
    result = subprocess.run([executable, *command[1:]], cwd=ROOT, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def check_compose(values: dict[str, str]) -> None:
    if shutil.which("docker") is None:
        print("\n> Docker absent : validation du compose ignorée localement.")
        return

    env = dict(values)
    env.setdefault("SECRET_KEY", "preflight-local-only-secret-longer-than-thirty-two-chars")
    print("\n> docker compose config --quiet", flush=True)
    result = subprocess.run(
        ["docker", "compose", "-f", "docker-compose.yml", "config", "--quiet"],
        cwd=ROOT,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["local", "deploy"], default="local")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--skip-commands", action="store_true")
    args = parser.parse_args()

    print(f"SAFECLICK pré-vérification — mode {args.mode}")
    values = environment_values(ROOT / args.env_file)

    problems = check_repository()
    if args.mode == "deploy":
        problems.extend(check_deploy_env(values))

    if problems:
        print("\nÉchecs de configuration :")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("Configuration conforme (aucun secret suivi, variables requises valides).")

    check_compose(values)

    if not args.skip_commands:
        for command in COMMANDS:
            run_command(command)

    print("\nPré-vérification terminée avec succès.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
