from dataclasses import dataclass


@dataclass
class MarketSnapshot:
    symbol: str
    last_price: float
    day_change_percent: float


@dataclass
class StrategySignal:
    symbol: str
    action: str
    strength: float
    reason: str


def generate_signal(snapshot: MarketSnapshot) -> StrategySignal:
    # Simple momentum rule for a first paper-trading iteration.
    if snapshot.day_change_percent >= 0.4:
        return StrategySignal(
            symbol=snapshot.symbol,
            action="buy",
            strength=min(1.0, 0.6 + snapshot.day_change_percent / 5.0),
            reason="Positive momentum detected",
        )
    if snapshot.day_change_percent <= -0.4:
        return StrategySignal(
            symbol=snapshot.symbol,
            action="sell",
            strength=min(1.0, 0.6 + abs(snapshot.day_change_percent) / 5.0),
            reason="Negative momentum detected",
        )

    return StrategySignal(
        symbol=snapshot.symbol,
        action="hold",
        strength=0.5,
        reason="No strong trend signal",
    )

