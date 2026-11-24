"""Entraîne le modèle, l'évalue et écrit les artefacts versionnés.

Usage (depuis la racine du dépôt) :
    .\\.venv\\Scripts\\python -m app.ml.train --app-dir services/api
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dataset import load_dataset, stratified_split
from .evaluation import evaluate
from .naive_bayes import train

ROOT = Path(__file__).resolve().parents[4]
DATASET = ROOT / "services" / "api" / "datasets" / "messages.jsonl"
MODEL_PATH = ROOT / "services" / "api" / "app" / "ml" / "model.json"
METRICS_PATH = ROOT / "services" / "api" / "datasets" / "metrics.json"
MODEL_VERSION = "nb-fr-v1"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument("--model-output", type=Path, default=MODEL_PATH)
    parser.add_argument("--metrics-output", type=Path, default=METRICS_PATH)
    parser.add_argument("--test-ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--alpha", type=float, default=1.0)
    args = parser.parse_args()

    samples = load_dataset(args.dataset)
    train_samples, test_samples = stratified_split(
        samples, test_ratio=args.test_ratio, seed=args.seed
    )
    if not train_samples or not test_samples:
        raise SystemExit("Jeu de données trop petit pour l'entraînement et le test.")

    model = train(train_samples, alpha=args.alpha)
    metrics = evaluate(model, test_samples)

    model_payload = {
        "version": MODEL_VERSION,
        "labels": ["phishing", "legitimate"],
        "log_prior": model.log_prior,
        "log_likelihood": model.log_likelihood,
        "unknown_log_prob": model.unknown_log_prob,
        "vocabulary_size": model.vocabulary_size,
        "alpha": args.alpha,
        "training": {
            "dataset": "services/api/datasets/messages.jsonl",
            "train_samples": len(train_samples),
            "test_samples": len(test_samples),
            "test_ratio": args.test_ratio,
            "seed": args.seed,
        },
    }
    metrics_payload = {
        "model_version": MODEL_VERSION,
        "note": "Jeu synthétique français. Métriques calculées, non estimées.",
        "metrics": metrics.as_dict(),
    }

    args.model_output.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_output.parent.mkdir(parents=True, exist_ok=True)
    args.model_output.write_text(
        json.dumps(model_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    args.metrics_output.write_text(
        json.dumps(metrics_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(
        f"Entraîné {MODEL_VERSION} : {len(train_samples)} entraînement, "
        f"{len(test_samples)} test."
    )
    print(json.dumps(metrics.as_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
