"""Naive Bayésien multinomial en Python pur (aucune dépendance native)."""

import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass

from .dataset import LABELS, Sample

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKD", text.casefold())
    plain = "".join(char for char in normalized if not unicodedata.combining(char))
    return [token for token in _TOKEN_RE.findall(plain) if len(token) >= 2]


@dataclass(frozen=True, slots=True)
class NaiveBayesModel:
    log_prior: dict[str, float]
    log_likelihood: dict[str, dict[str, float]]
    unknown_log_prob: dict[str, float]
    vocabulary_size: int

    def predict_scores(self, text: str) -> dict[str, float]:
        tokens = tokenize(text)
        scores: dict[str, float] = {}
        for label in LABELS:
            score = self.log_prior[label]
            for token in tokens:
                score += self.log_likelihood[label].get(
                    token, self.unknown_log_prob[label]
                )
            scores[label] = score
        return scores

    def predict(self, text: str) -> str:
        scores = self.predict_scores(text)
        return max(scores, key=lambda label: scores[label])

    def phishing_margin(self, text: str) -> float:
        """Écart de log-vraisemblance entre phishing et légitime."""
        scores = self.predict_scores(text)
        return scores["phishing"] - scores["legitimate"]


def train(samples: list[Sample], alpha: float = 1.0) -> NaiveBayesModel:
    """Estime les probabilités avec lissage de Laplace."""
    counts: dict[str, Counter[str]] = {label: Counter() for label in LABELS}
    totals: dict[str, int] = {label: 0 for label in LABELS}
    class_sizes = Counter(sample.label for sample in samples)

    for sample in samples:
        tokens = tokenize(sample.text)
        counts[sample.label].update(tokens)
        totals[sample.label] += len(tokens)

    vocabulary = set()
    for counter in counts.values():
        vocabulary.update(counter.keys())
    vocabulary_size = max(1, len(vocabulary))

    total_samples = sum(class_sizes.values())
    if total_samples == 0:
        raise ValueError("Jeu d'entraînement vide.")

    log_prior = {
        label: math.log(class_sizes[label] / total_samples) for label in LABELS
    }
    log_likelihood = {
        label: {
            token: math.log((counts[label][token] + alpha) / (totals[label] + alpha * vocabulary_size))
            for token in vocabulary
        }
        for label in LABELS
    }
    unknown_log_prob = {
        label: math.log(alpha / (totals[label] + alpha * vocabulary_size))
        for label in LABELS
    }

    return NaiveBayesModel(
        log_prior=log_prior,
        log_likelihood=log_likelihood,
        unknown_log_prob=unknown_log_prob,
        vocabulary_size=vocabulary_size,
    )
