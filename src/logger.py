import csv
import os
from datetime import datetime, timezone


def _ensure_parent(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def log_ai_decision(path: str, decision: dict, approved: bool, reasons: list[str]) -> None:
    _ensure_parent(path)
    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                [
                    "timestamp",
                    "symbol",
                    "action",
                    "confidence",
                    "max_risk_percent",
                    "qty",
                    "stop_loss",
                    "approved",
                    "reasons",
                ]
            )
        writer.writerow(
            [
                datetime.now(timezone.utc).isoformat(),
                decision.get("symbol"),
                decision.get("action"),
                decision.get("confidence"),
                decision.get("max_risk_percent"),
                decision.get("qty"),
                decision.get("stop_loss"),
                approved,
                " | ".join(reasons) if reasons else "Approved",
            ]
        )


def write_daily_summary(path: str, lines: list[str]) -> None:
    _ensure_parent(path)
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


