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


def build_decision(signal: StrategySignal, last_price: float, default_qty: float = 1.0) -> AIDecision:
    confidence = max(0.0, min(1.0, signal.strength))

    # Require stop loss in all non-hold decisions.
    if signal.action == "buy":
        stop_loss = round(last_price * 0.99, 2)
    elif signal.action == "sell":
        stop_loss = round(last_price * 1.01, 2)
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
