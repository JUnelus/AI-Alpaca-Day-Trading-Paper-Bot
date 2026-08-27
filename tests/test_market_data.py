from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from src.market_data import _snapshot_from_alpaca_snapshot, get_market_snapshots


def test_fresh_alpaca_data_can_be_used_for_trading():
    now = datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc)
    snapshot = SimpleNamespace(
        latest_trade=SimpleNamespace(price=100.0, timestamp=now - timedelta(minutes=1)),
        daily_bar=SimpleNamespace(close=99.5, timestamp=now - timedelta(minutes=1)),
        previous_daily_bar=SimpleNamespace(close=98.0, timestamp=now - timedelta(days=1)),
    )

    result = _snapshot_from_alpaca_snapshot("AAPL", "stock", snapshot, now)

    assert result.source == "alpaca"
    assert result.is_fresh
    assert not result.is_fallback
    assert result.last_price == 100.0
    assert round(result.day_change_percent, 2) == round((100.0 - 98.0) / 98.0 * 100, 2)


def test_missing_credentials_can_return_explicit_fallback_data_for_simulation(monkeypatch):
    monkeypatch.delenv("ALPACA_API_KEY", raising=False)
    monkeypatch.delenv("ALPACA_SECRET_KEY", raising=False)

    result = get_market_snapshots(
        [{"symbol": "AAPL", "type": "stock"}],
        allow_fallback_data=True,
    )

    snapshot = result.snapshots["AAPL"]
    assert not result.service_available
    assert result.used_fallback_data
    assert snapshot.source == "fallback"
    assert not snapshot.is_fresh
    assert snapshot.is_fallback


def test_missing_credentials_without_fallback_marks_data_unavailable(monkeypatch):
    monkeypatch.delenv("ALPACA_API_KEY", raising=False)
    monkeypatch.delenv("ALPACA_SECRET_KEY", raising=False)

    result = get_market_snapshots(
        [{"symbol": "AAPL", "type": "stock"}],
        allow_fallback_data=False,
    )

    snapshot = result.snapshots["AAPL"]
    assert not result.service_available
    assert not result.used_fallback_data
    assert snapshot.source == "unavailable"
    assert not snapshot.is_fresh
    assert snapshot.last_price == 0.0


