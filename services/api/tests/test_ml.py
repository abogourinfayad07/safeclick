"""Entraînement local, évaluation mesurée et intégration non accusatoire."""

from pathlib import Path

from app.detectors.message import analyze_message
from app.ml.dataset import load_dataset, stratified_split
from app.ml.evaluation import evaluate
from app.ml.model_store import load_model, model_version
from app.ml.naive_bayes import train

DATASET = Path(__file__).resolve().parents[1] / "datasets" / "messages.jsonl"


def test_dataset_is_balanced_and_labelled() -> None:
    samples = load_dataset(DATASET)

    assert len(samples) == 60
    assert sum(sample.label == "phishing" for sample in samples) == 30
    assert sum(sample.label == "legitimate" for sample in samples) == 30
    assert all(sample.text.strip() and sample.note for sample in samples)


def test_split_is_reproducible_and_stratified() -> None:
    samples = load_dataset(DATASET)

    first_train, first_test = stratified_split(samples, seed=42)
    second_train, second_test = stratified_split(samples, seed=42)

    assert [sample.text for sample in first_train] == [sample.text for sample in second_train]
    assert [sample.text for sample in first_test] == [sample.text for sample in second_test]
    for group in (first_train, first_test):
        assert sum(sample.label == "phishing" for sample in group) == len(group) // 2


def test_training_and_evaluation_are_measured() -> None:
    train_samples, test_samples = stratified_split(load_dataset(DATASET))
    model = train(train_samples)
    metrics = evaluate(model, test_samples).as_dict()

    assert metrics["tp"] + metrics["fp"] + metrics["tn"] + metrics["fn"] == len(test_samples)
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["precision"] <= 1.0
    assert 0.0 <= metrics["recall"] <= 1.0
    assert metrics["accuracy"] > 0.7


def test_serialized_model_is_usable_offline() -> None:
    model = load_model()

    assert model_version() == "nb-fr-v1"
    assert model.predict("URGENT : envoyez votre code OTP et votre mot de passe.") == "phishing"
    assert model.predict("Bonjour, voici le document dont on a parlé ce matin.") == "legitimate"


def test_ml_signal_is_explained_and_does_not_flag_benign_message() -> None:
    phishing = analyze_message(
        "URGENT!!! Votre compte sera bloqué. Envoyez votre code OTP et "
        "votre mot de passe à votre banque par mail immédiatement."
    )
    benign = analyze_message(
        "Bonjour, voici le document dont on a parlé ce matin. À bientôt."
    )

    assert "ml_statistical_signal" in {item.code for item in phishing["indicators"]}
    assert "ml_statistical_signal" not in {item.code for item in benign["indicators"]}
    assert any("60 exemples synthétiques" in item for item in phishing["limitations"])
    assert phishing["engine_version"] == "rules-v1+nb-fr-v1"
