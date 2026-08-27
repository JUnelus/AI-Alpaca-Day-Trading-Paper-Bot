from types import SimpleNamespace

from src.alpaca_client import AlpacaClient


class RecordingTradingClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.orders = []
        self.lookup = {}

    def submit_order(self, order):
        self.orders.append(order)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        order_id = getattr(response, "id", None)
        if order_id is not None:
            self.lookup[str(order_id)] = response
        return response

    def get_order_by_id(self, order_id, filter=None):
        return self.lookup.get(str(order_id))


def _order(**kwargs):
    return SimpleNamespace(**kwargs)


def test_buy_is_not_treated_as_protected_without_confirmed_stop_submission():
    entry = _order(
        id="entry-1",
        status="accepted",
        filled_qty=1.0,
        filled_avg_price=100.0,
        order_class=None,
        legs=[],
    )
    client = RecordingTradingClient([entry])
    alpaca = AlpacaClient(trading_client=client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=1.0,
        side="buy",
        asset_type="stock",
        mode="trade",
        stop_loss=95.0,
    )

    assert not result.success
    assert result.protection_failed
    assert not result.protection_active
    assert result.counts_as_trade
    assert result.status == "protection_failed"


def test_correct_stop_price_reaches_alpaca_order_request():
    stop_leg = _order(id="stop-1", status="new", stop_price=95.0)
    entry = _order(
        id="entry-1",
        status="accepted",
        filled_qty=1.0,
        filled_avg_price=100.0,
        order_class="oto",
        legs=[stop_leg],
    )
    client = RecordingTradingClient([entry])
    alpaca = AlpacaClient(trading_client=client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=1.0,
        side="buy",
        asset_type="stock",
        mode="trade",
        stop_loss=95.0,
    )

    submitted_request = client.orders[0]
    assert submitted_request.stop_loss.stop_price == 95.0
    assert submitted_request.order_class.value == "oto"
    assert result.success
    assert result.protection_active
    assert result.protective_order_id == "stop-1"


def test_stop_quantity_cannot_exceed_filled_entry_quantity():
    entry = _order(
        id="entry-1",
        status="filled",
        filled_qty=2.5,
        filled_avg_price=100.0,
        order_class=None,
        legs=[],
    )
    stop = _order(id="stop-1", status="new", stop_price=95.0)
    client = RecordingTradingClient([entry, stop])
    alpaca = AlpacaClient(trading_client=client, paper=True, prefer_attached_stops=False)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=5.0,
        side="buy",
        asset_type="stock",
        mode="trade",
        stop_loss=95.0,
    )

    stop_request = client.orders[1]
    assert stop_request.qty == 2.5
    assert result.filled_qty == 2.5
    assert result.protective_order_id == "stop-1"


def test_stop_placement_failure_is_surfaced_clearly():
    entry = _order(
        id="entry-1",
        status="filled",
        filled_qty=3.0,
        filled_avg_price=100.0,
        order_class=None,
        legs=[],
    )
    client = RecordingTradingClient([entry, RuntimeError("stop rejected")])
    alpaca = AlpacaClient(trading_client=client, paper=True, prefer_attached_stops=False)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=3.0,
        side="buy",
        asset_type="stock",
        mode="trade",
        stop_loss=95.0,
    )

    assert not result.success
    assert result.protection_failed
    assert result.counts_as_trade
    assert "CRITICAL" in (result.message or "")
    assert result.status == "protection_failed"


def test_sell_to_close_does_not_create_entry_style_stop():
    sell_order = _order(
        id="sell-1",
        status="accepted",
        filled_qty=1.0,
        filled_avg_price=101.0,
        order_class=None,
        legs=[],
    )
    client = RecordingTradingClient([sell_order])
    alpaca = AlpacaClient(trading_client=client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=1.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        stop_loss=None,
    )

    assert result.success
    assert result.protective_order_id is None
    assert not result.protection_active
    assert getattr(client.orders[0], "stop_loss", None) is None


def test_crypto_buy_is_rejected_when_protective_stop_cannot_be_guaranteed():
    client = RecordingTradingClient([])
    alpaca = AlpacaClient(trading_client=client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="BTC/USD",
        qty=0.1,
        side="buy",
        asset_type="crypto",
        mode="trade",
        stop_loss=60000.0,
    )

    assert not result.success
    assert result.status == "rejected_unprotected_asset"
    assert client.orders == []

