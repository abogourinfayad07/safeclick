"""Métriques calculées sur les prédictions réelles, jamais estimées."""

from dataclasses import dataclass

from .dataset import Sample
from .naive_bayes import NaiveBayesModel

POSITIVE = "phishing"


@dataclass(frozen=True, slots=True)
class Metrics:
    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int
    accuracy: float
    precision: float
    recall: float
    f1: float

    def as_dict(self) -> dict[str, float | int]:
        return {
            "tp": self.true_positive,
            "fp": self.false_positive,
            "tn": self.true_negative,
            "fn": self.false_negative,
            "accuracy": round(self.accuracy, 4),
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1": round(self.f1, 4),
        }


def evaluate(model: NaiveBayesModel, samples: list[Sample]) -> Metrics:
    tp = fp = tn = fn = 0
    correct = 0
    for sample in samples:
        prediction = model.predict(sample.text)
        if prediction == POSITIVE and sample.label == POSITIVE:
            tp += 1
        elif prediction == POSITIVE and sample.label != POSITIVE:
            fp += 1
        elif prediction != POSITIVE and sample.label != POSITIVE:
            tn += 1
        else:
            fn += 1
        if prediction == sample.label:
            correct += 1

    total = len(samples)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return Metrics(
        true_positive=tp,
        false_positive=fp,
        true_negative=tn,
        false_negative=fn,
        accuracy=correct / total if total else 0.0,
        precision=precision,
        recall=recall,
        f1=f1,
    )
