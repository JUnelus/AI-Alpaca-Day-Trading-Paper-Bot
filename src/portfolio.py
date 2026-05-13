"""Read live positions & P&L from the Alpaca paper account."""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, TYPE_CHECKING

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
    avg_entry_price: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float


@dataclass
class PortfolioState:
    starting_balance: float = STARTING_BALANCE
    account_equity: float = STARTING_BALANCE
    cash: float = STARTING_BALANCE
    positions: List[PositionSnapshot] = field(default_factory=list)
    total_pnl: float = 0.0
    total_pnl_pct: float = 0.0
    last_updated: str = ""
    trades_today: int = 0

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


def refresh_from_alpaca(
    alpaca_client: "AlpacaClient",
    symbol_type_map: Dict[str, str],
    price_map: Dict[str, float],
    trades_today: int = 0,
) -> PortfolioState:
    """Fetch the live Alpaca paper account and build a PortfolioState."""
    account = alpaca_client.get_account_snapshot()
    positions_raw = alpaca_client.list_positions()

    positions: List[PositionSnapshot] = []
    for pos in positions_raw:
        sym = _norm(getattr(pos, "symbol", ""))
        qty = float(getattr(pos, "qty", 0))
        avg_entry = float(getattr(pos, "avg_entry_price", 0))

        # Prefer Alpaca's own current_price; fall back to price_map snapshot.
        raw_current = getattr(pos, "current_price", None)
        current_price = float(raw_current) if raw_current else price_map.get(sym, avg_entry)

        raw_mv = getattr(pos, "market_value", None)
        mkt_value = float(raw_mv) if raw_mv else qty * current_price

        raw_pl = getattr(pos, "unrealized_pl", None)
        unrealized = float(raw_pl) if raw_pl else (current_price - avg_entry) * qty

        cost_basis = avg_entry * qty
        unrealized_pct = (unrealized / cost_basis * 100) if cost_basis else 0.0

        asset_type = symbol_type_map.get(sym, "stock")
        positions.append(
            PositionSnapshot(
                symbol=sym,
                asset_type=asset_type,
                qty=qty,
                avg_entry_price=avg_entry,
                current_price=current_price,
                market_value=mkt_value,
                unrealized_pnl=unrealized,
                unrealized_pnl_pct=unrealized_pct,
            )
        )

    equity = account.equity
    # P&L is calculated against the $10k portfolio budget, not the broker's
    # default paper balance (Alpaca starts paper accounts at $100k).
    total_pnl = sum(p.unrealized_pnl for p in positions)
    total_pnl_pct = (total_pnl / STARTING_BALANCE) * 100

    return PortfolioState(
        starting_balance=STARTING_BALANCE,
        account_equity=equity,
        cash=account.cash,
        positions=positions,
        total_pnl=total_pnl,
        total_pnl_pct=total_pnl_pct,
        last_updated=datetime.now(timezone.utc).isoformat(),
        trades_today=trades_today,
    )


