"""Chargement du jeu étiqueté et division déterminaire entraînement/test."""

import json
import random
from dataclasses import dataclass
from pathlib import Path

LABELS = ("phishing", "legitimate")


@dataclass(frozen=True, slots=True)
class Sample:
    text: str
    label: str
    note: str


def load_dataset(path: Path) -> list[Sample]:
    samples: list[Sample] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        payload = json.loads(line)
        label = payload.get("label")
        if label not in LABELS:
            raise ValueError(f"Étiquette inconnue ligne {line_number} : {label!r}")
        samples.append(
            Sample(
                text=str(payload["text"]),
                label=str(label),
                note=str(payload.get("note", "")),
            )
        )
    return samples


def stratified_split(
    samples: list[Sample], test_ratio: float = 0.2, seed: int = 42
) -> tuple[list[Sample], list[Sample]]:
    """Division reproductible, proportionnelle à chaque classe."""
    if not 0.0 < test_ratio < 1.0:
        raise ValueError("test_ratio doit être compris entre 0 et 1.")

    rng = random.Random(seed)
    train: list[Sample] = []
    test: list[Sample] = []
    for label in LABELS:
        group = [sample for sample in samples if sample.label == label]
        rng.shuffle(group)
        test_count = max(1, round(len(group) * test_ratio))
        test.extend(group[:test_count])
        train.extend(group[test_count:])
    return train, test
