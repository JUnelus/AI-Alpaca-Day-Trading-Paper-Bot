import os
from dataclasses import dataclass
from typing import Optional

try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce
except Exception:  # pragma: no cover - import guarded for local runs without deps
    TradingClient = None
    MarketOrderRequest = None
    OrderSide = None
    TimeInForce = None


@dataclass
class AccountSnapshot:
    equity: float
    cash: float


class AlpacaClient:
    def __init__(self) -> None:
        api_key = os.getenv("ALPACA_API_KEY")
        secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.paper = os.getenv("ALPACA_PAPER", "true").lower() == "true"
        self._client: Optional[TradingClient] = None

        if TradingClient and api_key and secret_key and self.paper:
            self._client = TradingClient(api_key, secret_key, paper=True)

    @property
    def is_ready(self) -> bool:
        return self._client is not None

    def get_account_snapshot(self) -> AccountSnapshot:
        if not self._client:
            # Safe fallback for local dry runs.
            return AccountSnapshot(equity=100000.0, cash=100000.0)

        account = self._client.get_account()
        return AccountSnapshot(equity=float(account.equity), cash=float(account.cash))

    def list_positions(self) -> list:
        if not self._client:
            return []
        try:
            return list(self._client.get_all_positions())
        except Exception:
            return []

    def place_paper_trade(self, symbol: str, qty: float, side: str):
        if not self._client:
            return {
                "status": "skipped",
                "message": "No Alpaca credentials available; dry-run only.",
                "symbol": symbol,
                "qty": qty,
                "side": side,
            }

        if not self.paper:
            raise ValueError("Paper trading is required for this bot.")

        # Crypto (symbol contains "/") requires GTC; stocks/ETFs use DAY.
        tif = TimeInForce.GTC if "/" in symbol else TimeInForce.DAY
        order = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
            time_in_force=tif,
        )
        try:
            return self._client.submit_order(order)
        except Exception as exc:
            return {"status": "error", "message": str(exc), "symbol": symbol, "qty": qty, "side": side}

