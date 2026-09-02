from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from typing import Optional, Union

from .execution_models import ExecutionResult
from .time_utils import ensure_aware, iso_to_trading_day


def _ensure_parent(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _execution_dict(execution_result: Optional[Union[ExecutionResult, dict]]) -> dict:
    if execution_result is None:
        return {}
    if isinstance(execution_result, ExecutionResult):
        return execution_result.to_dict()
    return dict(execution_result)


def log_ai_decision(
    path: str,
    decision: dict,
    approved: bool,
    reasons: list[str],
    notes: Optional[list[str]] = None,
    execution_result: Optional[Union[ExecutionResult, dict]] = None,
    now: Optional[datetime] = None,
) -> None:
    _ensure_parent(path)
    execution = _execution_dict(execution_result)
    timestamp = ensure_aware(now or datetime.now(timezone.utc)).isoformat()
    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                timestamp,
                decision.get("symbol"),
                decision.get("action"),
                decision.get("confidence"),
                decision.get("max_risk_percent"),
                decision.get("qty"),
                decision.get("stop_loss"),
                approved,
                " | ".join(reasons) if reasons else "Approved",
                " | ".join(notes or []),
                execution.get("counts_as_trade", False),
                execution.get("entry_order_id"),
                execution.get("protective_order_id"),
                execution.get("filled_qty"),
                execution.get("filled_avg_price"),
                execution.get("protection_active", False),
                execution.get("protection_failed", False),
                execution.get("status"),
                execution.get("message"),
            ]
        )


def load_trade_activity(path: str, trading_day_value: str) -> tuple[int, set[str]]:
    if not os.path.exists(path):
        return 0, set()

    trade_count = 0
    traded_symbols: set[str] = set()
    with open(path, encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            timestamp = row[0]
            if timestamp == "timestamp":
                continue
            row_day = iso_to_trading_day(timestamp) or timestamp[:10]
            if row_day != trading_day_value:
                continue

            action = row[2].strip().lower() if len(row) > 2 else ""
            approved = row[7].strip().lower() == "true" if len(row) > 7 else False
            if len(row) > 10:
                counted = row[10].strip().lower() == "true"
            else:
                counted = approved and action in {"buy", "sell"}

            if counted:
                trade_count += 1
                if len(row) > 1 and row[1]:
                    traded_symbols.add(row[1].strip().upper())

    return trade_count, traded_symbols


def write_daily_summary(path: str, lines: list[str]) -> None:
    _ensure_parent(path)
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


