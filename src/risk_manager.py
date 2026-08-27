from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from typing import Optional

from .time_utils import trading_day


@dataclass(frozen=True)
class RiskConfig:
    portfolio_size: float = 10_000.0
    max_position_percent: float = 10.0
    max_daily_loss_percent: float = 2.0
    max_daily_trades: int = 3
    max_total_exposure_percent: float = 80.0
    allow_margin: bool = False
    allow_shorts: bool = False
    min_confidence: float = 0.70
    max_risk_percent: float = 1.0

    @classmethod
    def from_sources(cls, config: Optional[dict] = None) -> "RiskConfig":
        config = config or {}
        return cls(
            portfolio_size=_env_float("PORTFOLIO_SIZE", config.get("portfolio_size", 10_000)),
            max_position_percent=_env_float("MAX_POSITION_PERCENT", config.get("max_position_pct", 10)),
            max_daily_loss_percent=_env_float("MAX_DAILY_LOSS_PERCENT", config.get("max_daily_loss_percent", 2)),
            max_daily_trades=_env_int("MAX_DAILY_TRADES", config.get("max_daily_trades", 3)),
            max_total_exposure_percent=_env_float(
                "MAX_TOTAL_EXPOSURE_PERCENT",
                config.get("max_total_exposure_percent", 80),
            ),
            allow_margin=_env_bool("ALLOW_MARGIN", config.get("allow_margin", False)),
            allow_shorts=_env_bool("ALLOW_SHORTS", config.get("allow_shorts", False)),
            min_confidence=_env_float("MIN_CONFIDENCE", config.get("min_confidence", 0.70)),
            max_risk_percent=_env_float("MAX_RISK_PERCENT", config.get("max_risk_percent", 1.0)),
        )


@dataclass
class RiskEvaluationContext:
    mode: str
    asset_type: str
    entry_price: float
    account_equity: float
    actual_available_cash: float
    remaining_portfolio_capacity: float
    current_position_qty: float
    current_position_market_value: float
    current_gross_exposure: float
    traded_symbols_today: set[str]
    daily_trade_count: int
    paper_trading: bool
    market_data_is_fresh: bool
    market_data_source: str
    market_data_service_available: bool
    daily_loss_triggered: bool
    protective_stop_supported: bool
    allow_shorts: bool = False


@dataclass
class RiskCheckResult:
    approved: bool
    reasons: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    adjusted_qty: float = 0.0
    requested_qty: float = 0.0


def _env_float(name: str, default) -> float:
    value = os.getenv(name)
    return float(value) if value is not None else float(default)


def _env_int(name: str, default) -> int:
    value = os.getenv(name)
    return int(value) if value is not None else int(default)


def _env_bool(name: str, default) -> bool:
    value = os.getenv(name)
    if value is None:
        return bool(default)
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_qty_for_asset(asset_type: str, qty: float) -> float:
    qty = max(0.0, _safe_float(qty))
    if asset_type == "crypto":
        return math.floor(qty * 10_000) / 10_000
    return float(math.floor(qty))


def qty_for_notional(asset_type: str, entry_price: float, notional_value: float) -> float:
    if entry_price <= 0 or notional_value <= 0:
        return 0.0
    return normalize_qty_for_asset(asset_type, notional_value / entry_price)


def notional_value(entry_price: float, qty: float) -> float:
    return max(0.0, entry_price) * max(0.0, qty)


def validate_trade_startup_config(config: RiskConfig, paper_trading: bool) -> list[str]:
    errors: list[str] = []

    if not paper_trading:
        errors.append("ALPACA_PAPER must remain true. Live trading is not supported.")
    if config.allow_margin:
        errors.append("ALLOW_MARGIN must remain false.")
    if config.allow_shorts:
        errors.append("ALLOW_SHORTS must remain false.")
    if config.portfolio_size <= 0:
        errors.append("PORTFOLIO_SIZE must be greater than 0.")
    if not (0 < config.max_position_percent <= 100):
        errors.append("MAX_POSITION_PERCENT must be between 0 and 100.")
    if not (0 < config.max_total_exposure_percent <= 100):
        errors.append("MAX_TOTAL_EXPOSURE_PERCENT must be between 0 and 100.")
    if config.max_position_percent > config.max_total_exposure_percent:
        errors.append("MAX_POSITION_PERCENT must be less than or equal to MAX_TOTAL_EXPOSURE_PERCENT.")
    if config.max_daily_trades < 1:
        errors.append("MAX_DAILY_TRADES must be at least 1.")
    if config.max_daily_loss_percent <= 0:
        errors.append("MAX_DAILY_LOSS_PERCENT must be greater than 0.")
    if config.max_risk_percent <= 0:
        errors.append("MAX_RISK_PERCENT must be greater than 0.")
    if not (0 <= config.min_confidence <= 1):
        errors.append("MIN_CONFIDENCE must be between 0 and 1.")

    return errors


