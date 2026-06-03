from src.strategy import MarketSnapshot, generate_signal


def test_quality_asset_dip_generates_dca_buy():
    snapshot = MarketSnapshot(symbol="MSFT", last_price=400.0, day_change_percent=-1.8)
    signal = generate_signal(snapshot, {"quality_score": 0.92})

    assert signal.action == "buy"
    assert "dca" in signal.reason.lower()
    assert signal.strength >= 0.7


def test_low_quality_breakdown_generates_sell():
    snapshot = MarketSnapshot(symbol="SOL/USD", last_price=70.0, day_change_percent=-3.4)
    signal = generate_signal(snapshot, {"quality_score": 0.5})

    assert signal.action == "sell"
    assert "risk reduction" in signal.reason.lower()


def test_up_day_without_extreme_move_holds():
    snapshot = MarketSnapshot(symbol="AAPL", last_price=200.0, day_change_percent=1.2)
    signal = generate_signal(snapshot, {"quality_score": 0.9})

    assert signal.action == "hold"

