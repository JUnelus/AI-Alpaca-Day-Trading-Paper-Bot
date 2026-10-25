import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.alpaca_client import AccountSnapshot, BrokerAsset
from src.execution_models import ExecutionResult
from src.main import ConfigurationError, EodCleanupError, apply_execution_to_available_cash, parse_args, run_once
from src.market_data import MarketDataResult
from src.portfolio import PortfolioState
from src.strategy import MarketSnapshot, StrategySignal


class DummyAlpacaClient:
    def __init__(self, execution_results=None, positions=None, account=None, account_snapshots=None, fail_on_place=False, paper=True, fractionable=True, eod_window="in_window", eod_results=None, positions_error=None):
        self.paper = paper
        self.fractionable = fractionable
        self.eod_window = eod_window
        self._eod_results = list(eod_results or [])
        self.positions_error = positions_error
        self.eod_calls = []
        self._execution_results = list(execution_results or [])
        self._positions = list(positions or [])
        self._account = account or AccountSnapshot(equity=10_000.0, cash=5_000.0, buying_power=5_000.0)
        self._account_snapshots = list(account_snapshots or [])
        self.fail_on_place = fail_on_place
        self.calls = []
        self.is_ready = True

    def get_account_snapshot(self):
        if self._account_snapshots:
            if len(self._account_snapshots) == 1:
                return self._account_snapshots[0]
            return self._account_snapshots.pop(0)
        return self._account

    def list_positions(self):
        return list(self._positions)

    def list_positions_strict(self):
        if self.positions_error is not None:
            raise self.positions_error
        return list(self._positions)

    def eod_cleanup_window(self):
        messages = {
            "in_window": None,
            "before_window": "200 minutes remain before the close, outside the 30-minute EOD cleanup window.",
            "closed": "The exchange is closed, so a DAY market SELL could not execute before this session's DAY stops expire.",
            "unavailable": "Alpaca market clock could not be read: clock down",
        }
        return {"state": self.eod_window, "minutes_to_close": None, "message": messages[self.eod_window]}

    def close_position_for_eod(self, symbol, qty, asset_type, current_position_qty):
        if self.fail_on_place:
            raise AssertionError("This run must never place an order.")
        self.eod_calls.append({"symbol": symbol, "qty": qty, "asset_type": asset_type, "current_position_qty": current_position_qty})
        if self._eod_results:
            return self._eod_results.pop(0)
        self._positions = [p for p in self._positions if getattr(p, "symbol", "") != symbol]
        return ExecutionResult(
            success=True,
            symbol=symbol,
            side="sell",
            requested_qty=qty,
            filled_qty=qty,
            filled_avg_price=100.0,
            entry_order_id=f"{symbol}-eod-sell",
            counts_as_trade=True,
            status="filled",
            message="SELL-to-close submitted after protective stop reconciliation.",
            asset_type=asset_type,
            cancelled_protective_order_ids=[f"{symbol}-day-stop"],
            actual_remaining_position_qty=0.0,
            protection_reconciled=True,
            eod_exit=True,
        )

    def get_position_qty(self, symbol: str):
        for position in self._positions:
            if getattr(position, "symbol", "") == symbol:
                return float(getattr(position, "qty", 0.0))
        return 0.0

    def get_asset(self, symbol: str):
        return BrokerAsset(symbol=symbol, tradable=True, fractionable=self.fractionable)

    def can_place_protected_buy(self, asset_type: str, allow_fractional: bool = False) -> bool:
        return asset_type in {"stock", "etf"}

    def place_paper_trade(self, **kwargs):
        if self.fail_on_place:
            raise AssertionError("Report mode must never place an order.")
        self.calls.append(kwargs)
        if self._execution_results:
            return self._execution_results.pop(0)

        side = kwargs["side"].lower()
        qty = kwargs["qty"]
        return ExecutionResult(
            success=True,
            symbol=kwargs["symbol"],
            side=side,
            requested_qty=qty,
            filled_qty=qty,
            filled_avg_price=100.0,
            entry_order_id=f"{kwargs['symbol']}-entry",
            protective_order_id=f"{kwargs['symbol']}-stop" if side == "buy" else None,
            protection_active=side == "buy",
            protection_failed=False,
            counts_as_trade=True,
            status="filled",
            message="executed",
            stop_price=kwargs.get("stop_loss"),
            asset_type=kwargs["asset_type"],
            order_class="oto" if side == "buy" else None,
        )


