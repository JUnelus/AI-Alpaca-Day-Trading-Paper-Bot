import json
from datetime import datetime, timezone
from pathlib import Path

from src.alpaca_client import AccountSnapshot
from src.execution_models import ExecutionResult
from src.main import apply_execution_to_available_cash, run_once
from src.market_data import MarketDataResult
from src.portfolio import PortfolioState
from src.strategy import MarketSnapshot, StrategySignal


class DummyAlpacaClient:
    def __init__(self, execution_results=None, positions=None, account=None, fail_on_place=False):
        self.paper = True
        self._execution_results = list(execution_results or [])
        self._positions = list(positions or [])
        self._account = account or AccountSnapshot(equity=10_000.0, cash=5_000.0, buying_power=5_000.0)
        self.fail_on_place = fail_on_place
        self.calls = []
        self.is_ready = True

    def get_account_snapshot(self):
        return self._account

    def list_positions(self):
        return list(self._positions)

    def can_place_protected_buy(self, asset_type: str) -> bool:
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
            snapshots={"AAPL": _fresh_snapshot("AAPL")},
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


def test_report_mode_cannot_place_orders_and_still_updates_reporting(monkeypatch, tmp_path):
    symbols = [{"symbol": "AAPL", "name": "Apple", "type": "stock", "quality_score": 0.9}]
    watchlist_path, log_path, summary_path, readme_path, state_path = _prepare_paths(tmp_path, symbols)
    alpaca = DummyAlpacaClient(fail_on_place=True)

    monkeypatch.setattr("src.main.refresh_weekly_watchlist", lambda *args, **kwargs: False)
    monkeypatch.setattr("src.main.send_daily_report", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={"AAPL": _fresh_snapshot("AAPL")},
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
            snapshots={"AAPL": _fresh_snapshot("AAPL", source="unavailable", is_fresh=False)},
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
            snapshots={"AAPL": _fresh_snapshot("AAPL")},
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
    monkeypatch.setattr("src.main.generate_signal", lambda snapshot, sym_cfg: signal_map[snapshot.symbol])
    monkeypatch.setattr(
        "src.main.get_market_snapshots",
        lambda *args, **kwargs: MarketDataResult(
            snapshots={str(symbol["symbol"]): _fresh_snapshot(str(symbol["symbol"])) for symbol in symbols},
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



