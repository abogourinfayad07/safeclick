"""Représentation stable d'un signal détecté."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class Indicator:
    """Un signal explicable, jamais une preuve."""

    code: str
    label: str
    detail: str
    weight: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
