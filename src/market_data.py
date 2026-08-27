"""Fetch live market data from Alpaca for all watchlist symbols."""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from .strategy import MarketSnapshot
from .time_utils import ensure_aware

_FALLBACK_PRICES: Dict[str, float] = {
    "AAPL": 190.25,
    "NVDA": 1080.50,
    "TSLA": 175.30,
    "MSFT": 415.20,
    "AMZN": 182.60,
    "META": 510.40,
    "SPY": 520.00,
    "BTC/USD": 65000.00,
    "ETH/USD": 3100.00,
    "SOL/USD": 165.00,
}
_STOCK_FRESHNESS = timedelta(minutes=20)
_CRYPTO_FRESHNESS = timedelta(minutes=10)


@dataclass
class MarketDataResult:
    snapshots: Dict[str, MarketSnapshot]
    service_available: bool
    used_fallback_data: bool = False
    message: str | None = None


def _fallback(symbol: str, as_of: datetime) -> MarketSnapshot:
    return MarketSnapshot(
        symbol=symbol,
        last_price=_FALLBACK_PRICES.get(symbol, 100.0),
        day_change_percent=0.0,
        source="fallback",
        timestamp=as_of,
        is_fresh=False,
        is_fallback=True,
    )


def _unavailable_snapshot(symbol: str) -> MarketSnapshot:
    return MarketSnapshot(
        symbol=symbol,
        last_price=0.0,
        day_change_percent=0.0,
        source="unavailable",
        timestamp=None,
        is_fresh=False,
        is_fallback=False,
    )


def _freshness_limit(asset_type: str) -> timedelta:
    return _CRYPTO_FRESHNESS if asset_type == "crypto" else _STOCK_FRESHNESS


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _snapshot_from_alpaca_snapshot(symbol: str, asset_type: str, snapshot, as_of: datetime) -> MarketSnapshot:
    latest_trade = getattr(snapshot, "latest_trade", None)
    daily_bar = getattr(snapshot, "daily_bar", None)
    previous_daily_bar = getattr(snapshot, "previous_daily_bar", None)

    raw_price = None
    if latest_trade is not None:
        raw_price = getattr(latest_trade, "price", None)
    if raw_price is None and daily_bar is not None:
        raw_price = getattr(daily_bar, "close", None)
    if raw_price is None and previous_daily_bar is not None:
        raw_price = getattr(previous_daily_bar, "close", None)
    if raw_price is None:
        return _unavailable_snapshot(symbol)

    price = _safe_float(raw_price)
    prev_close = getattr(previous_daily_bar, "close", None)
    prev_close_value = _safe_float(prev_close)
    day_change = ((price - prev_close_value) / prev_close_value * 100.0) if prev_close_value else 0.0

    raw_timestamp = None
    if latest_trade is not None:
        raw_timestamp = getattr(latest_trade, "timestamp", None)
    if raw_timestamp is None and daily_bar is not None:
        raw_timestamp = getattr(daily_bar, "timestamp", None)
    timestamp = ensure_aware(raw_timestamp or as_of)
    age_seconds = abs((as_of - timestamp).total_seconds())
    is_fresh = latest_trade is not None and age_seconds <= _freshness_limit(asset_type).total_seconds()

    return MarketSnapshot(
        symbol=symbol,
        last_price=price,
        day_change_percent=day_change,
        source="alpaca",
        timestamp=timestamp,
        is_fresh=is_fresh,
        is_fallback=False,
    )


def _get_mapping_entry(data, symbol: str):
    if data is None:
        return None
    if hasattr(data, "get"):
        return data.get(symbol)
    try:
        return data[symbol]
    except Exception:
        return None


