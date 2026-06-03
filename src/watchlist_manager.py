"""Weekly watchlist refresh based on market value (market cap / ETF assets)."""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

DEFAULT_WATCHLIST_UNIVERSE: List[dict] = [
    {"symbol": "MSFT", "name": "Microsoft Corp.", "type": "stock", "quality_score": 0.95},
    {"symbol": "AAPL", "name": "Apple Inc.", "type": "stock", "quality_score": 0.93},
    {"symbol": "NVDA", "name": "NVIDIA Corp.", "type": "stock", "quality_score": 0.89},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "type": "stock", "quality_score": 0.88},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "type": "stock", "quality_score": 0.90},
    {"symbol": "META", "name": "Meta Platforms Inc.", "type": "stock", "quality_score": 0.87},
    {"symbol": "BRK.B", "name": "Berkshire Hathaway", "type": "stock", "quality_score": 0.90},
    {"symbol": "LLY", "name": "Eli Lilly and Co.", "type": "stock", "quality_score": 0.82},
    {"symbol": "AVGO", "name": "Broadcom Inc.", "type": "stock", "quality_score": 0.84},
    {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "type": "stock", "quality_score": 0.81},
    {"symbol": "V", "name": "Visa Inc.", "type": "stock", "quality_score": 0.88},
    {"symbol": "WMT", "name": "Walmart Inc.", "type": "stock", "quality_score": 0.80},
    {"symbol": "XOM", "name": "Exxon Mobil Corp.", "type": "stock", "quality_score": 0.76},
    {"symbol": "UNH", "name": "UnitedHealth Group", "type": "stock", "quality_score": 0.78},
    {"symbol": "SPY", "name": "SPDR S&P 500 ETF", "type": "etf", "quality_score": 0.86},
    {"symbol": "QQQ", "name": "Invesco QQQ Trust", "type": "etf", "quality_score": 0.85},
    {"symbol": "VTI", "name": "Vanguard Total Stock Market ETF", "type": "etf", "quality_score": 0.84},
    {"symbol": "BTC/USD", "name": "Bitcoin", "type": "crypto", "quality_score": 0.72},
    {"symbol": "ETH/USD", "name": "Ethereum", "type": "crypto", "quality_score": 0.66},
    {"symbol": "SOL/USD", "name": "Solana", "type": "crypto", "quality_score": 0.55},
]


def _week_key(as_of: date) -> str:
    iso = as_of.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _to_yf_ticker(symbol: str, asset_type: str) -> str:
    if asset_type.lower() == "crypto":
        return symbol.replace("/", "-")
    return symbol


def _safe_market_value(ticker) -> float:
    fast_info = getattr(ticker, "fast_info", None)
    if fast_info:
        market_cap = fast_info.get("market_cap")
        if isinstance(market_cap, (int, float)) and market_cap > 0:
            return float(market_cap)

    info = getattr(ticker, "info", {}) or {}
    for key in ("marketCap", "enterpriseValue", "totalAssets"):
        value = info.get(key)
        if isinstance(value, (int, float)) and value > 0:
            return float(value)

    return 0.0


def _fetch_market_values(universe: Iterable[dict]) -> Dict[str, float]:
    try:
        import yfinance as yf
    except ImportError:
        return {}

    values: Dict[str, float] = {}
    for item in universe:
        symbol = item["symbol"]
        ticker_symbol = _to_yf_ticker(symbol, item.get("type", "stock"))
        try:
            ticker = yf.Ticker(ticker_symbol)
            values[symbol] = _safe_market_value(ticker)
        except Exception:
            values[symbol] = 0.0

    return values


def select_top_symbols(universe: List[dict], values: Dict[str, float], limit: int) -> List[dict]:
    # Stable sort keeps input order for equal values, then we trim to target size.
    ranked = sorted(universe, key=lambda item: values.get(item["symbol"], 0.0), reverse=True)
    selected = ranked[:limit]

    if len(selected) < limit:
        seen = {s["symbol"] for s in selected}
        for item in universe:
            if item["symbol"] in seen:
                continue
            selected.append(item)
            if len(selected) >= limit:
                break

    return selected


def refresh_weekly_watchlist(config_path: str, limit: int = 10, as_of: date | None = None) -> bool:
    config_file = Path(config_path)
    if not config_file.exists():
        return False

    now = as_of or date.today()
    this_week = _week_key(now)

    with config_file.open("r", encoding="utf-8") as f:
        config = json.load(f)

    if config.get("last_watchlist_refresh_week") == this_week:
        return False

    universe = config.get("watchlist_universe") or config.get("symbols") or DEFAULT_WATCHLIST_UNIVERSE
    values = _fetch_market_values(universe)

    if values:
        config["symbols"] = select_top_symbols(universe, values, limit)
    else:
        config["symbols"] = select_top_symbols(list(universe), {}, limit)

    config["last_watchlist_refresh_week"] = this_week
    config["last_watchlist_refresh_at"] = datetime.now(timezone.utc).isoformat()

    with config_file.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    return True

