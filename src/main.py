"""Entry point: run the full AI day-trading pipeline for every watchlist symbol."""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict
from datetime import date, datetime, timezone
from typing import Dict, Optional

from dotenv import load_dotenv

from .ai_agent import build_decision
from .alpaca_client import AlpacaClient
from .dashboard import README_PATH, generate_dashboard, update_readme
from .email_reporter import send_daily_report
from .execution_models import ExecutionResult
from .logger import load_trade_activity, log_ai_decision, write_daily_summary
from .market_data import MarketDataResult, get_market_snapshots
from .portfolio import PortfolioState, STATE_FILE, refresh_from_alpaca
from .risk_manager import RiskConfig, RiskEvaluationContext, RiskManager, normalize_qty_for_asset
from .strategy import MarketSnapshot, generate_signal, predict_next_day
from .time_utils import ensure_aware, iso_to_trading_day, trading_day
from .watchlist_manager import refresh_weekly_watchlist

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


def _load_watchlist(watchlist_path: str = WATCHLIST_PATH) -> dict:
    with open(watchlist_path, encoding="utf-8") as f:
        return json.load(f)


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _calc_qty(price: float, asset_type: str, max_position_value: float) -> float:
    """Compute share/unit quantity based on max position value."""
    if price <= 0:
        return 0.0

    qty = normalize_qty_for_asset(asset_type, max_position_value / price)
    if asset_type == "crypto":
        return qty if qty >= 0.0001 else 0.0
    return qty


def apply_execution_to_available_cash(
    available_cash: float,
    execution_result: ExecutionResult,
    reference_price: float,
) -> float:
    if not execution_result.counts_as_trade:
        return available_cash

    unit_price = execution_result.filled_avg_price or reference_price
    if execution_result.side == "buy":
        effective_qty = execution_result.filled_qty if execution_result.filled_qty > 0 else execution_result.requested_qty
        return max(0.0, available_cash - unit_price * effective_qty)

    if execution_result.side == "sell" and execution_result.filled_qty > 0:
        return available_cash + unit_price * execution_result.filled_qty

    return available_cash


def _apply_execution_to_position_state(
    symbol: str,
    execution_result: ExecutionResult,
    reference_price: float,
    held_qty_map: Dict[str, float],
    position_value_map: Dict[str, float],
    current_gross_exposure: float,
) -> float:
    if not execution_result.counts_as_trade:
        return current_gross_exposure

    tracked_value = position_value_map.get(symbol, 0.0)
    tracked_qty = held_qty_map.get(symbol, 0.0)

    if execution_result.side == "buy":
        effective_qty = execution_result.filled_qty if execution_result.filled_qty > 0 else execution_result.requested_qty
        value_delta = reference_price * effective_qty
        held_qty_map[symbol] = tracked_qty + effective_qty
        position_value_map[symbol] = tracked_value + value_delta
        return current_gross_exposure + value_delta

    if execution_result.side == "sell" and execution_result.filled_qty > 0:
        effective_qty = min(max(0.0, tracked_qty), execution_result.filled_qty)
        value_delta = min(tracked_value, reference_price * effective_qty)
        held_qty_map[symbol] = max(0.0, tracked_qty - effective_qty)
        position_value_map[symbol] = max(0.0, tracked_value - value_delta)
        return max(0.0, current_gross_exposure - value_delta)

    return current_gross_exposure


def _extract_position_state(alpaca: AlpacaClient) -> tuple[Dict[str, float], Dict[str, float], float]:
    held_qty_map: Dict[str, float] = {}
    position_value_map: Dict[str, float] = {}
    gross_exposure = 0.0

    if not alpaca.is_ready:
        return held_qty_map, position_value_map, gross_exposure

    for pos in alpaca.list_positions():
        sym = _normalize_sym(getattr(pos, "symbol", ""))
        qty = _safe_float(getattr(pos, "qty", 0.0))
        raw_market_value = getattr(pos, "market_value", None)
        market_value = abs(_safe_float(raw_market_value, _safe_float(getattr(pos, "current_price", 0.0)) * abs(qty)))
        held_qty_map[sym] = qty
        position_value_map[sym] = market_value
        gross_exposure += market_value

    return held_qty_map, position_value_map, gross_exposure