def _write_watchlist(path: Path, symbols: list[dict]) -> None:
    config = {
        "portfolio_size": 10_000,
        "max_position_pct": 10,
        "max_risk_percent": 1,
        "max_daily_loss_percent": 2,
        "max_daily_trades": 3,
        "max_total_exposure_percent": 80,
        "allow_margin": False,
        "allow_shorts": False,
        "min_confidence": 0.70,
        "symbols": symbols,
        "watchlist_universe": symbols,
        "last_watchlist_refresh_week": "2099-W01",
    }
    path.write_text(json.dumps(config, indent=2), encoding="utf-8")


def _prepare_paths(tmp_path: Path, symbols: list[dict]):
    watchlist_path = tmp_path / "watchlist.json"
    log_path = tmp_path / "trade_log.csv"
    summary_path = tmp_path / "daily_summary.md"
    readme_path = tmp_path / "README.md"
    state_path = tmp_path / "portfolio_state.json"

    _write_watchlist(watchlist_path, symbols)
    readme_path.write_text(
        "# Test README\n\n<!-- PORTFOLIO_DASHBOARD_START -->\nold\n<!-- PORTFOLIO_DASHBOARD_END -->\n",
        encoding="utf-8",
    )
    return watchlist_path, log_path, summary_path, readme_path, state_path


def _fresh_snapshot(symbol: str, day_change: float = -1.8, price: float = 100.0, source: str = "alpaca", is_fresh: bool = True, is_fallback: bool = False):
    return MarketSnapshot(
        symbol=symbol,
        last_price=price,
        day_change_percent=day_change,
        source=source,
        timestamp=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
        is_fresh=is_fresh,
        is_fallback=is_fallback,
    )


def test_apply_execution_to_available_cash_handles_buy_and_sell_correctly():
    buy_result = ExecutionResult(
        success=True,
        symbol="AAPL",
        side="buy",
        requested_qty=2.0,
        filled_qty=2.0,
        filled_avg_price=100.0,
        counts_as_trade=True,
        status="filled",
    )
    sell_result = ExecutionResult(
        success=True,
        symbol="AAPL",
        side="sell",
        requested_qty=2.0,
        filled_qty=2.0,
        filled_avg_price=100.0,
        counts_as_trade=True,
        status="filled",
    )

    assert apply_execution_to_available_cash(1_000.0, buy_result, 100.0) == 800.0
    assert apply_execution_to_available_cash(1_000.0, sell_result, 100.0) == 1_200.0


