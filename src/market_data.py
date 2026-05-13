"""Fetch live market data from Alpaca for all watchlist symbols."""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from .strategy import MarketSnapshot

_FALLBACK_PRICES: Dict[str, float] = {
    "AAPL":    190.25,
    "NVDA":   1080.50,
    "TSLA":    175.30,
    "MSFT":    415.20,
    "AMZN":    182.60,
    "META":    510.40,
    "SPY":     520.00,
    "BTC/USD": 65000.00,
    "ETH/USD":  3100.00,
    "SOL/USD":   165.00,
}


def _fallback(symbol: str) -> MarketSnapshot:
    return MarketSnapshot(
        symbol=symbol,
        last_price=_FALLBACK_PRICES.get(symbol, 100.0),
        day_change_percent=0.0,
    )


def _snapshot_from_bars(sym: str, bar_list) -> MarketSnapshot:
    """Build a MarketSnapshot from a list of Bar objects (oldest → newest)."""
    if len(bar_list) >= 2:
        prev_close = float(bar_list[-2].close)
        last_close = float(bar_list[-1].close)
        day_chg = (last_close - prev_close) / prev_close * 100 if prev_close else 0.0
    elif len(bar_list) == 1:
        last_close = float(bar_list[0].close)
        day_chg = 0.0
    else:
        return _fallback(sym)
    return MarketSnapshot(symbol=sym, last_price=last_close, day_change_percent=day_chg)


def get_market_snapshots(symbols: List[dict]) -> Dict[str, MarketSnapshot]:
    """Return a price/momentum snapshot for every symbol in the watchlist."""
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")
    snapshots: Dict[str, MarketSnapshot] = {}

    if not api_key:
        return {s["symbol"]: _fallback(s["symbol"]) for s in symbols}

    try:
        from alpaca.data.historical import (
            CryptoHistoricalDataClient,
            StockHistoricalDataClient,
        )
        from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
        from alpaca.data.timeframe import TimeFrame
    except ImportError:
        return {s["symbol"]: _fallback(s["symbol"]) for s in symbols}

    start = datetime.now(timezone.utc) - timedelta(days=7)

    stock_syms = [s["symbol"] for s in symbols if s["type"] != "crypto"]
    crypto_syms = [s["symbol"] for s in symbols if s["type"] == "crypto"]

    # ── Stocks & ETFs ──────────────────────────────────────────────────────────
    if stock_syms:
        try:
            client = StockHistoricalDataClient(api_key, secret_key)
            req = StockBarsRequest(
                symbol_or_symbols=stock_syms,
                timeframe=TimeFrame.Day,
                start=start,
            )
            bars = client.get_stock_bars(req)
            for sym in stock_syms:
                try:
                    bar_list = bars[sym]
                    snapshots[sym] = _snapshot_from_bars(sym, bar_list)
                except Exception:
                    snapshots[sym] = _fallback(sym)
        except Exception:
            for sym in stock_syms:
                snapshots.setdefault(sym, _fallback(sym))

    # ── Crypto ─────────────────────────────────────────────────────────────────
    if crypto_syms:
        try:
            crypto_client = CryptoHistoricalDataClient()
            crypto_req = CryptoBarsRequest(
                symbol_or_symbols=crypto_syms,
                timeframe=TimeFrame.Day,
                start=start,
            )
            cbars = crypto_client.get_crypto_bars(crypto_req)
            for sym in crypto_syms:
                try:
                    bar_list = cbars[sym]
                    snapshots[sym] = _snapshot_from_bars(sym, bar_list)
                except Exception:
                    snapshots[sym] = _fallback(sym)
        except Exception:
            for sym in crypto_syms:
                snapshots.setdefault(sym, _fallback(sym))

    # fill any remaining gaps
    for s in symbols:
        snapshots.setdefault(s["symbol"], _fallback(s["symbol"]))

    return snapshots

