"""Analyse de messages : règles françaises explicites et pondérées."""

import re

from app.models.enums import AnalysisKind

from .indicators import Indicator
from .scoring import classify, limitations, recommendations, score_from_indicators

_RULES: tuple[tuple[str, str, str, int, re.Pattern[str]], ...] = (
    (
        "urgency",
        "Urgence excessive",
        "Le message insiste pour obtenir une réaction immédiate.",
        12,
        re.compile(
            r"\b(urgent|imm[eé]diatement|maintenant|derni[eè]re chance|"
            r"dans les (5|cinq|10|dix) minutes|ne tardez pas| sans attendre)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "money_request",
        "Demande d'argent",
        "Le message demande un virement, un paiement ou une carte cadeau.",
        16,
        re.compile(
            r"\b(virement|envoyez (?:de l'|d')?argent|paiement|esp[eè]ces|"
            r"mandat cash|carte cadeau|transfert d'argent|payez|rib|iban)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "code_request",
        "Demande de code ou de mot de passe",
        "Le message réclame un code, un mot de passe ou une validation 2FA.",
        18,
        re.compile(
            r"\b(code|mot de passe|otp|2fa|cl[eé] de v[eé]rification|"
            r"code de v[eé]rification|code re[uû] par sms)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "impersonation",
        "Usurpation d'identité",
        "Le message cite une organisation sans preuve de son authenticité.",
        12,
        re.compile(
            r"\b(banque|assurance|caisse|imp[oô]ts?|sncf|orange|"
            r"whatsapp|administrateur|service client|direction|carbon?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "reward",
        "Promesse financière",
        "Le message promet un gain ou un avantage financier inhabituel.",
        12,
        re.compile(
            r"\b(gagn[eé]|loterie|jackpot|cadeau|prime|b[eé]n[eé]fice|"
            r"argent facile|remboursement exceptionnel)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "threat",
        "Menace de blocage",
        "Le message menace de bloquer ou fermer un compte.",
        12,
        re.compile(
            r"\b(compte[^.]{0,40}bloqu[eé]|suspendu|r[eé]siliation|"
            r"fermeture de compte|perte de votre compte)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "embedded_link",
        "Lien intégré",
        "Le message contient un lien dont la destination doit être vérifiée.",
        6,
        re.compile(r"https?://|www\.|bit\.ly|tinyurl", re.IGNORECASE),
    ),
    (
        "private_contact",
        "Demande de contact privé",
        "Le message demande de répondre hors du canal habituel.",
        8,
        re.compile(
            r"\b(r[eé]pondez (?:ici|par)|contactez-moi|appelez ce num[eé]ro|par mail)\b",
            re.IGNORECASE,
        ),
    ),
)


def analyze_message(raw: str) -> dict[str, object]:
    """Évalue un texte sans interpréter l'expéditeur ni joindre de service externe."""
    text = raw.strip()
    indicators: list[Indicator] = []

    for code, label, detail, weight, pattern in _RULES:
        if pattern.search(text):
            indicators.append(
                Indicator(code=code, label=label, detail=detail, weight=weight)
            )

    letters = [character for character in text if character.isalpha()]
    if len(letters) >= 20:
        upper_ratio = sum(character.isupper() for character in letters) / len(letters)
        if upper_ratio > 0.35:
            indicators.append(
                Indicator(
                    code="excessive_caps",
                    label="Majuscules excessives",
                    detail="Le message utilise beaucoup de majuscules pour forcer l'attention.",
                    weight=8,
                )
            )

    if text.count("!") >= 3:
        indicators.append(
            Indicator(
                code="repeated_exclamation",
                label="Points d'exclamation répétés",
                detail="La ponctuation cherche à créer un sentiment d'urgence.",
                weight=6,
            )
        )

    score = score_from_indicators(indicators)
    level = classify(score)
    return {
        "kind": AnalysisKind.MESSAGE,
        "risk_level": level,
        "score": score,
        "indicators": indicators,
        "recommendations": recommendations(level),
        "limitations": limitations("message"),
    }