def risk_budget_base(portfolio_size: float, account_equity: float) -> float:
    return min(max(0.0, portfolio_size), max(0.0, account_equity))


class RiskManager:
    def __init__(self, config: Optional[RiskConfig] = None, min_confidence: Optional[float] = None, max_risk_percent: Optional[float] = None) -> None:
        base_config = config or RiskConfig()
        if min_confidence is not None or max_risk_percent is not None:
            base_config = RiskConfig(
                portfolio_size=base_config.portfolio_size,
                max_position_percent=base_config.max_position_percent,
                max_daily_loss_percent=base_config.max_daily_loss_percent,
                max_daily_trades=base_config.max_daily_trades,
                max_total_exposure_percent=base_config.max_total_exposure_percent,
                allow_margin=base_config.allow_margin,
                allow_shorts=base_config.allow_shorts,
                min_confidence=base_config.min_confidence if min_confidence is None else min_confidence,
                max_risk_percent=base_config.max_risk_percent if max_risk_percent is None else max_risk_percent,
            )
        self.config = base_config

    def evaluate(self, decision: dict, context: RiskEvaluationContext) -> RiskCheckResult:
        symbol = str(decision.get("symbol", "")).upper()
        action = str(decision.get("action", "hold")).lower()
        confidence = _safe_float(decision.get("confidence", 0.0))
        requested_qty = normalize_qty_for_asset(context.asset_type, _safe_float(decision.get("qty", 0.0)))
        stop_loss_value = decision.get("stop_loss")
        max_risk_percent = _safe_float(decision.get("max_risk_percent", self.config.max_risk_percent), self.config.max_risk_percent)

        reasons: list[str] = []
        notes: list[str] = []

        if not context.paper_trading:
            reasons.append("Rejected: paper trading only.")

        if context.mode != "trade":
            reasons.append("Rejected: report mode cannot place orders.")

        if not context.market_data_service_available:
            reasons.append("Rejected: fresh market data unavailable; trading skipped.")
        elif not context.market_data_is_fresh:
            reasons.append(
                f"Rejected: fresh Alpaca market data unavailable for {symbol or 'symbol'} (source={context.market_data_source})."
            )

        if context.daily_trade_count >= self.config.max_daily_trades:
            reasons.append(
                f"Rejected: global daily trade limit reached ({self.config.max_daily_trades} trades per day)."
            )

        if symbol in context.traded_symbols_today:
            reasons.append("Rejected: max 1 trade per symbol per day exceeded.")

        if confidence < self.config.min_confidence:
            reasons.append(f"Rejected: confidence {confidence:.2f} below {self.config.min_confidence:.2f}.")

        if action not in {"buy", "sell", "hold"}:
            reasons.append("Rejected: invalid action.")

        if action == "hold":
            reasons.append("Rejected: hold signal does not place a trade.")

        if requested_qty <= 0.0:
            reasons.append("Rejected: quantity must be positive.")

        if max_risk_percent > self.config.max_risk_percent:
            reasons.append(
                f"Rejected: max_risk_percent {max_risk_percent:.2f}% exceeds {self.config.max_risk_percent:.2f}% policy."
            )

        if reasons:
            return RiskCheckResult(False, reasons=reasons, notes=notes, adjusted_qty=0.0, requested_qty=requested_qty)

        if action == "sell":
            return self._evaluate_sell(
                requested_qty=requested_qty,
                context=context,
                notes=notes,
            )

        return self._evaluate_buy(
            symbol=symbol,
            requested_qty=requested_qty,
            stop_loss_value=stop_loss_value,
            context=context,
            notes=notes,
        )

    def _evaluate_sell(
        self,
        requested_qty: float,
        context: RiskEvaluationContext,
        notes: list[str],
    ) -> RiskCheckResult:
        reasons: list[str] = []
        held_qty = max(0.0, context.current_position_qty)
        adjusted_qty = requested_qty

        if held_qty <= 0.0:
            reasons.append("Rejected: no long position exists to sell.")

        if not context.allow_shorts and requested_qty > held_qty > 0.0:
            adjusted_qty = normalize_qty_for_asset(context.asset_type, held_qty)
            notes.append(
                f"Resized SELL quantity from {requested_qty:g} to {adjusted_qty:g} so the trade cannot open or increase a short position."
            )

        if adjusted_qty <= 0.0:
            reasons.append("Rejected: sell quantity must not exceed the currently held long quantity.")

        return RiskCheckResult(
            approved=len(reasons) == 0,
            reasons=reasons,
            notes=notes,
            adjusted_qty=adjusted_qty if len(reasons) == 0 else 0.0,
            requested_qty=requested_qty,
        )

    def _evaluate_buy(
        self,
        symbol: str,
        requested_qty: float,
        stop_loss_value,
        context: RiskEvaluationContext,
        notes: list[str],
    ) -> RiskCheckResult:
        reasons: list[str] = []

        if context.daily_loss_triggered:
            reasons.append("Rejected: daily loss circuit breaker triggered; new BUY orders are blocked.")

        if not context.protective_stop_supported:
            reasons.append(
                f"Rejected: unable to guarantee broker-side protective stop placement for {symbol or 'this asset'}."
            )

        stop_price = _safe_float(stop_loss_value, 0.0)
        if stop_loss_value is None:
            reasons.append("Rejected: stop loss is required for BUY orders.")
        elif stop_price <= 0.0:
            reasons.append("Rejected: stop loss must be numeric and positive.")
        elif stop_price >= context.entry_price:
            reasons.append("Rejected: BUY stop loss must be below the entry price.")

        if not context.allow_shorts and context.current_position_qty < 0.0:
            reasons.append("Rejected: BUY against an existing short position is not supported while shorts are disabled.")

        if reasons:
            return RiskCheckResult(False, reasons=reasons, notes=notes, adjusted_qty=0.0, requested_qty=requested_qty)

        max_position_value = self.config.portfolio_size * (self.config.max_position_percent / 100.0)
        max_total_exposure_value = self.config.portfolio_size * (self.config.max_total_exposure_percent / 100.0)
        current_position_value = max(0.0, context.current_position_market_value)
        remaining_position_value = max(0.0, max_position_value - current_position_value)
        remaining_exposure_value = max(0.0, max_total_exposure_value - context.current_gross_exposure)
        remaining_portfolio_capacity = max(0.0, context.remaining_portfolio_capacity)
        actual_available_cash = max(0.0, context.actual_available_cash)

        per_unit_risk = max(0.0, context.entry_price - stop_price)
        risk_base = risk_budget_base(self.config.portfolio_size, context.account_equity)
        allowed_risk = max(0.0, risk_base * (self.config.max_risk_percent / 100.0))
        risk_qty_limit = normalize_qty_for_asset(
            context.asset_type,
            allowed_risk / per_unit_risk if per_unit_risk > 0.0 else 0.0,
        )

        qty_limits = {
            "position": qty_for_notional(context.asset_type, context.entry_price, remaining_position_value),
            "exposure": qty_for_notional(context.asset_type, context.entry_price, remaining_exposure_value),
            "cash": qty_for_notional(context.asset_type, context.entry_price, actual_available_cash),
            "portfolio": qty_for_notional(context.asset_type, context.entry_price, remaining_portfolio_capacity),
            "risk": risk_qty_limit,
        }
        adjusted_qty = requested_qty
        for qty_limit in qty_limits.values():
            adjusted_qty = min(adjusted_qty, qty_limit)
        adjusted_qty = normalize_qty_for_asset(context.asset_type, adjusted_qty)

        if adjusted_qty <= 0.0:
            if remaining_position_value <= 0.0:
                reasons.append(
                    f"Rejected: projected {symbol} position would exceed the ${max_position_value:.2f} max-position limit."
                )
            if remaining_exposure_value <= 0.0:
                reasons.append(
                    f"Rejected: projected exposure would exceed the ${max_total_exposure_value:.2f} max-total-exposure limit."
                )
            if remaining_portfolio_capacity <= 0.0:
                reasons.append("Rejected: configured portfolio budget is fully deployed.")
            if actual_available_cash <= 0.0:
                reasons.append("Rejected: no margin allowed; insufficient configured available cash.")
            if risk_qty_limit <= 0.0:
                reasons.append("Rejected: stop distance exceeds the allowed per-trade risk budget.")
            if not reasons:
                reasons.append("Rejected: no BUY quantity remained after applying safety constraints.")
            return RiskCheckResult(False, reasons=reasons, notes=notes, adjusted_qty=0.0, requested_qty=requested_qty)

        if adjusted_qty < requested_qty:
            notes.append(
                f"Resized BUY quantity from {requested_qty:g} to {adjusted_qty:g} to stay within position, exposure, cash, and risk limits."
            )

        approved_value = notional_value(context.entry_price, adjusted_qty)
        projected_position_value = current_position_value + approved_value
        projected_total_exposure = context.current_gross_exposure + approved_value

        if projected_position_value > max_position_value + 1e-9:
            reasons.append(
                f"Rejected: projected {symbol} position would exceed the ${max_position_value:.2f} max-position limit."
            )
        if projected_total_exposure > max_total_exposure_value + 1e-9:
            reasons.append(
                f"Rejected: projected exposure would exceed the ${max_total_exposure_value:.2f} max-total-exposure limit."
            )
        if approved_value > actual_available_cash + 1e-9:
            reasons.append("Rejected: no margin allowed; insufficient configured available cash.")
        if approved_value > remaining_portfolio_capacity + 1e-9:
            reasons.append("Rejected: purchase would exceed the configured portfolio budget.")

        return RiskCheckResult(
            approved=len(reasons) == 0,
            reasons=reasons,
            notes=notes,
            adjusted_qty=adjusted_qty if len(reasons) == 0 else 0.0,
            requested_qty=requested_qty,
        )


def today() -> str:
    return trading_day()


