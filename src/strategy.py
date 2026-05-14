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


def predict_next_day(snapshot: MarketSnapshot, today_signal: StrategySignal) -> dict:
    """
    Predict the likely next trading session action based on today's price momentum.

    Three tiers:
      - Flat day (<0.4% move)      → Hold expected (no trend to continue)
      - Moderate move (0.4–2.5%)   → Momentum continuation (same direction)
      - Extreme move (>2.5%)       → Mean reversion likely (opposite direction)

    Returns a dict with predicted_action, predicted_confidence, and basis note.
    """
    chg = snapshot.day_change_percent
    abs_chg = abs(chg)

    if abs_chg < 0.4:
        return {
            "predicted_action": "HOLD",
            "predicted_confidence": 0.50,
            "basis": f"Flat session today ({chg:+.2f}%) — no trend to carry forward",
        }

    if abs_chg >= 2.5:
        # Overextended move — mean reversion pull likely
        reversal = "BUY" if chg < 0 else "SELL"
        confidence = round(min(0.78, 0.55 + abs_chg / 20.0), 2)
        direction = "gain" if chg > 0 else "loss"
        return {
            "predicted_action": reversal,
            "predicted_confidence": confidence,
            "basis": f"Extreme {direction} today ({chg:+.2f}%) — mean reversion pullback likely",
        }

    # Moderate momentum → continuation
    continuation = "BUY" if chg > 0 else "SELL"
    confidence = round(min(0.85, today_signal.strength * 0.88), 2)
    direction = "positive" if chg > 0 else "negative"
    return {
        "predicted_action": continuation,
        "predicted_confidence": confidence,
        "basis": f"Moderate {direction} momentum ({chg:+.2f}%) — continuation expected",
    }