def _current_state_day(previous_state: PortfolioState) -> Optional[str]:
    if previous_state.trading_day:
        return previous_state.trading_day
    if previous_state.last_updated:
        return iso_to_trading_day(previous_state.last_updated)
    return None


def _build_daily_loss_state(
    previous_state: PortfolioState,
    current_equity: float,
    trading_day_value: str,
    risk_config: RiskConfig,
) -> tuple[float, float, float, bool]:
    previous_day = _current_state_day(previous_state)
    same_day = previous_day == trading_day_value
    start_of_day_equity = (
        previous_state.start_of_day_equity
        if same_day and previous_state.start_of_day_equity is not None
        else current_equity
    )
    daily_pnl = current_equity - start_of_day_equity
    daily_loss_limit = risk_config.portfolio_size * (risk_config.max_daily_loss_percent / 100.0)
    daily_loss_triggered = daily_pnl <= -daily_loss_limit
    return start_of_day_equity, daily_pnl, daily_loss_limit, daily_loss_triggered


def _build_safety_warnings(
    state: PortfolioState,
    risk_config: RiskConfig,
    market_data_result: MarketDataResult,
    mode: str,
    daily_pnl: float,
    daily_loss_limit: float,
) -> list[str]:
    warnings: list[str] = []
    max_position_value = risk_config.portfolio_size * (risk_config.max_position_percent / 100.0)
    max_total_exposure = risk_config.portfolio_size * (risk_config.max_total_exposure_percent / 100.0)

    if state.gross_exposure > max_total_exposure + 1e-9:
        warnings.append(
            f"Current gross exposure ${state.gross_exposure:.2f} exceeds the configured limit of ${max_total_exposure:.2f}. New BUY orders are blocked until exposure is reduced."
        )

    for pos in state.positions:
        if abs(pos.market_value) > max_position_value + 1e-9:
            warnings.append(
                f"Existing {pos.symbol} position value ${abs(pos.market_value):.2f} exceeds the configured per-position limit of ${max_position_value:.2f}."
            )

    if mode == "trade" and not market_data_result.service_available:
        warnings.append("Trading skipped because fresh market data was unavailable.")

    stale_symbols = [snapshot.symbol for snapshot in market_data_result.snapshots.values() if not snapshot.is_fresh]
    if mode == "trade" and stale_symbols:
        warnings.append(
            f"Fresh market data was unavailable for: {', '.join(sorted(stale_symbols))}. Those symbols were not traded."
        )

    if state.daily_loss_triggered:
        circuit_breaker_message = (
            f"Daily loss circuit breaker triggered: Start-of-day equity: ${state.start_of_day_equity:.2f}; "
            f"Current equity: ${state.account_equity:.2f}; Daily P&L: ${daily_pnl:.2f}; Limit: -${daily_loss_limit:.2f}."
        )
        warnings.append(circuit_breaker_message)
        print(circuit_breaker_message)

    if market_data_result.message:
        warnings.append(market_data_result.message)

    deduped: list[str] = []
    for warning in warnings:
        if warning not in deduped:
            deduped.append(warning)
    return deduped


# ── main ───────────────────────────────────────────────────────────────────────

