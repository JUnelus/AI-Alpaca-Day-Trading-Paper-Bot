from dataclasses import dataclass, field
from datetime import date


@dataclass
class RiskCheckResult:
    approved: bool
    reasons: list[str] = field(default_factory=list)


class RiskManager:
    def __init__(self, min_confidence: float = 0.70, max_risk_percent: float = 1.0) -> None:
        self.min_confidence = min_confidence
        self.max_risk_percent = max_risk_percent

    def evaluate(
        self,
        decision: dict,
        account_equity: float,
        available_cash: float,
        entry_price: float,
        traded_symbols_today: set[str],
        paper_trading: bool,
    ) -> RiskCheckResult:
        reasons: list[str] = []
        symbol = decision.get("symbol", "").upper()
        action = decision.get("action", "hold").lower()
        confidence = float(decision.get("confidence", 0.0))
        qty = float(decision.get("qty", 0))
        stop_loss_value = decision.get("stop_loss")
        numeric_stop_loss: float | None = None
        max_risk_percent = float(decision.get("max_risk_percent", self.max_risk_percent))

        if not paper_trading:
            reasons.append("Rejected: paper trading only.")

        if symbol in traded_symbols_today:
            reasons.append("Rejected: max 1 trade per symbol per day exceeded.")

        if confidence < self.min_confidence:
            reasons.append(f"Rejected: confidence {confidence:.2f} below {self.min_confidence:.2f}.")

        if action not in {"buy", "sell", "hold"}:
            reasons.append("Rejected: invalid action.")

        if action == "hold":
            reasons.append("Rejected: hold signal does not place a trade.")

        if qty <= 0.0:
            reasons.append("Rejected: quantity must be positive.")

        if stop_loss_value is None:
            reasons.append("Rejected: stop loss is required.")
        else:
            try:
                numeric_stop_loss = float(stop_loss_value)
            except (TypeError, ValueError):
                reasons.append("Rejected: stop loss must be numeric.")

        if max_risk_percent > self.max_risk_percent:
            reasons.append(
                f"Rejected: max_risk_percent {max_risk_percent:.2f}% exceeds {self.max_risk_percent:.2f}% policy."
            )

        if action in {"buy", "sell"} and qty > 0 and numeric_stop_loss is not None:
            per_share_risk = abs(entry_price - numeric_stop_loss)
            total_risk = per_share_risk * qty
            allowed_risk = account_equity * (self.max_risk_percent / 100.0)
            if total_risk > allowed_risk:
                reasons.append(
                    f"Rejected: risk ${total_risk:.2f} exceeds ${allowed_risk:.2f} ({self.max_risk_percent:.2f}% of equity)."
                )

        # No margin in first version: position value must fit available cash.
        position_value = entry_price * max(qty, 0)
        if position_value > available_cash:
            reasons.append("Rejected: no margin allowed; insufficient cash.")

        return RiskCheckResult(approved=len(reasons) == 0, reasons=reasons)


def today() -> str:
    return date.today().isoformat()


