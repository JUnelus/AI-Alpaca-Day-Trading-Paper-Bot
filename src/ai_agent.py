from __future__ import annotations

from dataclasses import asdict, dataclass

from .strategy import StrategySignal


@dataclass
class AIDecision:
    symbol: str
    action: str
    confidence: float
    reason: str
    max_risk_percent: float
    qty: float
    stop_loss: float

    def to_dict(self) -> dict:
        return asdict(self)


# Protective stop distance from entry. 1% sat inside the normal intraday range of the mega-cap
# names and converted ordinary noise into realized losses; 2% is paired with a halved DCA budget
# so the dollar risk per position is unchanged.
STOP_LOSS_PERCENT = 2.0


def build_decision(signal: StrategySignal, last_price: float, default_qty: float = 1.0) -> AIDecision:
    confidence = max(0.0, min(1.0, signal.strength))

    if signal.action == "buy":
        stop_loss = round(last_price * (1.0 - STOP_LOSS_PERCENT / 100.0), 2)
    elif signal.action == "sell":
        stop_loss = round(last_price * (1.0 + STOP_LOSS_PERCENT / 100.0), 2)
    else:
        stop_loss = round(last_price, 2)

    return AIDecision(
        symbol=signal.symbol,
        action=signal.action,
        confidence=confidence,
        reason=signal.reason,
        max_risk_percent=1.0,
        qty=max(0.0001, float(default_qty)),
        stop_loss=stop_loss,
    )

