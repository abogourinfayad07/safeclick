"""Analyse passive d'URL : aucune résolution DNS et aucun fetch serveur."""

import ipaddress
import re
from urllib.parse import unquote, urlparse

from app.models.enums import AnalysisKind

from .indicators import Indicator
from .scoring import classify, limitations, recommendations, score_from_indicators

_SCHEME_RE = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.-]*)://")
_HOMOGLYPHS = str.maketrans(
    {
        "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x",
        "і": "i", "ѕ": "s", "ԁ": "d", "у": "y", "т": "t", "н": "h",
    }
)
_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
    "cutt.ly", "rebrand.ly", "buff.ly", "s.id", "rb.gy", "shorturl.at",
}
_BRANDS = (
    "paypal", "facebook", "instagram", "google", "apple", "amazon",
    "whatsapp", "orange", "bnpp", "caisse", "impots", "sncf", "airbnb",
)
_SENSITIVE_QUERY = (
    "password", "mdp", "code", "otp", "verif", "compte", "banque",
    "login", "secure", "connexion",
)


def analyze_url(raw: str) -> dict[str, object]:
    """Retourne un contrat d'analyse sans jamais contacter le site visé."""
    value = raw.strip()
    scheme_match = _SCHEME_RE.match(value)
    scheme = scheme_match.group(1).lower() if scheme_match else "https"
    candidate = value if scheme_match else f"https://{value}"
    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower()
    labels = [label for label in host.split(".") if label]

    indicators: list[Indicator] = []

    def add(code: str, label: str, detail: str, weight: int) -> None:
        indicators.append(Indicator(code, label, detail, weight))

    if scheme == "http":
        add(
            "insecure_scheme",
            "Lien non chiffré",
            "Le lien utilise http:// plutôt que https://.",
            8,
        )

    if any(ord(character) > 127 for character in host):
        add(
            "unicode_host",
            "Caractères inhabituels dans le domaine",
            "Le domaine contient des caractères non ASCII.",
            14,
        )

    if host.translate(_HOMOGLYPHS) != host:
        add(
            "homoglyph",
            "Lettres visuellement proches",
            "Le domaine mêle des lettres de paramètres linguistiques différents.",
            20,
        )

    if "xn--" in host:
        add(
            "punycode",
            "Domaine encodé",
            "Le domaine utilise la forme punycode (xn--).",
            10,
        )

    if len(labels) > 4:
        add(
            "many_subdomains",
            "Sous-domaines nombreux",
            f"Le domaine contient {len(labels)} segments.",
            8,
        )

    if any(len(label) > 40 for label in labels):
        add(
            "long_label",
            "Segment de domaine très long",
            "Un segment dépasse 40 caractères.",
            8,
        )

    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        add(
            "ip_host",
            "Adresse IP directe",
            "Le lien pointe vers une adresse IP au lieu d'un nom de domaine.",
            14,
        )

    if any(host == shortener or host.endswith(f".{shortener}") for shortener in _SHORTENERS):
        add(
            "shortener",
            "Raccourcisseur de lien",
            "La destination réelle n'est pas visible dans le lien.",
            12,
        )

    if len(labels) >= 3:
        subdomains = labels[:-2]
        if any(brand in subdomain for brand in _BRANDS for subdomain in subdomains):
            add(
                "brand_in_subdomain",
                "Marque placée en sous-domaine",
                "Une marque connue apparaît avant le domaine principal.",
                18,
            )

    if any("-" in label and brand in label for label in labels for brand in _BRANDS):
        add(
            "brand_with_hyphen",
            "Marque associée à un tiret",
            "Le domaine contient une marque et un tiret, motif fréquent d'usurpation.",
            12,
        )

    query = unquote(parsed.query).casefold()
    if any(word in query for word in _SENSITIVE_QUERY):
        add(
            "sensitive_query",
            "Données sensibles demandées dans l'adresse",
            "L'adresse contient un terme lié à un mot de passe, un code ou une connexion.",
            10,
        )

    if len(value) > 300:
        add(
            "very_long_url",
            "Adresse très longue",
            "Une adresse exceptionnellement longue peut masquer la destination.",
            6,
        )

    if not host or "." not in host:
        add(
            "atypical_host",
            "Domaine atypique",
            "La structure du domaine est inhabituelle.",
            10,
        )

    score = score_from_indicators(indicators)
    level = classify(score)
    return {
        "kind": AnalysisKind.URL,
        "risk_level": level,
        "score": score,
        "indicators": indicators,
        "recommendations": recommendations(level),
        "limitations": limitations("url"),
    }
