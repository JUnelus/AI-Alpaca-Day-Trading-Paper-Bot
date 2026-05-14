"""Entry point: run the full AI day-trading pipeline for every watchlist symbol."""
from __future__ import annotations

import csv
import json
import os
from dataclasses import asdict
from datetime import date, datetime, timezone
from typing import Dict, Set

from dotenv import load_dotenv

from .ai_agent import build_decision
from .alpaca_client import AlpacaClient
from .dashboard import generate_dashboard, update_readme
from .logger import log_ai_decision, write_daily_summary
from .market_data import get_market_snapshots
from .portfolio import PortfolioState, STATE_FILE, refresh_from_alpaca
from .risk_manager import RiskManager
from .strategy import generate_signal

# ── paths ──────────────────────────────────────────────────────────────────────
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WATCHLIST_PATH = os.path.join(_ROOT, "config", "watchlist.json")
LOG_PATH = os.path.join(_ROOT, "data", "trade_log.csv")
SUMMARY_PATH = os.path.join(_ROOT, "reports", "daily_summary.md")


# ── helpers ────────────────────────────────────────────────────────────────────

_CRYPTO_NORMALIZE: Dict[str, str] = {
    "BTCUSD": "BTC/USD",
    "ETHUSD": "ETH/USD",
    "SOLUSD": "SOL/USD",
}


def _normalize_sym(symbol: str) -> str:
    return _CRYPTO_NORMALIZE.get(symbol.upper(), symbol)


def _load_watchlist() -> dict:
    with open(WATCHLIST_PATH, encoding="utf-8") as f:
        return json.load(f)