def _build_snapshots_for_group(
    symbols: List[str],
    asset_type: str,
    client,
    request,
    request_method: str,
    allow_fallback_data: bool,
    as_of: datetime,
) -> tuple[Dict[str, MarketSnapshot], bool, str | None]:
    if not symbols:
        return {}, False, None

    try:
        response = getattr(client, request_method)(request)
    except Exception as exc:
        fallback_map = {
            symbol: (_fallback(symbol, as_of) if allow_fallback_data else _unavailable_snapshot(symbol))
            for symbol in symbols
        }
        return fallback_map, False, str(exc)

    snapshots: Dict[str, MarketSnapshot] = {}
    for symbol in symbols:
        snapshot = _get_mapping_entry(response, symbol)
        if snapshot is None:
            snapshots[symbol] = _fallback(symbol, as_of) if allow_fallback_data else _unavailable_snapshot(symbol)
            continue
        snapshots[symbol] = _snapshot_from_alpaca_snapshot(symbol, asset_type, snapshot, as_of)
    return snapshots, True, None


def get_market_snapshots(
    symbols: List[dict],
    allow_fallback_data: bool = False,
    now: datetime | None = None,
) -> MarketDataResult:
    """Return a validated market-data snapshot for every symbol in the watchlist."""
    as_of = ensure_aware(now or datetime.now(timezone.utc))
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        snapshot_map = {
            item["symbol"]: (_fallback(item["symbol"], as_of) if allow_fallback_data else _unavailable_snapshot(item["symbol"]))
            for item in symbols
        }
        return MarketDataResult(
            snapshots=snapshot_map,
            service_available=False,
            used_fallback_data=allow_fallback_data,
            message="Fresh Alpaca market data was unavailable because credentials were not configured.",
        )

    try:
        from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
        from alpaca.data.requests import CryptoSnapshotRequest, StockSnapshotRequest
    except ImportError:
        snapshot_map = {
            item["symbol"]: (_fallback(item["symbol"], as_of) if allow_fallback_data else _unavailable_snapshot(item["symbol"]))
            for item in symbols
        }
        return MarketDataResult(
            snapshots=snapshot_map,
            service_available=False,
            used_fallback_data=allow_fallback_data,
            message="Fresh Alpaca market data was unavailable because alpaca-py market-data support could not be imported.",
        )

    stock_symbols = [item["symbol"] for item in symbols if item["type"] != "crypto"]
    crypto_symbols = [item["symbol"] for item in symbols if item["type"] == "crypto"]
    snapshots: Dict[str, MarketSnapshot] = {}
    errors: list[str] = []
    any_api_success = False

    if stock_symbols:
        stock_client = StockHistoricalDataClient(api_key, secret_key)
        stock_request = StockSnapshotRequest(symbol_or_symbols=stock_symbols)
        stock_snapshots, stock_success, stock_error = _build_snapshots_for_group(
            symbols=stock_symbols,
            asset_type="stock",
            client=stock_client,
            request=stock_request,
            request_method="get_stock_snapshot",
            allow_fallback_data=allow_fallback_data,
            as_of=as_of,
        )
        snapshots.update(stock_snapshots)
        any_api_success = any_api_success or stock_success
        if stock_error:
            errors.append(f"stock data: {stock_error}")

    if crypto_symbols:
        crypto_client = CryptoHistoricalDataClient()
        crypto_request = CryptoSnapshotRequest(symbol_or_symbols=crypto_symbols)
        crypto_snapshots, crypto_success, crypto_error = _build_snapshots_for_group(
            symbols=crypto_symbols,
            asset_type="crypto",
            client=crypto_client,
            request=crypto_request,
            request_method="get_crypto_snapshot",
            allow_fallback_data=allow_fallback_data,
            as_of=as_of,
        )
        snapshots.update(crypto_snapshots)
        any_api_success = any_api_success or crypto_success
        if crypto_error:
            errors.append(f"crypto data: {crypto_error}")

    for item in symbols:
        snapshots.setdefault(
            item["symbol"],
            _fallback(item["symbol"], as_of) if allow_fallback_data else _unavailable_snapshot(item["symbol"]),
        )

    return MarketDataResult(
        snapshots=snapshots,
        service_available=any_api_success,
        used_fallback_data=any(snapshot.is_fallback for snapshot in snapshots.values()),
        message="; ".join(errors) if errors else None,
    )

