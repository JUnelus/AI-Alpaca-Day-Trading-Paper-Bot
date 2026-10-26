from src.risk_manager import (
    RiskConfig,
    RiskEvaluationContext,
    RiskManager,
    allows_fractional_equity_orders,
    normalize_qty_for_asset,
    qty_for_notional,
    uses_fractional_quantity,
    validate_trade_startup_config,
)


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




# ── fractional equity sizing ──────────────────────────────────────────────────


def _small_budget_config() -> RiskConfig:
    # Mirrors the live bot's ~$100 strategy capital: $10 per-symbol cap, $80 gross exposure cap.
    return RiskConfig(
        portfolio_size=100,
        max_position_percent=10,
        max_daily_loss_percent=2,
        max_daily_trades=3,
        max_total_exposure_percent=80,
        allow_margin=False,
        allow_shorts=False,
        min_confidence=0.70,
        max_risk_percent=1.0,
    )


def _small_budget_context(**overrides) -> RiskEvaluationContext:
    values = {
        "entry_price": 347.0,
        "account_equity": 200.0,
        "actual_available_cash": 100.0,
        "remaining_portfolio_capacity": 100.0,
    }
    values.update(overrides)
    return _context(**values)


def test_fractional_buy_sizes_below_one_share_when_equity_is_under_threshold():
    manager = RiskManager(config=_small_budget_config())
    allow_fractional = allows_fractional_equity_orders(200.0, "stock", True, manager.config.fractional_equity_threshold)
    assert allow_fractional is True

    result = manager.evaluate(
        _decision(qty=0.0288, stop_loss=340.0),
        _small_budget_context(symbol_fractionable=True, allow_fractional=allow_fractional),
    )

    assert result.approved, result.reasons
    # $10 position cap / $347 share price = 0.02881..., floored to 4 decimal places.
    assert result.adjusted_qty == 0.0288
    assert result.adjusted_qty * 347.0 <= 10.0


def test_fractional_buy_is_resized_down_to_the_position_cap():
    manager = RiskManager(config=_small_budget_config())
    result = manager.evaluate(
        _decision(qty=1.0, stop_loss=340.0),
        _small_budget_context(symbol_fractionable=True, allow_fractional=True),
    )
    assert result.approved, result.reasons
    assert result.adjusted_qty == 0.0288
    assert any("resized buy quantity" in note.lower() for note in result.notes)


def test_whole_share_flooring_is_kept_when_equity_is_over_threshold():
    threshold = RiskConfig().fractional_equity_threshold
    assert allows_fractional_equity_orders(25_000.0, "stock", True, threshold) is False
    assert normalize_qty_for_asset("stock", 2.9) == 2.0
    assert qty_for_notional("stock", 347.0, 1_000.0) == 2.0

    manager = RiskManager(config=_config())
    result = manager.evaluate(
        _decision(qty=3.7, stop_loss=340.0),
        _context(entry_price=347.0, account_equity=25_000.0, symbol_fractionable=True, allow_fractional=False),
    )
    assert result.approved, result.reasons
    assert result.adjusted_qty == 2.0


def test_small_budget_without_fractional_allowance_cannot_buy_expensive_stock():
    # Over the threshold (or asset not fractionable) a $10 cap on a $347 stock floors to zero shares.
    manager = RiskManager(config=_small_budget_config())
    result = manager.evaluate(
        _decision(qty=0.0288, stop_loss=340.0),
        _small_budget_context(symbol_fractionable=True, allow_fractional=False),
    )
    assert not result.approved
    assert any("quantity must be positive" in reason.lower() for reason in result.reasons)


def test_fractional_buy_requires_broker_fractionable_asset():
    manager = RiskManager(config=_small_budget_config())
    result = manager.evaluate(
        _decision(qty=0.0288, stop_loss=340.0),
        _small_budget_context(symbol_fractionable=False, allow_fractional=True),
    )
    assert not result.approved
    assert any("fractional-share execution" in reason.lower() for reason in result.reasons)


def test_crypto_sizing_is_unchanged_by_fractional_equity_policy():
    threshold = RiskConfig().fractional_equity_threshold
    assert allows_fractional_equity_orders(100_000.0, "crypto", False, threshold) is True
    assert normalize_qty_for_asset("crypto", 0.123456) == 0.1234
    assert normalize_qty_for_asset("crypto", 0.123456, allow_fractional=True) == 0.1234
    assert qty_for_notional("crypto", 60_000.0, 10.0) == 0.0001
    assert uses_fractional_quantity("crypto", 2.0) is True
    assert uses_fractional_quantity("stock", 2.0) is False
    assert uses_fractional_quantity("etf", 0.5) is True

    manager = RiskManager(config=_small_budget_config())
    result = manager.evaluate(
        _decision(symbol="BTC/USD", qty=0.0001, stop_loss=59_000.0),
        _small_budget_context(asset_type="crypto", entry_price=60_000.0, allow_fractional=False),
    )
    assert result.approved, result.reasons
    assert result.adjusted_qty == 0.0001


def test_fractional_equity_policy_uses_configured_threshold():
    threshold = 20_000.0
    assert allows_fractional_equity_orders(100.0, "stock", True, threshold) is True
    assert allows_fractional_equity_orders(19_999.99, "etf", True, threshold) is True
    assert allows_fractional_equity_orders(20_000.0, "stock", True, threshold) is False
    assert allows_fractional_equity_orders(100.0, "stock", False, threshold) is False
    assert allows_fractional_equity_orders(100.0, "option", True, threshold) is False


def test_fractional_position_can_still_be_sold_to_close():
    manager = RiskManager(config=_small_budget_config())
    context = _small_budget_context(
        current_position_qty=0.0288,
        current_position_market_value=10.0,
        symbol_fractionable=True,
        allow_fractional=True,
    )

    exact = manager.evaluate(_decision(action="sell", qty=0.0288, stop_loss=None), context)
    assert exact.approved, exact.reasons
    assert exact.adjusted_qty == 0.0288

    oversized = manager.evaluate(_decision(action="sell", qty=1.0, stop_loss=None), context)
    assert oversized.approved, oversized.reasons
    assert oversized.adjusted_qty == 0.0288
    assert any("resized sell quantity" in note.lower() for note in oversized.notes)


def test_fractional_equity_threshold_is_read_from_env_and_config(monkeypatch):
    monkeypatch.delenv("FRACTIONAL_EQUITY_THRESHOLD", raising=False)
    assert RiskConfig.from_sources({}).fractional_equity_threshold == 20_000.0
    assert RiskConfig.from_sources({"fractional_equity_threshold": 500}).fractional_equity_threshold == 500.0

    monkeypatch.setenv("FRACTIONAL_EQUITY_THRESHOLD", "1500")
    assert RiskConfig.from_sources({"fractional_equity_threshold": 500}).fractional_equity_threshold == 1_500.0

    errors = validate_trade_startup_config(RiskConfig(fractional_equity_threshold=-1), paper_trading=True)
    assert any("FRACTIONAL_EQUITY_THRESHOLD" in error for error in errors)
    assert validate_trade_startup_config(RiskConfig(fractional_equity_threshold=0), paper_trading=True) == []