def test_trade_mode_can_reach_order_execution_layer(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    alpaca = DummyAlpacaClient()

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    result = run_once(
        mode="trade",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    assert result["mode"] == "trade"
    assert len(alpaca.calls) == 1
    assert result["results"][0]["order_result"]["counts_as_trade"]
    assert result["email_sent"]


def test_report_mode_cannot_place_orders_and_still_updates_reporting(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    alpaca = DummyAlpacaClient(fail_on_place=True)

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    run_once(
        mode="report",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    assert alpaca.calls == []
    assert summary_path.exists()
    assert "Live Portfolio Dashboard" in readme_path.read_text(encoding="utf-8")


def test_global_market_data_failure_places_zero_orders(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    alpaca = DummyAlpacaClient()

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL", source="unavailable", is_fresh=False), **_benchmarks()},
            service_available=False,
            used_fallback_data=False,
            message="service unavailable",
        ),
    )

    result = run_once(
        mode="trade",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    assert alpaca.calls == []
    assert not result["results"][0]["risk"]["approved"]
    assert any("fresh market data unavailable" in reason.lower() for reason in result["results"][0]["risk"]["reasons"])


def test_fallback_data_cannot_execute_trade_but_can_be_used_for_report_mode(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)

    fallback_result = MarketDataResult(
        snapshots={"AAPL": _fresh_snapshot("AAPL", source="fallback", is_fresh=False, is_fallback=True)},
        service_available=False,
        used_fallback_data=True,
        message="fallback in use",
    )
    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr("src.main.get_market_snapshots", lambda *args, **kwargs: fallback_result)

    trade_client = DummyAlpacaClient()
    trade_result = run_once(
        mode="trade",
        allow_fallback_data=True,
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
        alpaca_client=trade_client,
    )
    assert trade_client.calls == []
    assert trade_result["market_data"]["used_fallback_data"]

    report_client = DummyAlpacaClient(fail_on_place=True)
    report_result = run_once(
        mode="report",
        allow_fallback_data=True,
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
        alpaca_client=report_client,
    )
    assert report_client.calls == []
    assert report_result["market_data"]["used_fallback_data"]


def test_daily_loss_circuit_breaker_resets_on_new_trading_day(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    previous_state = PortfolioState(
        starting_balance=10_000.0,
        account_equity=9_700.0,
        cash=4_000.0,
        buying_power=4_000.0,
        total_pnl=-300.0,
        total_pnl_pct=-3.0,
        last_updated="2026-08-26T20:00:00+00:00",
        trading_day="2026-08-26",
        start_of_day_equity=10_000.0,
        daily_pnl=-300.0,
        daily_loss_limit=200.0,
        daily_loss_triggered=True,
        mode="trade",
    )
    previous_state.save(str(state_path))

    alpaca = DummyAlpacaClient(account=AccountSnapshot(equity=9_700.0, cash=4_000.0, buying_power=4_000.0))
    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    result = run_once(
        mode="report",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    assert result["portfolio"]["start_of_day_equity"] == 9_700.0
    assert result["portfolio"]["daily_pnl"] == 0.0
    assert not result["portfolio"]["daily_loss_triggered"]


def test_first_three_qualifying_trades_execute_and_fourth_is_rejected(monkeypatch, tmp_path):
    symbols = [
        {"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9},
        {"symbol": "MSFT", "name": "Microsoft", "type": "stock", "quality_score": 0.9},
        {"symbol": "NVDA", "name": "NVIDIA", "type": "stock", "quality_score": 0.9},
        {"symbol": "AMZN", "name": "Amazon", "type": "stock", "quality_score": 0.9},
        {"symbol": "META", "name": "Meta", "type": "stock", "quality_score": 0.9},
        {"symbol": "TSLA", "name": "Tesla", "type": "stock", "quality_score": 0.9},
    ]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    alpaca = DummyAlpacaClient()
    signal_map = {
        "AAPL": StrategySignal("AAPL", "buy", 0.95, "Buy 1"),
        "MSFT": StrategySignal("MSFT", "buy", 0.95, "Buy 2"),
        "NVDA": StrategySignal("NVDA", "buy", 0.95, "Buy 3"),
        "AMZN": StrategySignal("AMZN", "buy", 0.95, "Buy 4"),
        "META": StrategySignal("META", "hold", 0.55, "Hold"),
        "TSLA": StrategySignal("TSLA", "buy", 0.60, "Low confidence buy"),
    }

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr("src.main.generate_signal", lambda snapshot, sym_cfg, **kwargs: signal_map[snapshot.symbol])
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={**{str(symbol["symbol"]): _fresh_snapshot(str(symbol["symbol"])) for symbol in symbols}, **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    result = run_once(
        mode="trade",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    assert len(alpaca.calls) == 3
    assert result["portfolio"]["trades_today"] == 3
    fourth_result = next(item for item in result["results"] if item["symbol"] == "AMZN")
    assert not fourth_result["risk"]["approved"]
    assert any("daily trade limit" in reason.lower() for reason in fourth_result["risk"]["reasons"])


def test_successful_trade_and_failed_email_still_persists_state(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    alpaca = DummyAlpacaClient()

    monkeypatch.setenv("EMAIL_REQUIRED", "false")
    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    result = run_once(
        mode="trade",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    saved_state = PortfolioState.load(str(state_path))
    assert not result["email_sent"]
    assert saved_state.trades_today == 1
    assert summary_path.exists()
    assert readme_path.exists()
    assert log_path.exists()
    assert any("email delivery failed" in warning.lower() for warning in saved_state.warnings)


def test_email_required_failure_raises_after_state_is_persisted(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    alpaca = DummyAlpacaClient()

    monkeypatch.setenv("EMAIL_REQUIRED", "true")
    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    with pytest.raises(RuntimeError, match="Execution state was persisted"):
        run_once(
            mode="trade",
            watchlist_path=str(watchlist_path),
            log_path=str(log_path),
            summary_path=str(summary_path),
            readme_path=str(readme_path),
            state_path=str(state_path),
            now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
            alpaca_client=alpaca,
        )

    saved_state = PortfolioState.load(str(state_path))
    assert saved_state.trades_today == 1
    assert log_path.exists()
    assert summary_path.exists()
    assert readme_path.exists()
    assert any("email delivery failed" in warning.lower() for warning in saved_state.warnings)


def test_rerun_after_email_failure_reads_trade_log_and_blocks_duplicate_symbol(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    monkeypatch.setenv("EMAIL_REQUIRED", "true")
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: False)
    with pytest.raises(RuntimeError):
        run_once(
            mode="trade",
            watchlist_path=str(watchlist_path),
            log_path=str(log_path),
            summary_path=str(summary_path),
            readme_path=str(readme_path),
            state_path=str(state_path),
            now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
            alpaca_client=DummyAlpacaClient(),
        )

    second_client = DummyAlpacaClient()
    monkeypatch.setenv("EMAIL_REQUIRED", "false")
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    result = run_once(
        mode="trade",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 14, 5, tzinfo=timezone.utc),
        alpaca_client=second_client,
    )

    assert second_client.calls == []
    assert result["portfolio"]["trades_today"] == 1
    assert any("per symbol per day" in reason.lower() for reason in result["results"][0]["risk"]["reasons"])


def test_scheduled_trade_runs_once_per_eastern_day_but_manual_trade_is_still_allowed(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    first_client = DummyAlpacaClient()
    first = run_once(
        mode="trade",
        scheduled_run=True,
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 13, 45, tzinfo=timezone.utc),
        alpaca_client=first_client,
    )
    assert not first.get("scheduled_marker_skipped", False)
    assert len(first_client.calls) == 1
    assert PortfolioState.load(str(state_path)).last_scheduled_trade_day == "2026-08-27"

    second_client = DummyAlpacaClient()
    skipped = run_once(
        mode="trade",
        scheduled_run=True,
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 13, 50, tzinfo=timezone.utc),
        alpaca_client=second_client,
    )
    assert skipped["scheduled_marker_skipped"]
    assert second_client.calls == []

    manual_state_path = tmp_path / "manual_state.json"
    PortfolioState(last_scheduled_trade_day="2026-08-27").save(str(manual_state_path))
    manual_client = DummyAlpacaClient()
    manual = run_once(
        mode="trade",
        scheduled_run=False,
        watchlist_path=str(watchlist_path),
        log_path=str(tmp_path / "manual_trade_log.csv"),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(manual_state_path),
        now=datetime(2026, 8, 27, 13, 55, tzinfo=timezone.utc),
        alpaca_client=manual_client,
    )
    assert not manual.get("scheduled_marker_skipped", False)
    assert len(manual_client.calls) == 1


def test_scheduled_trade_runs_again_on_next_eastern_day(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    previous_state = PortfolioState(last_scheduled_trade_day="2026-08-27", trading_day="2026-08-27")
    previous_state.save(str(state_path))

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    client = DummyAlpacaClient()
    result = run_once(
        mode="trade",
        scheduled_run=True,
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 28, 13, 45, tzinfo=timezone.utc),
        alpaca_client=client,
    )

    assert not result.get("scheduled_marker_skipped", False)
    assert len(client.calls) == 1
    assert PortfolioState.load(str(state_path)).last_scheduled_trade_day == "2026-08-28"


def test_scheduled_report_runs_once_per_eastern_day(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    first = run_once(
        mode="report",
        scheduled_run=True,
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 20, 15, tzinfo=timezone.utc),
        alpaca_client=DummyAlpacaClient(),
    )
    assert not first.get("scheduled_marker_skipped", False)
    assert PortfolioState.load(str(state_path)).last_scheduled_report_day == "2026-08-27"

    second = run_once(
        mode="report",
        scheduled_run=True,
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 20, 20, tzinfo=timezone.utc),
        alpaca_client=DummyAlpacaClient(),
    )
    assert second["scheduled_marker_skipped"]


def test_daily_pnl_uses_final_authoritative_equity(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    alpaca = DummyAlpacaClient(
        account_snapshots=[
            AccountSnapshot(equity=10_000.0, cash=5_000.0, buying_power=5_000.0),
            AccountSnapshot(equity=9_850.0, cash=4_850.0, buying_power=4_850.0),
        ],
        positions=[SimpleNamespace(symbol="AAPL", qty="1", avg_entry_price="100", current_price="100", market_value="100", cost_basis="100", unrealized_pl="0", unrealized_plpc="0")],
    )

    result = run_once(
        mode="report",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 20, 15, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    assert result["portfolio"]["start_of_day_equity"] == 10_000.0
    assert result["portfolio"]["account_equity"] == 9_850.0
    assert result["portfolio"]["daily_pnl"] == -150.0
    assert not result["portfolio"]["daily_loss_triggered"]


def test_daily_loss_circuit_breaker_uses_final_equity_value(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    alpaca = DummyAlpacaClient(
        account_snapshots=[
            AccountSnapshot(equity=10_000.0, cash=5_000.0, buying_power=5_000.0),
            AccountSnapshot(equity=9_800.0, cash=4_800.0, buying_power=4_800.0),
        ],
    )

    result = run_once(
        mode="report",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 27, 20, 15, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    assert result["portfolio"]["daily_pnl"] == -200.0
    assert result["portfolio"]["daily_loss_triggered"]


def test_same_eastern_day_report_does_not_reset_start_of_day_equity(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    previous_state = PortfolioState(
        trading_day="2026-08-27",
        start_of_day_equity=10_000.0,
        account_equity=9_900.0,
        daily_pnl=-100.0,
        daily_loss_limit=200.0,
    )
    previous_state.save(str(state_path))

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    alpaca = DummyAlpacaClient(
        account_snapshots=[
            AccountSnapshot(equity=9_950.0, cash=4_950.0, buying_power=4_950.0),
            AccountSnapshot(equity=9_900.0, cash=4_900.0, buying_power=4_900.0),
        ]
    )
    result = run_once(
        mode="report",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 28, 0, 30, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    assert result["portfolio"]["trading_day"] == "2026-08-27"
    assert result["portfolio"]["start_of_day_equity"] == 10_000.0
    assert result["portfolio"]["daily_pnl"] == -100.0


def test_new_eastern_day_resets_start_of_day_equity(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    previous_state = PortfolioState(
        trading_day="2026-08-27",
        start_of_day_equity=10_000.0,
        account_equity=9_900.0,
        daily_pnl=-100.0,
        daily_loss_limit=200.0,
    )
    previous_state.save(str(state_path))

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL"), **_benchmarks()},
            service_available=True,
            used_fallback_data=False,
        ),
    )

    alpaca = DummyAlpacaClient(
        account_snapshots=[
            AccountSnapshot(equity=9_920.0, cash=4_920.0, buying_power=4_920.0),
            AccountSnapshot(equity=9_910.0, cash=4_910.0, buying_power=4_910.0),
        ]
    )
    result = run_once(
        mode="report",
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=datetime(2026, 8, 28, 5, 0, tzinfo=timezone.utc),
        alpaca_client=alpaca,
    )

    assert result["portfolio"]["trading_day"] == "2026-08-28"
    assert result["portfolio"]["start_of_day_equity"] == 9_920.0
    assert result["portfolio"]["daily_pnl"] == -10.0


def test_invalid_trade_startup_configuration_raises_before_order_placement(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    config = json.loads(watchlist_path.read_text(encoding="utf-8"))
    config["allow_margin"] = True
    watchlist_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    client = DummyAlpacaClient()

    with pytest.raises(ConfigurationError, match="ALLOW_MARGIN"):
        run_once(
            mode="trade",
            watchlist_path=str(watchlist_path),
            log_path=str(log_path),
            summary_path=str(summary_path),
            readme_path=str(readme_path),
            state_path=str(state_path),
            now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc),
            alpaca_client=client,
        )

    assert client.calls == []


def _benchmarks() -> dict:
    """Fresh, flat SPY/QQQ snapshots: the market filter fails closed without them, so trade stubs include them."""
    return {symbol: _fresh_snapshot(symbol, day_change=0.0) for symbol in ("SPY", "QQQ")}


# ── end-of-day fractional cleanup ─────────────────────────────────────────────

def _position(symbol, qty, side="long", price=100.0):
    return SimpleNamespace(symbol=symbol, qty=str(qty), side=side, current_price=price, market_value=qty * price, avg_entry_price=price, cost_basis=qty * price, unrealized_pl=0.0, unrealized_plpc=0.0)


_EOD_SYMBOLS = [
    {"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9},
    {"symbol": "MSFT", "name": "Microsoft", "type": "stock", "quality_score": 0.9},
    {"symbol": "BTC/USD", "name": "Bitcoin", "type": "crypto", "quality_score": 0.9},
]
_EOD_NOW = datetime(2026, 8, 27, 19, 40, tzinfo=timezone.utc)  # 15:40 New York


def _eod_positions():
    return [_position("AAPL", 0.0288), _position("MSFT", 1.0), _position("BTC/USD", 0.01), _position("SPY", 0.5, side="short")]


def _run_eod(alpaca, paths, scheduled_run=True, now=_EOD_NOW):
    watchlist_path, log_path, summary_path, readme_path, state_path = paths
    return run_once(
        mode="eod",
        scheduled_run=scheduled_run,
        watchlist_path=str(watchlist_path),
        log_path=str(log_path),
        summary_path=str(summary_path),
        readme_path=str(readme_path),
        state_path=str(state_path),
        now=now,
        alpaca_client=alpaca,
    )


def test_eod_mode_sells_only_long_fractional_equity_positions(monkeypatch, tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    watchlist_path, log_path, summary_path, readme_path, state_path = paths
    alpaca = DummyAlpacaClient(positions=_eod_positions())
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("eod mode must not email")))

    result = _run_eod(alpaca, paths)

    assert result["mode"] == "eod"
    assert [call["symbol"] for call in alpaca.eod_calls] == ["AAPL"]
    assert alpaca.eod_calls[0] == {"symbol": "AAPL", "qty": 0.0288, "asset_type": "stock", "current_position_qty": 0.0288}
    assert alpaca.calls == []  # never routed through the strategy order path
    assert result["results"][0]["order_result"]["eod_exit"]
    assert result["email_sent"] is False

    state = PortfolioState.load(str(state_path))
    assert state.mode == "eod"
    assert state.last_scheduled_eod_day == "2026-08-27"
    assert state.eod_cleanup_warnings == []
    assert state.trades_today == 1
    assert state.traded_symbols_today == ["AAPL"]
    assert [p.symbol for p in state.positions] == ["MSFT", "BTC/USD", "SPY"]

    log_rows = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(log_rows) == 1
    assert ",AAPL,sell," in log_rows[0]
    assert "AAPL-eod-sell" in log_rows[0]
    summary = summary_path.read_text(encoding="utf-8")
    assert "Run mode: `eod`" in summary
    assert "EOD Cleanup Exits" in summary
    assert "**AAPL** — SELL" in summary and "✅ EXECUTED" in summary
    assert "**AAPL** | SELL" in readme_path.read_text(encoding="utf-8")


def test_eod_mode_with_nothing_fractional_is_a_clean_run(tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    alpaca = DummyAlpacaClient(positions=[_position("MSFT", 2.0), _position("BTC/USD", 0.5)])

    result = _run_eod(alpaca, paths)

    assert result["results"] == []
    assert alpaca.eod_calls == []
    assert "No fractional stock/ETF positions needed an end-of-day exit." in paths[2].read_text(encoding="utf-8")
    assert PortfolioState.load(str(paths[4])).last_scheduled_eod_day == "2026-08-27"


def test_eod_mode_before_window_is_a_noop_that_leaves_no_marker(tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    alpaca = DummyAlpacaClient(positions=_eod_positions(), eod_window="before_window")

    result = _run_eod(alpaca, paths)

    assert result["scheduled_marker_skipped"]
    assert "outside the 30-minute EOD cleanup window" in result["reason"]
    assert alpaca.eod_calls == []
    assert not paths[4].exists()  # nothing persisted, so the in-window run later today still acts


@pytest.mark.parametrize("window", ["closed", "unavailable"])
def test_eod_mode_refuses_to_sell_when_the_session_is_closed_or_the_clock_is_unusable(tmp_path, window):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    alpaca = DummyAlpacaClient(positions=_eod_positions(), eod_window=window, fail_on_place=True)

    with pytest.raises(EodCleanupError, match="unresolved"):
        _run_eod(alpaca, paths)

    state = PortfolioState.load(str(paths[4]))
    assert state.last_scheduled_eod_day == ""  # a failed cleanup stays retryable
    assert len(state.eod_cleanup_warnings) == 1
    assert "EOD cleanup failed for AAPL" in state.eod_cleanup_warnings[0]
    assert state.eod_cleanup_warnings[0] in state.warnings
    log_rows = paths[1].read_text(encoding="utf-8").strip().splitlines()
    assert len(log_rows) == 1 and "eod_exit_blocked" in log_rows[0]


def test_eod_mode_without_fractional_positions_tolerates_a_closed_session(tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    alpaca = DummyAlpacaClient(positions=[_position("MSFT", 2.0)], eod_window="closed")

    result = _run_eod(alpaca, paths)

    assert result["results"] == []
    assert PortfolioState.load(str(paths[4])).eod_cleanup_warnings == []


def test_eod_mode_exit_failure_raises_after_persisting_state_and_log(tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    failure = ExecutionResult(
        success=False, symbol="AAPL", side="sell", requested_qty=0.0288, status="critical_unprotected_position",
        message="CRITICAL: EOD SELL for AAPL did not reach a terminal state after cancellation.", asset_type="stock", protection_failed=True, eod_exit=True,
    )
    alpaca = DummyAlpacaClient(positions=_eod_positions(), eod_results=[failure])

    with pytest.raises(EodCleanupError, match="AAPL"):
        _run_eod(alpaca, paths)

    state = PortfolioState.load(str(paths[4]))
    assert state.mode == "eod"
    assert state.last_scheduled_eod_day == ""
    assert any("did not reach a terminal state" in w for w in state.warnings)
    assert "critical_unprotected_position" in paths[1].read_text(encoding="utf-8")
    assert "⚠️ PROTECTION FAILED" in paths[2].read_text(encoding="utf-8")

    # A scheduled retry the same day is still allowed and can finish the job.
    retry = DummyAlpacaClient(positions=_eod_positions())
    _run_eod(retry, paths, now=_EOD_NOW + timedelta(minutes=3))
    assert len(retry.eod_calls) == 1
    retried_state = PortfolioState.load(str(paths[4]))
    assert retried_state.last_scheduled_eod_day == "2026-08-27"
    assert retried_state.eod_cleanup_warnings == []


def test_eod_mode_position_listing_failure_raises_instead_of_reading_flat(tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    alpaca = DummyAlpacaClient(positions=_eod_positions(), positions_error=RuntimeError("positions endpoint down"))

    with pytest.raises(RuntimeError, match="positions endpoint down"):
        _run_eod(alpaca, paths)

    assert alpaca.eod_calls == []


def test_eod_mode_requires_a_ready_paper_client(tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    alpaca = DummyAlpacaClient(positions=_eod_positions())
    alpaca.is_ready = False

    with pytest.raises(EodCleanupError, match="credentials"):
        _run_eod(alpaca, paths)
    assert alpaca.eod_calls == []

    with pytest.raises(ConfigurationError):
        _run_eod(DummyAlpacaClient(positions=_eod_positions(), paper=False), paths)


def test_scheduled_eod_runs_once_per_eastern_day_but_manual_rerun_is_allowed(tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    first = DummyAlpacaClient(positions=_eod_positions())
    _run_eod(first, paths)
    assert len(first.eod_calls) == 1

    second = DummyAlpacaClient(positions=_eod_positions())
    rerun = _run_eod(second, paths, now=_EOD_NOW + timedelta(minutes=5))
    assert rerun["scheduled_marker_skipped"]
    assert second.eod_calls == []

    manual = DummyAlpacaClient(positions=_eod_positions())
    _run_eod(manual, paths, scheduled_run=False, now=_EOD_NOW + timedelta(minutes=6))
    assert len(manual.eod_calls) == 1

    next_day = DummyAlpacaClient(positions=_eod_positions())
    _run_eod(next_day, paths, now=_EOD_NOW + timedelta(days=1))
    assert len(next_day.eod_calls) == 1


def test_eod_cleanup_warnings_surface_on_same_day_report_and_expire_next_day(monkeypatch, tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    watchlist_path, log_path, summary_path, readme_path, state_path = paths
    alpaca = DummyAlpacaClient(positions=_eod_positions(), eod_window="closed")
    with pytest.raises(EodCleanupError):
        _run_eod(alpaca, paths)

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(snapshots={**{s["symbol"]: _fresh_snapshot(s["symbol"]) for s in _EOD_SYMBOLS}, **_benchmarks()}, service_available=True, used_fallback_data=False),
    )

    def report(now):
        return run_once(
            mode="report", scheduled_run=True, watchlist_path=str(watchlist_path), log_path=str(log_path), summary_path=str(summary_path),
            readme_path=str(readme_path), state_path=str(state_path), now=now, alpaca_client=DummyAlpacaClient(positions=_eod_positions(), fail_on_place=True),
        )

    same_day = report(_EOD_NOW + timedelta(minutes=35))
    assert any("EOD cleanup failed for AAPL" in w for w in same_day["portfolio"]["warnings"])
    assert PortfolioState.load(str(state_path)).last_scheduled_eod_day == ""

    next_day = report(_EOD_NOW + timedelta(days=1))
    assert not any("EOD cleanup failed" in w for w in next_day["portfolio"]["warnings"])
    assert PortfolioState.load(str(state_path)).eod_cleanup_warnings == []


def test_parse_args_accepts_eod_mode():
    args = parse_args(["--mode", "eod", "--scheduled-run"])
    assert args.mode == "eod"
    assert args.scheduled_run
    with pytest.raises(SystemExit):
        parse_args(["--mode", "cleanup"])


def test_eod_mode_uses_broker_asset_class_before_symbol_heuristics(tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    doge = _position("DOGEUSD", 12.5)
    doge.asset_class = "crypto"
    unlisted_equity = _position("NVDA", 0.25)
    unlisted_equity.asset_class = SimpleNamespace(value="us_equity")
    alpaca = DummyAlpacaClient(positions=[doge, unlisted_equity, _position("AAPL", 0.0288)])

    _run_eod(alpaca, paths)

    assert sorted(call["symbol"] for call in alpaca.eod_calls) == ["AAPL", "NVDA"]


def test_eod_mode_persists_failures_even_when_the_account_refresh_breaks(tmp_path):
    paths = _prepare_paths(tmp_path, _EOD_SYMBOLS)
    failure = ExecutionResult(success=False, symbol="AAPL", side="sell", requested_qty=0.0288, status="critical_unprotected_position", message="CRITICAL: ambiguous", asset_type="stock", protection_failed=True, eod_exit=True)
    alpaca = DummyAlpacaClient(positions=_eod_positions(), eod_results=[failure])
    alpaca.get_account_snapshot = lambda: (_ for _ in ()).throw(RuntimeError("account endpoint down"))

    with pytest.raises(EodCleanupError, match="ambiguous"):
        _run_eod(alpaca, paths)

    state = PortfolioState.load(str(paths[4]))
    assert any("ambiguous" in w for w in state.eod_cleanup_warnings)
    assert any("account endpoint down" in w for w in state.eod_cleanup_warnings)
    assert state.last_scheduled_eod_day == ""


def test_sell_of_a_fractional_holding_is_sized_to_the_holding_above_the_threshold(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    # Equity far above the fractional threshold: new BUYs would be whole-share only.
    alpaca = DummyAlpacaClient(positions=[_position("AAPL", 0.0288, price=347.0)], account=AccountSnapshot(equity=100_000.0, cash=90_000.0, buying_power=90_000.0))

    monkeypatch.setenv("PORTFOLIO_SIZE", "100")  # $10 per-symbol cap: whole-share sizing floors to zero
    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr("src.main.get_market_snapshots", lambda *args, **kwargs: MarketDataResult(snapshots={"AAPL": _fresh_snapshot("AAPL", day_change=3.0, price=347.0), **_benchmarks()}, service_available=True, used_fallback_data=False))
    monkeypatch.setattr("src.main.generate_signal", lambda snapshot, cfg, market_context=None: StrategySignal(symbol="AAPL", action="sell", strength=0.9, reason="take profit"))

    result = run_once(mode="trade", watchlist_path=str(watchlist_path), log_path=str(log_path), summary_path=str(summary_path), readme_path=str(readme_path), state_path=str(state_path), now=datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc), alpaca_client=alpaca)

    assert len(alpaca.calls) == 1
    assert alpaca.calls[0]["side"] == "sell"
    assert alpaca.calls[0]["qty"] == 0.0288
    assert result["results"][0]["decision"]["requested_qty"] == 0.0288
