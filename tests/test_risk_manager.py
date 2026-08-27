from src.risk_manager import RiskConfig, RiskEvaluationContext, RiskManager, validate_trade_startup_config


def _config() -> RiskConfig:
    return RiskConfig(
        portfolio_size=10_000,
        max_position_percent=10,
        max_daily_loss_percent=2,
        max_daily_trades=3,
        max_total_exposure_percent=80,
        allow_margin=False,
        allow_shorts=False,
        min_confidence=0.70,
        max_risk_percent=1.0,
    )


def _decision(**overrides) -> dict:
    decision = {
        "symbol": "AAPL",
        "action": "buy",
        "confidence": 0.90,
        "reason": "DCA buy: quality asset on a deep pullback",
        "max_risk_percent": 1.0,
        "qty": 2.0,
        "stop_loss": 99.0,
    }
    decision.update(overrides)
    return decision


def _context(**overrides) -> RiskEvaluationContext:
    context = RiskEvaluationContext(
        mode="trade",
        asset_type="stock",
        entry_price=100.0,
        account_equity=10_000.0,
        actual_available_cash=5_000.0,
        remaining_portfolio_capacity=5_000.0,
        current_position_qty=0.0,
        current_position_market_value=0.0,
        current_gross_exposure=0.0,
        traded_symbols_today=set(),
        daily_trade_count=0,
        paper_trading=True,
        market_data_is_fresh=True,
        market_data_source="alpaca",
        market_data_service_available=True,
        daily_loss_triggered=False,
        protective_stop_supported=True,
    )
    for key, value in overrides.items():
        setattr(context, key, value)
    return context


def test_reject_low_confidence():
    manager = RiskManager(config=_config())
    result = manager.evaluate(_decision(confidence=0.69), _context())
    assert not result.approved
    assert any("confidence" in reason.lower() for reason in result.reasons)


def test_reject_second_trade_same_symbol_same_day():
    manager = RiskManager(config=_config())
    result = manager.evaluate(_decision(), _context(traded_symbols_today={"AAPL"}))
    assert not result.approved
    assert any("per symbol per day" in reason.lower() for reason in result.reasons)


def test_reject_if_not_paper_trading():
    manager = RiskManager(config=_config())
    result = manager.evaluate(_decision(), _context(paper_trading=False))
    assert not result.approved
    assert any("paper trading" in reason.lower() for reason in result.reasons)


def test_reject_without_stop_loss_for_buy():
    manager = RiskManager(config=_config())
    result = manager.evaluate(_decision(stop_loss=None), _context())
    assert not result.approved
    assert any("stop loss" in reason.lower() for reason in result.reasons)


def test_approve_valid_trade():
    manager = RiskManager(config=_config())
    result = manager.evaluate(_decision(), _context())
    assert result.approved
    assert result.adjusted_qty == 2.0
    assert result.reasons == []


def test_existing_900_position_resizes_new_buy_to_remaining_capacity():
    manager = RiskManager(config=_config())
    result = manager.evaluate(
        _decision(qty=2.0),
        _context(current_position_market_value=900.0),
    )
    assert result.approved
    assert result.adjusted_qty == 1.0
    assert any("resized buy quantity" in note.lower() for note in result.notes)


def test_existing_1000_position_blocks_another_buy():
    manager = RiskManager(config=_config())
    result = manager.evaluate(
        _decision(qty=1.0),
        _context(current_position_market_value=1_000.0),
    )
    assert not result.approved
    assert any("max-position limit" in reason.lower() for reason in result.reasons)


def test_new_buy_below_total_exposure_limit_passes():
    manager = RiskManager(config=_config())
    result = manager.evaluate(_decision(qty=2.0), _context(current_gross_exposure=7_700.0))
    assert result.approved
    assert result.adjusted_qty == 2.0


def test_new_buy_that_pushes_exposure_above_limit_is_resized():
    manager = RiskManager(config=_config())
    result = manager.evaluate(_decision(qty=3.0), _context(current_gross_exposure=7_800.0))
    assert result.approved
    assert result.adjusted_qty == 2.0
    assert any("resized buy quantity" in note.lower() for note in result.notes)


def test_existing_exposure_above_limit_blocks_new_buys():
    manager = RiskManager(config=_config())
    result = manager.evaluate(_decision(qty=1.0), _context(current_gross_exposure=8_100.0))
    assert not result.approved
    assert any("max-total-exposure limit" in reason.lower() for reason in result.reasons)


