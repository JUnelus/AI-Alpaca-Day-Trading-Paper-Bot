"""Read live positions & P&L from the Alpaca paper account."""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .alpaca_client import AlpacaClient

STARTING_BALANCE: float = 10_000.00
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "portfolio_state.json")

_CRYPTO_NORMALIZE: Dict[str, str] = {
    "BTCUSD": "BTC/USD",
    "ETHUSD": "ETH/USD",
    "SOLUSD": "SOL/USD",
}


def _norm(symbol: str) -> str:
    return _CRYPTO_NORMALIZE.get(symbol.upper(), symbol)


@dataclass
class PositionSnapshot:
    symbol: str
    asset_type: str
    qty: float
    avg_entry_price: Optional[float]
    current_price: Optional[float]
    market_value: Optional[float]
    cost_basis: Optional[float]
    unrealized_pnl: Optional[float]
    unrealized_pnl_pct: Optional[float]


@dataclass
class PortfolioState:
    starting_balance: float = STARTING_BALANCE
    account_equity: float = STARTING_BALANCE
    cash: float = STARTING_BALANCE
    buying_power: float = STARTING_BALANCE
    positions: List[PositionSnapshot] = field(default_factory=list)
    total_pnl: float = 0.0
    total_pnl_pct: float = 0.0
    yesterday_total_pnl: Optional[float] = None
    yesterday_equity: Optional[float] = None
    last_updated: str = ""
    trades_today: int = 0
    trading_day: str = ""
    traded_symbols_today: List[str] = field(default_factory=list)
    start_of_day_equity: Optional[float] = None
    daily_pnl: float = 0.0
    daily_loss_limit: float = 0.0
    daily_loss_triggered: bool = False
    gross_exposure: float = 0.0
    max_total_exposure: float = 0.0
    warnings: List[str] = field(default_factory=list)
    mode: str = "report"
    last_scheduled_trade_day: str = ""
    last_scheduled_report_day: str = ""
    pnl_data_complete: bool = True
    unknown_position_pnl_count: int = 0

    # ── persistence ────────────────────────────────────────────────────────────

    def save(self, path: str = STATE_FILE) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2, default=str)

    @classmethod
    def load(cls, path: str = STATE_FILE) -> "PortfolioState":
        if not os.path.exists(path):
            return cls()
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            positions = [PositionSnapshot(**p) for p in data.pop("positions", [])]
            state = cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
            state.positions = positions
            return state
        except Exception:
            return cls()


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_optional_float(value) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def refresh_from_alpaca(
    alpaca_client: "AlpacaClient",
    symbol_type_map: Dict[str, str],
    price_map: Dict[str, float],
    starting_balance: float = STARTING_BALANCE,
    trades_today: int = 0,
    account_snapshot=None,
) -> PortfolioState:
    """Fetch the live Alpaca paper account and build a PortfolioState."""
    account = account_snapshot or alpaca_client.get_account_snapshot()
    positions_raw = alpaca_client.list_positions()

    positions: List[PositionSnapshot] = []
    unknown_position_pnl_count = 0
    for pos in positions_raw:
        sym = _norm(getattr(pos, "symbol", ""))
        qty = _safe_float(getattr(pos, "qty", 0.0))

        raw_cost_basis = _safe_optional_float(getattr(pos, "cost_basis", None))
        cost_basis = raw_cost_basis if raw_cost_basis is not None and raw_cost_basis > 0 else None

        raw_avg_entry = _safe_optional_float(getattr(pos, "avg_entry_price", None))
        avg_entry = raw_avg_entry if raw_avg_entry is not None and raw_avg_entry > 0 else None
        if avg_entry is None and cost_basis is not None and qty > 0:
            avg_entry = cost_basis / qty

        # Prefer Alpaca's own current_price; fall back to price_map snapshot.
        raw_current = _safe_optional_float(getattr(pos, "current_price", None))
        current_price = raw_current if raw_current is not None else price_map.get(sym, avg_entry)
        if current_price is not None and current_price <= 0:
            current_price = None

        raw_mv = _safe_optional_float(getattr(pos, "market_value", None))
        mkt_value = raw_mv if raw_mv is not None else (qty * current_price if current_price is not None else None)

        raw_pl = _safe_optional_float(getattr(pos, "unrealized_pl", None))
        raw_plpc = _safe_optional_float(getattr(pos, "unrealized_plpc", None))
        if raw_pl is not None:
            unrealized = raw_pl
        elif current_price is not None and avg_entry is not None:
            unrealized = (current_price - avg_entry) * qty
        else:
            unrealized = None

        if raw_plpc is not None:
            unrealized_pct = raw_plpc * 100.0
        elif unrealized is not None and cost_basis is not None and cost_basis > 0:
            unrealized_pct = (unrealized / cost_basis) * 100.0
        else:
            unrealized_pct = None

        if unrealized is None:
            unknown_position_pnl_count += 1

        asset_type = symbol_type_map.get(sym, "crypto" if "/" in sym else "stock")
        positions.append(
            PositionSnapshot(
                symbol=sym,
                asset_type=asset_type,
                qty=qty,
                avg_entry_price=avg_entry,
                current_price=current_price,
                market_value=mkt_value,
                cost_basis=cost_basis,
                unrealized_pnl=unrealized,
                unrealized_pnl_pct=unrealized_pct,
            )
        )

    equity = account.equity
    total_pnl = sum(p.unrealized_pnl for p in positions if p.unrealized_pnl is not None)
    total_pnl_pct = (total_pnl / starting_balance * 100) if starting_balance else 0.0
    gross_exposure = sum(abs(p.market_value) for p in positions if p.market_value is not None)

    return PortfolioState(
        starting_balance=starting_balance,
        account_equity=equity,
        cash=account.cash,
        buying_power=account.buying_power,
        positions=positions,
        total_pnl=total_pnl,
        total_pnl_pct=total_pnl_pct,
        last_updated=datetime.now(timezone.utc).isoformat(),
        trades_today=trades_today,
        gross_exposure=gross_exposure,
        pnl_data_complete=unknown_position_pnl_count == 0,
        unknown_position_pnl_count=unknown_position_pnl_count,
    )


