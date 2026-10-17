from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MarketSnapshot:
    symbol: str
    last_price: float
    day_change_percent: float
    source: str = "alpaca"
    timestamp: datetime | None = None
    is_fresh: bool = False
    is_fallback: bool = False


@dataclass
class StrategySignal:
    symbol: str
    action: str
    strength: float
    reason: str


# Broad-market filter for dip buys: a "quality asset on a dip" on a day the whole market gapped
# down is just buying a falling market. Benchmarks are read at entry alongside the watchlist.
BENCHMARK_SYMBOLS: tuple[str, ...] = ("SPY", "QQQ")
MARKET_FILTER_MAX_DROP_PERCENT = -0.3
DIP_BUY_MAX_CHANGE_PERCENT = -0.3  # a dip buy needs the asset down at least this much


@dataclass
class MarketContext:
    """Benchmark day changes at entry; only fresh benchmarks are included."""

    benchmark_changes: dict[str, float] = field(default_factory=dict)
    unavailable: tuple[str, ...] = ()


def build_market_context(snapshots: dict[str, MarketSnapshot], benchmarks: tuple[str, ...] = BENCHMARK_SYMBOLS) -> MarketContext:
    changes: dict[str, float] = {}
    unavailable: list[str] = []
    for symbol in benchmarks:
        snapshot = snapshots.get(symbol)
        if snapshot is None or not snapshot.is_fresh or snapshot.last_price <= 0:
            unavailable.append(symbol)
        else:
            changes[symbol] = snapshot.day_change_percent
    return MarketContext(benchmark_changes=changes, unavailable=tuple(unavailable))


def market_filter_reason(market_context: MarketContext) -> str | None:
    """Return why dip buys are suspended under this market context, or None when they may proceed.

    Fails closed: with no fresh benchmark the filter cannot clear the market, so dip buys wait.
    """
    if not market_context.benchmark_changes:
        missing = ", ".join(market_context.unavailable) or "none requested"
        return f"Market filter: benchmark data unavailable ({missing}); dip buys suspended"
    symbol, change = min(market_context.benchmark_changes.items(), key=lambda item: item[1])
    if change < MARKET_FILTER_MAX_DROP_PERCENT:
        return (f"Market filter: {symbol} {change:+.2f}% at entry is below {MARKET_FILTER_MAX_DROP_PERCENT:+.1f}%; "
                f"dip buy skipped")
    return None


def generate_signal(
    snapshot: MarketSnapshot,
    symbol_cfg: dict | None = None,
    market_context: MarketContext | None = None,
) -> StrategySignal:
    """Momentum + DCA signal structure shared with the paper bot, plus an optional broad-market filter.

    ``market_context`` applies to dip buys only. When it is given and the market filter objects,
    the dip buy becomes a hold carrying the filter's reason. Without a context (the parity gate,
    unit scenarios) the signal is the unfiltered structure both repos share.
    """
    symbol_cfg = symbol_cfg or {}
    quality_score = float(symbol_cfg.get("quality_score", 0.6))
    is_quality = quality_score >= 0.70
    chg = snapshot.day_change_percent
    abs_chg = abs(chg)

    if is_quality and chg <= DIP_BUY_MAX_CHANGE_PERCENT and market_context is not None:
        filter_reason = market_filter_reason(market_context)
        if filter_reason:
            return StrategySignal(symbol=snapshot.symbol, action="hold", strength=0.55, reason=filter_reason)

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
    chg = snapshot.day_change_percent
    abs_chg = abs(chg)

    if abs_chg < 0.4:
        return {
            "predicted_action": "HOLD",
            "predicted_confidence": 0.50,
            "basis": f"Flat session today ({chg:+.2f}%) — no trend to carry forward",
        }

    if abs_chg >= 2.5:
        reversal = "BUY" if chg < 0 else "SELL"
        confidence = round(min(0.78, 0.55 + abs_chg / 20.0), 2)
        direction = "gain" if chg > 0 else "loss"
        return {
            "predicted_action": reversal,
            "predicted_confidence": confidence,
            "basis": f"Extreme {direction} today ({chg:+.2f}%) — mean reversion pullback likely",
        }

    continuation = "BUY" if chg > 0 else "SELL"
    confidence = round(min(0.85, today_signal.strength * 0.88), 2)
    direction = "positive" if chg > 0 else "negative"
    return {
        "predicted_action": continuation,
        "predicted_confidence": confidence,
        "basis": f"Moderate {direction} momentum ({chg:+.2f}%) — continuation expected",
    }