def _traded_symbols_today() -> Set[str]:
    """Return symbols that already have an APPROVED trade in today's log."""
    if not os.path.exists(LOG_PATH):
        return set()
    today_str = date.today().isoformat()
    traded: Set[str] = set()
    try:
        with open(LOG_PATH, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = row.get("timestamp", "")
                if ts.startswith(today_str) and row.get("approved") == "True":
                    traded.add(row.get("symbol", "").upper())
    except Exception:
        pass
    return traded


def _calc_qty(price: float, asset_type: str, max_position_value: float) -> float:
    """Compute share/unit quantity based on max position value."""
    if price <= 0:
        return 1.0
    if asset_type == "crypto":
        # Fractional crypto up to 4 decimal places
        return max(0.0001, round(max_position_value / price, 4))
    # Whole shares for stocks / ETFs
    return max(1.0, float(int(max_position_value / price)))


# ── main ───────────────────────────────────────────────────────────────────────

def run_once() -> dict:
    load_dotenv()

    config = _load_watchlist()
    symbols: list[dict] = config["symbols"]
    min_confidence = float(os.getenv("MIN_CONFIDENCE", str(config.get("min_confidence", 0.70))))
    max_risk_pct = float(os.getenv("MAX_RISK_PERCENT", "1"))
    max_pos_pct = config.get("max_position_pct", 15) / 100.0
    min_buying_power_to_trade = float(
        os.getenv("MIN_BUYING_POWER_TO_TRADE", str(config.get("min_buying_power_to_trade", 100.0)))
    )
    allow_shorts = str(os.getenv("ALLOW_SHORTS", str(config.get("allow_shorts", False)))).lower() in {"1", "true", "yes"}

    previous_state = PortfolioState.load()

    alpaca = AlpacaClient()
    account = alpaca.get_account_snapshot()

    # Use the configured $10k portfolio budget — not the raw Alpaca paper balance —
    # so position sizing stays within our intended allocation.
    portfolio_budget = float(config.get("portfolio_size", 10_000))
    max_pos_value = portfolio_budget * max_pos_pct

    # Fetch current positions: map symbol → qty (positive = long, negative = short).
    held_qty_map: Dict[str, float] = {}
    if alpaca.is_ready:
        for pos in alpaca.list_positions():
            sym_raw = getattr(pos, "symbol", "")
            held_qty_map[_normalize_sym(sym_raw)] = float(getattr(pos, "qty", 0))

    traded_today = _traded_symbols_today()
    risk_manager = RiskManager(min_confidence=min_confidence, max_risk_percent=max_risk_pct)

    # Fetch real-time prices for all symbols in one go
    snapshots = get_market_snapshots(symbols)

    results = []
    signal_map: Dict[str, dict] = {}
    # Use broker's actual buying_power (not gross cash) so the risk manager
    # rejects orders the broker would deny. Cap at portfolio_budget ($10k).
    available_cash = min(account.buying_power, portfolio_budget)
    trading_paused_reason = ""
    if available_cash < min_buying_power_to_trade:
        trading_paused_reason = (
            f"Insufficient buying power (${available_cash:.2f}) below minimum "
            f"${min_buying_power_to_trade:.2f}; skipping order placement."
        )

    for sym_cfg in symbols:
        sym = sym_cfg["symbol"]
        asset_type = sym_cfg["type"]
        snapshot = snapshots.get(sym)
        if not snapshot:
            continue

        if trading_paused_reason:
            signal_map[sym] = {
                "action": "hold",
                "confidence": 0.0,
                "last_price": snapshot.last_price,
                "day_change_percent": snapshot.day_change_percent,
            }
            results.append(
                {
                    "symbol": sym,
                    "decision": {"action": "hold", "confidence": 0.0},
                    "risk": {"approved": False, "reasons": [trading_paused_reason]},
                    "order_result": None,
                }
            )
            continue

        signal = generate_signal(snapshot)

        # Gate SELL signals based on long-only mode and current held position.
        if signal.action == "sell":
            held_qty = held_qty_map.get(sym, 0.0)
            if held_qty == 0.0:
                # No position at all — nothing to sell or short
                rejection_reason = "No position to sell."
                signal_map[sym] = {"action": "hold", "confidence": signal.strength, "last_price": snapshot.last_price, "day_change_percent": snapshot.day_change_percent}
                results.append({"symbol": sym, "decision": {"action": "hold"}, "risk": {"approved": False, "reasons": [rejection_reason]}, "order_result": None})
                continue
            if not allow_shorts and held_qty < 0:
                # Long-only mode: already short, don't deepen the short
                rejection_reason = "Long-only mode: cannot add to an existing short position."
                signal_map[sym] = {"action": "hold", "confidence": signal.strength, "last_price": snapshot.last_price, "day_change_percent": snapshot.day_change_percent}
                results.append({"symbol": sym, "decision": {"action": "hold"}, "risk": {"approved": False, "reasons": [rejection_reason]}, "order_result": None})
                continue
            if not allow_shorts and held_qty == 0.0:
                # Long-only mode: no position, sell would open a new short — block it
                rejection_reason = "Long-only mode: SELL blocked — would open a new short position."
                signal_map[sym] = {"action": "hold", "confidence": signal.strength, "last_price": snapshot.last_price, "day_change_percent": snapshot.day_change_percent}
                results.append({"symbol": sym, "decision": {"action": "hold"}, "risk": {"approved": False, "reasons": [rejection_reason]}, "order_result": None})
                continue
            # held_qty > 0 → long position exists; allow sell-to-close

        qty = _calc_qty(snapshot.last_price, asset_type, max_pos_value)
        decision = build_decision(signal, last_price=snapshot.last_price, default_qty=qty).to_dict()

        risk = risk_manager.evaluate(
            decision=decision,
            account_equity=account.equity,
            available_cash=available_cash,
            entry_price=snapshot.last_price,
            traded_symbols_today=traded_today,
            paper_trading=alpaca.paper,
        )

        log_ai_decision(LOG_PATH, decision, risk.approved, risk.reasons)

        order_result = None
        if risk.approved:
            order_result = alpaca.place_paper_trade(
                symbol=sym,
                qty=qty,
                side=decision["action"],
            )
            traded_today.add(sym.upper())
            # Deduct estimated cost from tracked cash for subsequent risk checks
            available_cash = max(0.0, available_cash - snapshot.last_price * qty)

        signal_map[sym] = {
            "action": decision["action"],
            "confidence": decision["confidence"],
            "last_price": snapshot.last_price,
            "day_change_percent": snapshot.day_change_percent,
        }

        results.append(
            {
                "symbol": sym,
                "decision": decision,
                "risk": {"approved": risk.approved, "reasons": risk.reasons},
                "order_result": str(order_result) if order_result else None,
            }
        )

    trades_today_count = sum(
        1 for r in results
        if r["risk"]["approved"]
        and r.get("order_result")
        and "error" not in str(r.get("order_result", ""))
        and "skipped" not in str(r.get("order_result", ""))
    )

    # ── portfolio state ────────────────────────────────────────────────────────
    symbol_type_map = {s["symbol"]: s["type"] for s in symbols}
    price_map = {sym: snap.last_price for sym, snap in snapshots.items()}

    if alpaca.is_ready:
        state = refresh_from_alpaca(alpaca, symbol_type_map, price_map, trades_today_count)
    else:
        state = PortfolioState.load()
        state.trades_today = trades_today_count
        state.buying_power = account.buying_power
        state.last_updated = datetime.now(timezone.utc).isoformat()

    today = date.today()
    previous_date = None
    if previous_state.last_updated:
        try:
            previous_date = datetime.fromisoformat(previous_state.last_updated).date()
        except ValueError:
            previous_date = None

    if previous_date is not None and previous_date < today:
        state.yesterday_total_pnl = previous_state.total_pnl
        state.yesterday_equity = previous_state.account_equity
    else:
        state.yesterday_total_pnl = previous_state.yesterday_total_pnl
        state.yesterday_equity = previous_state.yesterday_equity

    state.save()

    # ── update README dashboard ────────────────────────────────────────────────
    dashboard_md = generate_dashboard(state, symbols, signal_map, results)
    update_readme(dashboard_md)

    # ── daily summary report ───────────────────────────────────────────────────
    lines = [
        f"# Daily Summary — {date.today().isoformat()}",
        "",
        "## 💰 Portfolio",
        f"- Equity: ${state.account_equity:,.2f}",
        f"- Cash:   ${state.cash:,.2f}",
        f"- Buying power: ${state.buying_power:,.2f}",
        f"- P&L:    ${state.total_pnl:+,.2f} ({state.total_pnl_pct:+.2f}%)",
        f"- Trades executed today: {trades_today_count}",
        "",
        "## 🤖 AI Decisions",
    ]
    for r in results:
        approved = r["risk"]["approved"]
        status = "✅ APPROVED" if approved else "❌ REJECTED"
        reason = "; ".join(r["risk"]["reasons"]) if not approved else "Passed all risk checks"
        lines.append(
            f"- **{r['symbol']}** — {r['decision'].get('action', '?').upper()} "
            f"(conf={r['decision'].get('confidence', 0):.2f}) → {status}: {reason}"
        )
    write_daily_summary(SUMMARY_PATH, lines)

    return {"results": results, "portfolio": asdict(state)}


if __name__ == "__main__":
    result = run_once()
    print(json.dumps(result, indent=2, default=str))
