from src.risk_manager import RiskManager


def _base_decision() -> dict:
    return {
        "symbol": "AAPL",
        "action": "buy",
        "confidence": 0.9,
        "reason": "Momentum trend confirmed",
        "max_risk_percent": 1,
        "qty": 1,
        "stop_loss": 99.0,
    }


def test_reject_low_confidence():
    manager = RiskManager(min_confidence=0.70, max_risk_percent=1.0)
    decision = _base_decision()
    decision["confidence"] = 0.69

    result = manager.evaluate(decision, 100000, 100000, 100.0, set(), True)
    assert not result.approved
    assert any("confidence" in reason.lower() for reason in result.reasons)


def test_reject_second_trade_same_symbol_same_day():
    manager = RiskManager()
    result = manager.evaluate(_base_decision(), 100000, 100000, 100.0, {"AAPL"}, True)
    assert not result.approved
    assert any("per symbol per day" in reason.lower() for reason in result.reasons)


def test_reject_if_not_paper_trading():
    manager = RiskManager()
    result = manager.evaluate(_base_decision(), 100000, 100000, 100.0, set(), False)
    assert not result.approved
    assert any("paper trading" in reason.lower() for reason in result.reasons)


def test_reject_without_stop_loss():
    manager = RiskManager()
    decision = _base_decision()
    decision["stop_loss"] = None

    result = manager.evaluate(decision, 100000, 100000, 100.0, set(), True)
    assert not result.approved
    assert any("stop loss" in reason.lower() for reason in result.reasons)


def test_approve_valid_trade():
    manager = RiskManager()
    result = manager.evaluate(_base_decision(), 100000, 100000, 100.0, set(), True)
    assert result.approved
    assert result.reasons == []
