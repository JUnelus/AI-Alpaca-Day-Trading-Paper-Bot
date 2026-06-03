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


def generate_signal(snapshot: MarketSnapshot, symbol_cfg: dict | None = None) -> StrategySignal:
    """Bias toward DCA buys on pullbacks in high-quality assets; avoid chasing breakouts."""
    symbol_cfg = symbol_cfg or {}
    quality_score = float(symbol_cfg.get("quality_score", 0.6))
    is_quality = quality_score >= 0.70
    chg = snapshot.day_change_percent
    abs_chg = abs(chg)

    if is_quality and chg <= -1.5:
        return StrategySignal(
            symbol=snapshot.symbol,
            action="buy",
            strength=min(1.0, 0.72 + abs_chg / 8.0 + max(0.0, quality_score - 0.7) * 0.2),
            reason="DCA buy: quality asset on a deep pullback",
        )

    if is_quality and -1.5 < chg <= -0.3:
        return StrategySignal(
            symbol=snapshot.symbol,
            action="buy",
            strength=min(0.85, 0.65 + abs_chg / 6.0 + max(0.0, quality_score - 0.7) * 0.15),
            reason="DCA buy: quality asset on a mild dip",
        )

    if chg >= 4.0:
        return StrategySignal(
            symbol=snapshot.symbol,
            action="sell",
            strength=min(1.0, 0.70 + chg / 10.0),
            reason="Take-profit trim after overextended rally",
        )

    if not is_quality and chg <= -3.0:
        return StrategySignal(
            symbol=snapshot.symbol,
            action="sell",
            strength=min(0.95, 0.68 + abs_chg / 10.0),
            reason="Risk reduction: weak asset in breakdown",
        )

    return StrategySignal(
        symbol=snapshot.symbol,
        action="hold",
        strength=0.55,
        reason="Wait for better value entry",
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


