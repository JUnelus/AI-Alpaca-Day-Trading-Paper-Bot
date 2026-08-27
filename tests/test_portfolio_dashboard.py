from types import SimpleNamespace

from src.alpaca_client import AccountSnapshot
from src.dashboard import generate_dashboard
from src.portfolio import PortfolioState, refresh_from_alpaca


class PortfolioClientStub:
    def __init__(self, account, positions):
        self._account = account
        self._positions = list(positions)

    def get_account_snapshot(self):
        return self._account

    def list_positions(self):
        return list(self._positions)


def test_refresh_from_alpaca_uses_valid_broker_crypto_fields():
    client = PortfolioClientStub(
        AccountSnapshot(equity=110000.0, cash=5000.0, buying_power=5000.0),
        [
            SimpleNamespace(
                symbol="ETH/USD",
                qty="2",
                avg_entry_price="2000",
                current_price="2500",
                market_value="5000",
                cost_basis="4000",
                unrealized_pl="1000",
                unrealized_plpc="0.25",
            )
        ],
    )

    state = refresh_from_alpaca(
        client,
        {"ETH/USD": "crypto"},
        {"ETH/USD": 2500.0},
        starting_balance=10000.0,
        trades_today=0,
        account_snapshot=client.get_account_snapshot(),
    )

    position = state.positions[0]
    assert position.avg_entry_price == 2000.0
    assert position.cost_basis == 4000.0
    assert position.unrealized_pnl == 1000.0
    assert position.unrealized_pnl_pct == 25.0
    assert state.total_pnl == 1000.0
    assert state.pnl_data_complete
    assert state.unknown_position_pnl_count == 0


def test_missing_crypto_cost_basis_is_not_treated_as_full_profit_and_dashboard_shows_na():
    client = PortfolioClientStub(
        AccountSnapshot(equity=110000.0, cash=5000.0, buying_power=5000.0),
        [
            SimpleNamespace(
                symbol="ETH/USD",
                qty="0.5",
                avg_entry_price=None,
                current_price="2500",
                market_value="1250",
                cost_basis=None,
                unrealized_pl=None,
                unrealized_plpc=None,
            )
        ],
    )

    state = refresh_from_alpaca(
        client,
        {"ETH/USD": "crypto"},
        {"ETH/USD": 2500.0},
        starting_balance=10000.0,
        trades_today=0,
        account_snapshot=client.get_account_snapshot(),
    )
    state.max_total_exposure = 800.0
    state.daily_pnl = -50.0
    state.start_of_day_equity = 110050.0

    position = state.positions[0]
    assert position.avg_entry_price is None
    assert position.unrealized_pnl is None
    assert position.unrealized_pnl_pct is None
    assert state.total_pnl == 0.0
    assert not state.pnl_data_complete
    assert state.unknown_position_pnl_count == 1

    dashboard = generate_dashboard(state, [{"symbol": "ETH/USD", "name": "Ethereum", "type": "crypto"}])
    assert "Configured Strategy Budget" in dashboard
    assert "Alpaca Paper Account Equity" in dashboard
    assert "Strategy Max Gross Exposure" in dashboard
    assert "Actual Broker Gross Exposure" in dashboard
    assert "LEGACY PAPER ACCOUNT STATE" in dashboard
    assert "N/A" in dashboard

