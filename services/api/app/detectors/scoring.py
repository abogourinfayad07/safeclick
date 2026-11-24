"""Score indicatif et classification à trois niveaux."""

from app.models.enums import RiskLevel

from .indicators import Indicator

LOW_MAX = 30
MEDIUM_MAX = 60

_RECOMMENDATIONS: dict[RiskLevel, tuple[str, ...]] = {
    RiskLevel.LOW: (
        "Vérifiez l'expéditeur même si rien n'est apparu comme suspect.",
        "N'ouvrez pas ce lien si vous n'attendiez pas ce message.",
    ),
    RiskLevel.MEDIUM: (
        "Ouvrez le site en tapant l'adresse connue dans votre navigateur.",
        "Ne saisissez aucun mot de passe ni code reçu par SMS.",
        "Confirmez la demande auprès de l'organisation par un autre canal.",
    ),
    RiskLevel.HIGH: (
        "Ne cliquez pas sur ce lien et ne transmettez aucun code.",
        "Contactez directement l'organisation via son application ou son numéro officiel.",
        "Signalez le message, puis supprimez-le après vérification.",
    ),
}

_BASE_LIMITATIONS = (
    "Analyse passive de la chaîne : SAFECLICK ne visite pas le lien.",
    "Les résultats sont indicatifs et peuvent comporter des faux positifs ou faux négatifs.",
    "Un risque faible n'est jamais une garantie de sécurité.",
)


def score_from_indicators(indicators: list[Indicator]) -> int:
    """Somme plafonnée des poids : indicatif, non probabiliste."""
    return min(100, max(0, sum(indicator.weight for indicator in indicators)))


def classify(score: int) -> RiskLevel:
    if score < LOW_MAX:
        return RiskLevel.LOW
    if score < MEDIUM_MAX:
        return RiskLevel.MEDIUM
    return RiskLevel.HIGH


def recommendations(level: RiskLevel) -> list[str]:
    return list(_RECOMMENDATIONS[level])


def limitations(kind: str) -> list[str]:
    context = (
        "L'analyse porte sur le texte du message, sans accès à son expéditeur réel."
        if kind == "message"
        else "L'analyse porte sur la structure de l'URL, sans accès à son contenu."
    )
    return [context, *_BASE_LIMITATIONS]