def run_once(
    mode: str = "report",
    allow_fallback_data: bool = False,
    watchlist_path: str = WATCHLIST_PATH,
    log_path: str = LOG_PATH,
    summary_path: str = SUMMARY_PATH,
    readme_path: str = README_PATH,
    state_path: str = STATE_FILE,
    now: Optional[datetime] = None,
    alpaca_client: Optional[object] = None,
) -> dict:
    load_dotenv()
    if mode not in {"trade", "report"}:
        raise ValueError("mode must be 'trade' or 'report'.")

    run_time = ensure_aware(now or datetime.now(timezone.utc))
    trading_day_value = trading_day(run_time)
    email_required = str(os.getenv("EMAIL_REQUIRED", "false")).lower() in {"1", "true", "yes"}

    # Refresh once per ISO week so the active 10-symbol basket stays market-value ranked.
    refresh_weekly_watchlist(watchlist_path, limit=10)

    config = _load_watchlist(watchlist_path)
    symbols: list[dict] = config["symbols"]
    risk_config = RiskConfig.from_sources(config)

    previous_state = PortfolioState.load(state_path)

    alpaca = alpaca_client or AlpacaClient()
    account = alpaca.get_account_snapshot()
    held_qty_map, position_value_map, current_gross_exposure = _extract_position_state(alpaca)
    trades_today_count, traded_today = load_trade_activity(log_path, trading_day_value)
    start_of_day_equity, daily_pnl, daily_loss_limit, daily_loss_triggered = _build_daily_loss_state(
        previous_state,
        account.equity,
        trading_day_value,
        risk_config,
    )
    risk_manager = RiskManager(config=risk_config)

    # Fetch validated current prices for all symbols in one go.
    market_data_result = get_market_snapshots(
        symbols,
        allow_fallback_data=allow_fallback_data,
        now=run_time,
    )
    snapshots = market_data_result.snapshots

    results = []
    signal_map: Dict[str, dict] = {}
    estimated_available_cash = max(0.0, account.cash)
    max_position_value = risk_config.portfolio_size * (risk_config.max_position_percent / 100.0)

    for sym_cfg in symbols:
        sym = sym_cfg["symbol"]
        asset_type = sym_cfg["type"]
        snapshot = snapshots.get(sym) or MarketSnapshot(symbol=sym, last_price=0.0, day_change_percent=0.0, source="unavailable")

        signal = generate_signal(snapshot, sym_cfg)

        dca_position_value = max_position_value
        if signal.action == "buy" and "dca buy" in signal.reason.lower():
            # Stage into positions gradually to lower average cost over time.
            dca_position_value = max_position_value * 0.35

        qty = _calc_qty(snapshot.last_price, asset_type, dca_position_value)
        decision = build_decision(signal, last_price=snapshot.last_price, default_qty=qty).to_dict()
        decision["requested_qty"] = decision.get("qty", qty)

        risk_context = RiskEvaluationContext(
            mode=mode,
            asset_type=asset_type,
            entry_price=snapshot.last_price,
            account_equity=account.equity,
            actual_available_cash=estimated_available_cash,
            remaining_portfolio_capacity=max(0.0, risk_config.portfolio_size - current_gross_exposure),
            current_position_qty=held_qty_map.get(sym, 0.0),
            current_position_market_value=position_value_map.get(sym, 0.0),
            current_gross_exposure=current_gross_exposure,
            traded_symbols_today=traded_today,
            daily_trade_count=trades_today_count,
            paper_trading=alpaca.paper,
            market_data_is_fresh=snapshot.is_fresh,
            market_data_source=snapshot.source,
            market_data_service_available=market_data_result.service_available,
            daily_loss_triggered=daily_loss_triggered,
            protective_stop_supported=alpaca.can_place_protected_buy(asset_type),
        )
        risk = risk_manager.evaluate(decision=decision, context=risk_context)

        if risk.approved:
            decision["qty"] = risk.adjusted_qty

        order_result: Optional[ExecutionResult] = None
        if risk.approved:
            order_result = alpaca.place_paper_trade(
                symbol=sym,
                qty=risk.adjusted_qty,
                side=decision["action"],
                asset_type=asset_type,
                mode=mode,
                stop_loss=decision.get("stop_loss"),
            )
            if order_result.counts_as_trade:
                trades_today_count += 1
                traded_today.add(sym.upper())
                estimated_available_cash = apply_execution_to_available_cash(
                    estimated_available_cash,
                    order_result,
                    snapshot.last_price,
                )
                current_gross_exposure = _apply_execution_to_position_state(
                    sym,
                    order_result,
                    snapshot.last_price,
                    held_qty_map,
                    position_value_map,
                    current_gross_exposure,
                )

        log_ai_decision(log_path, decision, risk.approved, risk.reasons, risk.notes, order_result)

        signal_map[sym] = {
            "action": decision["action"],
            "confidence": decision["confidence"],
            "last_price": snapshot.last_price,
            "day_change_percent": snapshot.day_change_percent,
            "prediction": predict_next_day(snapshot, signal),
            "source": snapshot.source,
            "is_fresh": snapshot.is_fresh,
        }

        results.append(
            {
                "symbol": sym,
                "decision": decision,
                "risk": {
                    "approved": risk.approved,
                    "reasons": risk.reasons,
                    "notes": risk.notes,
                    "adjusted_qty": risk.adjusted_qty,
                    "requested_qty": risk.requested_qty,
                },
                "order_result": order_result.to_dict() if order_result else None,
                "market_data": {
                    "source": snapshot.source,
                    "timestamp": snapshot.timestamp.isoformat() if snapshot.timestamp else None,
                    "is_fresh": snapshot.is_fresh,
                    "is_fallback": snapshot.is_fallback,
                },
            }
        )

    # ── portfolio state ────────────────────────────────────────────────────────
    symbol_type_map = {s["symbol"]: s["type"] for s in symbols}
    price_map = {sym: snap.last_price for sym, snap in snapshots.items()}

    if alpaca.is_ready:
        state = refresh_from_alpaca(
            alpaca,
            symbol_type_map,
            price_map,
            starting_balance=risk_config.portfolio_size,
            trades_today=trades_today_count,
        )
    else:
        state = PortfolioState.load(state_path)
        state.starting_balance = risk_config.portfolio_size
        state.account_equity = account.equity
        state.cash = account.cash
        state.trades_today = trades_today_count
        state.buying_power = account.buying_power
        state.gross_exposure = current_gross_exposure
        state.last_updated = run_time.isoformat()

    previous_day = _current_state_day(previous_state)
    if previous_day is not None and previous_day < trading_day_value:
        state.yesterday_total_pnl = previous_state.total_pnl
        state.yesterday_equity = previous_state.account_equity
    else:
        state.yesterday_total_pnl = previous_state.yesterday_total_pnl
        state.yesterday_equity = previous_state.yesterday_equity

    state.trading_day = trading_day_value
    state.traded_symbols_today = sorted(traded_today)
    state.start_of_day_equity = start_of_day_equity
    state.daily_pnl = daily_pnl
    state.daily_loss_limit = daily_loss_limit
    state.daily_loss_triggered = daily_loss_triggered
    state.max_total_exposure = risk_config.portfolio_size * (risk_config.max_total_exposure_percent / 100.0)
    state.mode = mode
    state.warnings = _build_safety_warnings(
        state,
        risk_config,
        market_data_result,
        mode,
        daily_pnl,
        daily_loss_limit,
    )

    state.save(state_path)

    # ── update README dashboard ────────────────────────────────────────────────
    dashboard_md = generate_dashboard(state, symbols, signal_map, results)
    update_readme(dashboard_md, readme_path=readme_path)

    # ── daily summary report ───────────────────────────────────────────────────
    lines = [
        f"# Daily Summary — {date.fromisoformat(trading_day_value).isoformat()}",
        "",
        f"- Run mode: `{mode}`",
        "## 💰 Portfolio",
        f"- Equity: ${state.account_equity:,.2f}",
        f"- Cash:   ${state.cash:,.2f}",
        f"- Buying power: ${state.buying_power:,.2f}",
        f"- P&L:    ${state.total_pnl:+,.2f} ({state.total_pnl_pct:+.2f}%)",
        f"- Trades executed today: {trades_today_count}",
        "",
        "## ⚠️ Safety Status",
    ]
    if state.warnings:
        lines.extend(f"- {warning}" for warning in state.warnings)
    else:
        lines.append("- No active safety warnings.")

    lines += [
        "",
        "## 🤖 AI Decisions",
    ]
    for r in results:
        order_result = r.get("order_result") or {}
        if order_result.get("protection_failed"):
            status = "⚠️ PROTECTION FAILED"
            reason = order_result.get("message", "Protective stop placement failed.")
        elif order_result.get("counts_as_trade"):
            status = "✅ EXECUTED"
            reason = order_result.get("message", "Broker accepted the order.")
        elif r["risk"]["approved"]:
            status = "⏭️ NOT EXECUTED"
            reason = order_result.get("message", "Order was approved but not sent to the broker.")
        else:
            status = "❌ REJECTED"
            reason = "; ".join(r["risk"]["reasons"])
        lines.append(
            f"- **{r['symbol']}** — {r['decision'].get('action', '?').upper()} "
            f"(conf={r['decision'].get('confidence', 0):.2f}) → {status}: {reason}"
        )
    write_daily_summary(summary_path, lines)

    # ── send daily report via email ────────────────────────────────────────────────
    executed_trades = [
        {
            "symbol": r["symbol"],
            "action": r["decision"].get("action", "?"),
            "confidence": r["decision"].get("confidence", 0),
            "reason": r["decision"].get("reason", "—"),
            "filled_qty": (r.get("order_result") or {}).get("filled_qty", 0),
            "stop_price": (r.get("order_result") or {}).get("stop_price"),
            "protected": (r.get("order_result") or {}).get("protection_active", False),
            "status": (r.get("order_result") or {}).get("status"),
        }
        for r in results
        if (r.get("order_result") or {}).get("counts_as_trade")
    ]
    
    open_positions = [
        {
            "symbol": pos.symbol,
            "asset_type": pos.asset_type,
            "qty": pos.qty,
            "avg_cost": pos.avg_entry_price,
            "price": pos.current_price,
            "mkt_value": pos.market_value,
            "unrealized_pnl": pos.unrealized_pnl,
            "pnl_pct": pos.unrealized_pnl_pct * 100,
        }
        for pos in state.positions
    ]
    
    predictions_data = [
        {
            "symbol": sym_cfg["symbol"],
            "name": sym_cfg.get("name", "?"),
            "action": signal_map.get(sym_cfg["symbol"], {}).get("prediction", {}).get("predicted_action", "HOLD"),
            "confidence": int(signal_map.get(sym_cfg["symbol"], {}).get("prediction", {}).get("predicted_confidence", 0.5) * 100),
            "basis": signal_map.get(sym_cfg["symbol"], {}).get("prediction", {}).get("basis", "—"),
        }
        for sym_cfg in symbols
    ]
    
    email_sent = send_daily_report(state, executed_trades, open_positions, predictions_data)
    if email_required and not email_sent:
        raise RuntimeError("EMAIL_REQUIRED=true but daily report email was not sent.")

    return {
        "mode": mode,
        "results": results,
        "portfolio": asdict(state),
        "market_data": {
            "service_available": market_data_result.service_available,
            "used_fallback_data": market_data_result.used_fallback_data,
            "message": market_data_result.message,
        },
    }


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Alpaca paper-trading bot in a safe explicit mode.")
    parser.add_argument(
        "--mode",
        choices=("trade", "report"),
        default="report",
        help="trade places broker orders; report updates portfolio/reporting only.",
    )
    parser.add_argument(
        "--allow-fallback-data",
        action="store_true",
        help="Allow non-tradeable fallback market data for explicit local reporting/simulation only.",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    result = run_once(mode=args.mode, allow_fallback_data=args.allow_fallback_data)
    print(json.dumps(result, indent=2, default=str))
