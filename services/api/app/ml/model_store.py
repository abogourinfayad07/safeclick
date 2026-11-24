"""Charge l'artefact entraîné sans dépendance réseau ni service externe."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .naive_bayes import NaiveBayesModel

MODEL_PATH = Path(__file__).with_name("model.json")


@lru_cache(maxsize=1)
def load_model(path: Path = MODEL_PATH) -> NaiveBayesModel:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return NaiveBayesModel(
        log_prior=payload["log_prior"],
        log_likelihood=payload["log_likelihood"],
        unknown_log_prob=payload["unknown_log_prob"],
        vocabulary_size=int(payload["vocabulary_size"]),
    )


def model_version(path: Path = MODEL_PATH) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return str(payload["version"])
