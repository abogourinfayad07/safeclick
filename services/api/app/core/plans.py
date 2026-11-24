"""Source unique des offres lue depuis `packages/shared/plans.json`."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

PLANS_PATH = Path(__file__).resolve().parents[4] / "packages" / "shared" / "plans.json"


@lru_cache(maxsize=1)
def plans_catalog() -> dict[str, object]:
    payload = json.loads(PLANS_PATH.read_text(encoding="utf-8"))
    if len(payload["plans"]) != 3:
        raise ValueError("Le catalogue doit contenir exactement trois offres.")
    return payload


def plan_by_code(code: str) -> dict[str, object] | None:
    for plan in plans_catalog()["plans"]:
        if plan["code"] == code:
            return plan
    return None


def daily_limit_for_plan(code: str) -> int:
    plan = plan_by_code(code)
    if plan is None:
        raise ValueError(f"Offre inconnue : {code}")
    return int(plan["dailyAnalyses"])