def test_existing_exposure_above_limit_still_permits_sell_to_close():
    manager = RiskManager(config=_config())
    result = manager.evaluate(
        _decision(action="sell", qty=3.0, stop_loss=None),
        _context(
            current_position_qty=5.0,
            current_position_market_value=1_200.0,
            current_gross_exposure=8_500.0,
            actual_available_cash=0.0,
            daily_loss_triggered=True,
        ),
    )
    assert result.approved
    assert result.adjusted_qty == 3.0


def test_sell_is_not_rejected_due_to_insufficient_cash():
    manager = RiskManager(config=_config())
    result = manager.evaluate(
        _decision(action="sell", qty=2.0, stop_loss=None),
        _context(current_position_qty=4.0, actual_available_cash=0.0),
    )
    assert result.approved
    assert not any("cash" in reason.lower() for reason in result.reasons)


def test_sell_cannot_exceed_held_quantity_when_shorts_disabled():
    manager = RiskManager(config=_config())
    result = manager.evaluate(
        _decision(action="sell", qty=9.0, stop_loss=None),
        _context(current_position_qty=4.0),
    )
    assert result.approved
    assert result.adjusted_qty == 4.0
    assert any("cannot open or increase a short" in note.lower() for note in result.notes)


def test_daily_trade_limit_blocks_fourth_trade():
    manager = RiskManager(config=_config())
    result = manager.evaluate(_decision(), _context(daily_trade_count=3))
    assert not result.approved
    assert any("daily trade limit" in reason.lower() for reason in result.reasons)


def test_daily_loss_circuit_breaker_blocks_buy_but_not_sell():
    manager = RiskManager(config=_config())
    buy_result = manager.evaluate(_decision(), _context(daily_loss_triggered=True))
    sell_result = manager.evaluate(
        _decision(action="sell", qty=1.0, stop_loss=None),
        _context(daily_loss_triggered=True, current_position_qty=2.0),
    )
    assert not buy_result.approved
    assert any("daily loss circuit breaker" in reason.lower() for reason in buy_result.reasons)
    assert sell_result.approved


def test_margin_cannot_exceed_remaining_portfolio_capacity():
    manager = RiskManager(config=_config())
    result = manager.evaluate(
        _decision(qty=2.0),
        _context(actual_available_cash=5_000.0, remaining_portfolio_capacity=150.0),
    )
    assert result.approved
    assert result.adjusted_qty == 1.0


def test_risk_uses_configured_portfolio_size_when_account_equity_is_larger():
    manager = RiskManager(config=_config())
    result = manager.evaluate(
        _decision(qty=30.0, stop_loss=5.0),
        _context(account_equity=108_000.0, entry_price=10.0),
    )
    assert result.approved
    assert result.adjusted_qty == 20.0


def test_risk_uses_lower_account_equity_when_equity_falls_below_portfolio_size():
    manager = RiskManager(config=_config())
    result = manager.evaluate(
        _decision(qty=30.0, stop_loss=5.0),
        _context(account_equity=8_000.0, entry_price=10.0),
    )
    assert result.approved
    assert result.adjusted_qty == 16.0


def test_validate_trade_startup_config_rejects_unsafe_settings():
    config = RiskConfig(
        portfolio_size=0,
        max_position_percent=120,
        max_daily_loss_percent=0,
        max_daily_trades=0,
        max_total_exposure_percent=5,
        allow_margin=True,
        allow_shorts=True,
        min_confidence=1.5,
        max_risk_percent=0,
    )

    errors = validate_trade_startup_config(config, paper_trading=False)

    assert any("ALPACA_PAPER" in error for error in errors)
    assert any("ALLOW_MARGIN" in error for error in errors)
    assert any("ALLOW_SHORTS" in error for error in errors)
    assert any("PORTFOLIO_SIZE" in error for error in errors)
    assert any("MAX_POSITION_PERCENT" in error for error in errors)
    assert any("MAX_TOTAL_EXPOSURE_PERCENT" in error for error in errors)
    assert any("MAX_DAILY_TRADES" in error for error in errors)
    assert any("MAX_DAILY_LOSS_PERCENT" in error for error in errors)
    assert any("MAX_RISK_PERCENT" in error for error in errors)
    assert any("MIN_CONFIDENCE" in error for error in errors)


