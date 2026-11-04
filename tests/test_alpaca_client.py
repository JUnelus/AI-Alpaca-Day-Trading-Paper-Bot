from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from src import alpaca_client as alpaca_client_module
from src.alpaca_client import AlpacaClient

# The fractional-entry tests build real alpaca-py request objects, so they need the SDK installed
# (as CI does via requirements.txt); the long-standing tests above are left as they were.
_requires_alpaca_sdk = pytest.mark.skipif(
    alpaca_client_module.TimeInForce is None,
    reason="alpaca-py is not installed; Alpaca request/enum types are unavailable",
)


_CLOCK_NOW = datetime(2026, 8, 27, 14, 0, tzinfo=timezone.utc)


def _clock(is_open=True, minutes_to_close=120.0, now=_CLOCK_NOW):
    return SimpleNamespace(is_open=is_open, timestamp=now, next_close=now + timedelta(minutes=minutes_to_close))


class _NotFound(Exception):
    status_code = 404


class RecordingTradingClient:
    def __init__(self, responses=None, open_orders=None, cancel_fail_ids=None, order_sequences=None, positions=None, fractionable=True, clock=None, clock_error=None, on_submit=None):
        self.responses = list(responses or [])
        self.fractionable = fractionable
        # Default: an open market with ample time before the close, so fractional entries are not cut off.
        self.clock = clock if clock is not None else _clock()
        self.clock_error = clock_error
        self.on_submit = on_submit
        self.orders = []
        self.lookup = {}
        self.open_orders = []
        self.cancelled_ids = []
        self.cancel_fail_ids = set(cancel_fail_ids or [])
        self.order_sequences = {str(order_id): list(sequence) for order_id, sequence in (order_sequences or {}).items()}
        self.positions = list(positions or [])

        for order in open_orders or []:
            self._register(order, include_in_open=True)

    def get_clock(self):
        if self.clock_error is not None:
            raise self.clock_error
        return self.clock

    def submit_order(self, order):
        self.orders.append(order)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        if self.on_submit is not None:
            self.on_submit(order, response)

        if getattr(response, "symbol", None) is None:
            response.symbol = getattr(order, "symbol", None)
        if getattr(response, "qty", None) is None:
            response.qty = getattr(order, "qty", None)
        if getattr(response, "side", None) is None:
            response.side = getattr(order, "side", None)
        if getattr(response, "stop_price", None) is None and getattr(order, "stop_price", None) is not None:
            response.stop_price = getattr(order, "stop_price")
        if getattr(response, "client_order_id", None) is None and getattr(order, "client_order_id", None) is not None:
            response.client_order_id = getattr(order, "client_order_id")

        self._register(response)
        return response

    def get_order_by_client_id(self, client_order_id):
        if getattr(self, "client_lookup_error", None) is not None:
            raise self.client_lookup_error
        for order in self.lookup.values():
            if getattr(order, "client_order_id", None) == client_order_id:
                return order
        raise _NotFound()

    def get_order_by_id(self, order_id, filter=None):
        sequence = self.order_sequences.get(str(order_id))
        if sequence:
            if len(sequence) > 1:
                return sequence.pop(0)
            return sequence[0]
        return self.lookup.get(str(order_id))

    def get_asset(self, symbol):
        return SimpleNamespace(symbol=symbol, tradable=True, fractionable=self.fractionable)

    def get_open_position(self, symbol):
        for position in self.positions:
            if getattr(position, "symbol", None) == symbol:
                return position
        raise RuntimeError("position not found")

    def get_all_positions(self):
        return list(self.positions)

    def get_orders(self, filter=None):
        symbols = getattr(filter, "symbols", None) if filter is not None else None
        orders = []
        for order in self.open_orders:
            order_id = str(getattr(order, "id", ""))
            current_order = self.order_sequences[order_id][0] if order_id in self.order_sequences and self.order_sequences[order_id] else order
            status = str(getattr(current_order, "status", "")).lower()
            if status in {"canceled", "cancelled", "filled", "rejected"}:
                continue
            if symbols and getattr(current_order, "symbol", None) not in symbols:
                continue
            orders.append(current_order)
        return orders

    def cancel_order_by_id(self, order_id):
        if str(order_id) in self.cancel_fail_ids:
            raise RuntimeError("cancel rejected")
        if str(order_id) not in self.order_sequences:
            order = self.lookup[str(order_id)]
            order.status = "canceled"
        self.cancelled_ids.append(str(order_id))

    def _register(self, order, include_in_open=None):
        order_id = getattr(order, "id", None)
        if order_id is not None:
            self.lookup[str(order_id)] = order
        status = str(getattr(order, "status", "")).lower()
        should_open = include_in_open if include_in_open is not None else status in {"new", "accepted", "pending_new", "partially_filled"}
        if should_open and order not in self.open_orders:
            self.open_orders.append(order)


def _order(**kwargs):
    return SimpleNamespace(**kwargs)


def _alpaca(client, **kwargs):
    return AlpacaClient(trading_client=client, sleep_fn=lambda *_: None, **kwargs)


def test_protected_stock_buy_uses_gtc_and_passes_stop_price():
    stop_leg = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=95.0, qty=1.0)
    entry = _order(
        id="entry-1",
        symbol="AAPL",
        side="buy",
        status="accepted",
        filled_qty=1.0,
        filled_avg_price=100.0,
        order_class="oto",
        legs=[stop_leg],
    )
    client = RecordingTradingClient([entry])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=1.0,
        side="buy",
        asset_type="stock",
        mode="trade",
        stop_loss=95.0,
    )

    submitted_request = client.orders[0]
    assert submitted_request.time_in_force.value == "gtc"
    assert submitted_request.stop_loss.stop_price == 95.0
    assert submitted_request.order_class.value == "oto"
    assert result.success
    assert result.protection_active
    assert result.protective_order_id == "stop-1"


def test_protected_etf_buy_uses_gtc():
    stop_leg = _order(id="stop-1", symbol="SPY", side="sell", status="new", stop_price=495.0, qty=1.0)
    entry = _order(
        id="entry-1",
        symbol="SPY",
        side="buy",
        status="accepted",
        filled_qty=1.0,
        filled_avg_price=500.0,
        order_class="oto",
        legs=[stop_leg],
    )
    client = RecordingTradingClient([entry])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="SPY",
        qty=1.0,
        side="buy",
        asset_type="etf",
        mode="trade",
        stop_loss=495.0,
    )

    assert client.orders[0].time_in_force.value == "gtc"
    assert result.success


def test_buy_is_not_treated_as_protected_without_confirmed_stop_submission():
    entry = _order(
        id="entry-1",
        symbol="AAPL",
        side="buy",
        status="accepted",
        filled_qty=1.0,
        filled_avg_price=100.0,
        order_class=None,
        legs=[],
    )
    client = RecordingTradingClient([entry])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

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


def test_stop_quantity_cannot_exceed_filled_entry_quantity():
    entry = _order(
        id="entry-1",
        symbol="AAPL",
        side="buy",
        status="filled",
        filled_qty=2.5,
        filled_avg_price=100.0,
        order_class=None,
        legs=[],
    )
    stop = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=95.0, qty=2.5)
    client = RecordingTradingClient([entry, stop])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=False)

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
        symbol="AAPL",
        side="buy",
        status="filled",
        filled_qty=3.0,
        filled_avg_price=100.0,
        order_class=None,
        legs=[],
    )
    client = RecordingTradingClient([entry, RuntimeError("stop rejected")])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=False)

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
        status="filled",
        symbol="AAPL",
        side="sell",
        filled_qty=1.0,
        filled_avg_price=101.0,
        order_class="oto",
        legs=[],
    )
    client = RecordingTradingClient([sell_order])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

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
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

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


def test_paper_false_blocks_all_order_placement():
    client = RecordingTradingClient([])
    alpaca = _alpaca(client, paper=False, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=1.0,
        side="buy",
        asset_type="stock",
        mode="trade",
        stop_loss=95.0,
    )

    assert not result.success
    assert result.status == "rejected_live_disabled"
    assert client.orders == []


def test_full_sell_cancels_existing_protective_stop_before_exit():
    stop_order = _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=5.0, filled_qty=5.0, filled_avg_price=101.0, status="filled", order_class=None, legs=[])
    client = RecordingTradingClient(responses=[sell_order], open_orders=[stop_order])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=5.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=5.0,
    )

    assert result.success
    assert result.protection_reconciled
    assert result.remaining_position_qty == 0.0
    assert result.cancelled_protective_order_ids == ["stop-1"]
    assert client.cancelled_ids == ["stop-1"]
    assert client.orders[0].side.value == "sell"


def test_partial_sell_replaces_protection_with_remaining_quantity():
    old_stop = _order(id="stop-old", symbol="AAPL", side="sell", qty=10.0, stop_price=95.0, status="new")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=4.0, filled_qty=4.0, filled_avg_price=101.0, status="filled", order_class=None, legs=[])
    replacement_stop = _order(id="stop-new", symbol="AAPL", side="sell", qty=6.0, stop_price=95.0, status="new")
    client = RecordingTradingClient(
        responses=[sell_order, replacement_stop],
        open_orders=[old_stop],
        positions=[_order(symbol="AAPL", qty="6", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=4.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=10.0,
    )

    assert result.success
    assert result.protection_reconciled
    assert result.remaining_position_qty == 6.0
    assert result.cancelled_protective_order_ids == ["stop-old"]
    assert result.replacement_protective_order_id == "stop-new"
    assert result.protective_order_id == "stop-new"
    assert client.orders[1].qty == 6.0


def test_sell_is_blocked_if_protective_stop_cancellation_fails():
    stop_order = _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    client = RecordingTradingClient(open_orders=[stop_order], cancel_fail_ids={"stop-1"})
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=5.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=5.0,
    )

    assert not result.success
    assert result.status == "protective_stop_cancel_failed"
    assert client.orders == []


def test_sell_is_blocked_if_protective_stop_cannot_be_identified_safely():
    ambiguous_sell = _order(id="sell-open", symbol="AAPL", side="sell", qty=5.0, status="new")
    client = RecordingTradingClient(open_orders=[ambiguous_sell])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=5.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=5.0,
    )

    assert not result.success
    assert result.status == "protection_reconciliation_failed"
    assert client.orders == []


def test_sell_failure_after_stop_cancellation_is_surfaced_clearly():
    stop_order = _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    restored_stop = _order(id="stop-restored", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    client = RecordingTradingClient(
        responses=[RuntimeError("sell rejected"), restored_stop],
        open_orders=[stop_order],
        positions=[_order(symbol="AAPL", qty="5", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=5.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=5.0,
    )

    assert not result.success
    assert result.status == "sell_failed_protection_restored"
    assert result.cancelled_protective_order_ids == ["stop-1"]
    assert result.protection_restored


def test_partial_sell_replacement_stop_failure_is_surfaced_clearly():
    old_stop = _order(id="stop-old", symbol="AAPL", side="sell", qty=10.0, stop_price=95.0, status="new")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=4.0, filled_qty=4.0, filled_avg_price=101.0, status="filled", order_class=None, legs=[])
    client = RecordingTradingClient(
        responses=[sell_order, RuntimeError("replacement failed"), RuntimeError("replacement failed"), RuntimeError("replacement failed")],
        open_orders=[old_stop],
        positions=[_order(symbol="AAPL", qty="6", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=4.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=10.0,
    )

    assert not result.success
    assert result.counts_as_trade
    assert result.protection_failed
    assert result.actual_remaining_position_qty == 6.0
    assert result.status == "critical_unprotected_position"


def test_sell_with_ambiguous_fill_after_cancellation_fails_closed():
    stop_order = _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=5.0, filled_qty=0.0, filled_avg_price=None, status="accepted", order_class=None, legs=[])
    restored_stop = _order(id="stop-restored", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    client = RecordingTradingClient(
        responses=[sell_order, restored_stop],
        open_orders=[stop_order],
        positions=[_order(symbol="AAPL", qty="5", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=5.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=5.0,
    )

    assert not result.success
    assert result.counts_as_trade
    assert result.status == "sell_failed_protection_restored"
    assert result.protection_restored


def test_sell_failure_restores_original_stop_when_possible():
    stop_order = _order(id="stop-old", symbol="AAPL", side="sell", qty=10.0, stop_price=95.0, status="new", time_in_force="gtc", type="stop")
    restored_stop = _order(id="stop-restored", symbol="AAPL", side="sell", qty=10.0, stop_price=95.0, status="new")
    client = RecordingTradingClient(
        responses=[RuntimeError("sell failed"), restored_stop],
        open_orders=[stop_order],
        positions=[_order(symbol="AAPL", qty="10", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=10.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=10.0,
    )

    assert not result.success
    assert result.protection_restore_attempted
    assert result.protection_restored
    assert result.restored_protective_order_id == "stop-restored"
    assert result.actual_remaining_position_qty == 10.0


def test_sell_failure_without_restoration_returns_critical_unprotected_state():
    stop_order = _order(id="stop-old", symbol="AAPL", side="sell", qty=10.0, stop_price=95.0, status="new", time_in_force="gtc", type="stop")
    client = RecordingTradingClient(
        responses=[RuntimeError("sell failed"), RuntimeError("restore failed"), RuntimeError("restore failed"), RuntimeError("restore failed")],
        open_orders=[stop_order],
        positions=[_order(symbol="AAPL", qty="10", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=10.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=10.0,
    )

    assert not result.success
    assert result.status == "critical_unprotected_position"
    assert result.protection_failed
    assert not result.protection_reconciled


def test_partial_sell_replacement_retries_and_succeeds():
    old_stop = _order(id="stop-old", symbol="AAPL", side="sell", qty=10.0, stop_price=95.0, status="new", time_in_force="gtc", type="stop")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=4.0, filled_qty=4.0, filled_avg_price=101.0, status="filled", order_class=None, legs=[])
    replacement_stop = _order(id="stop-new", symbol="AAPL", side="sell", qty=6.0, stop_price=95.0, status="new")
    client = RecordingTradingClient(
        responses=[sell_order, RuntimeError("replacement failed once"), replacement_stop],
        open_orders=[old_stop],
        positions=[_order(symbol="AAPL", qty="6", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=4.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=10.0,
    )

    assert result.success
    assert result.protection_reconciled
    assert result.actual_remaining_position_qty == 6.0
    assert result.replacement_protective_order_id == "stop-new"
    assert result.protection_retry_count == 2


def test_partial_sell_replacement_all_retries_fail_returns_critical_unprotected_state():
    old_stop = _order(id="stop-old", symbol="AAPL", side="sell", qty=10.0, stop_price=95.0, status="new", time_in_force="gtc", type="stop")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=4.0, filled_qty=4.0, filled_avg_price=101.0, status="filled", order_class=None, legs=[])
    client = RecordingTradingClient(
        responses=[sell_order, RuntimeError("replacement failed"), RuntimeError("replacement failed"), RuntimeError("replacement failed")],
        open_orders=[old_stop],
        positions=[_order(symbol="AAPL", qty="6", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=4.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=10.0,
    )

    assert not result.success
    assert result.status == "critical_unprotected_position"
    assert result.protection_failed
    assert result.actual_remaining_position_qty == 6.0


def test_cancel_verification_succeeds_after_pending_cancel_polling():
    stop_order = _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=5.0, filled_qty=5.0, filled_avg_price=101.0, status="filled", order_class=None, legs=[])
    client = RecordingTradingClient(
        responses=[sell_order],
        open_orders=[stop_order],
        order_sequences={
            "stop-1": [
                _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="pending_cancel"),
                _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="pending_cancel"),
                _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="canceled"),
            ]
        },
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=5.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=5.0,
    )

    assert result.success
    assert result.cancel_poll_attempts == 3


def test_cancel_timeout_fails_closed():
    stop_order = _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    client = RecordingTradingClient(
        open_orders=[stop_order],
        order_sequences={
            "stop-1": [
                _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="pending_cancel"),
                _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="pending_cancel"),
                _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="pending_cancel"),
                _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="pending_cancel"),
                _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="pending_cancel"),
            ]
        },
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True, cancel_poll_attempts=5)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=5.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=5.0,
    )

    assert not result.success
    assert result.status == "protective_stop_cancel_timeout"
    assert client.orders == []


def test_stop_fill_during_cancellation_prevents_duplicate_sell():
    stop_order = _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    client = RecordingTradingClient(
        open_orders=[stop_order],
        positions=[],
        order_sequences={
            "stop-1": [_order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="pending_cancel"), _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="filled")]
        },
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=5.0,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=5.0,
    )

    assert not result.success
    assert result.status == "position_closed_by_protective_stop"
    assert client.orders == []


def test_attached_stop_child_can_appear_after_bounded_polling():
    submitted = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=1.0, filled_avg_price=100.0, order_class="oto", legs=[])
    delayed_stop = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=95.0, qty=1.0)
    polled_order = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=1.0, filled_avg_price=100.0, order_class="oto", legs=[delayed_stop])
    client = RecordingTradingClient(
        responses=[submitted],
        order_sequences={"entry-1": [submitted, submitted, polled_order]},
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True, stop_confirmation_poll_attempts=5)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=1.0,
        side="buy",
        asset_type="stock",
        mode="trade",
        stop_loss=95.0,
    )

    assert result.success
    assert result.stop_confirmation_poll_attempts == 3


def test_attached_oto_without_stop_child_fails_closed():
    submitted = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=1.0, filled_avg_price=100.0, order_class="oto", legs=[])
    client = RecordingTradingClient(
        responses=[submitted],
        order_sequences={"entry-1": [submitted] * 5},
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True, stop_confirmation_poll_attempts=5)

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
    assert result.protective_order_id is None


def test_attached_stop_child_without_id_fails_closed():
    stop_leg = _order(symbol="AAPL", side="sell", status="new", stop_price=95.0, qty=1.0)
    submitted = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=1.0, filled_avg_price=100.0, order_class="oto", legs=[stop_leg])
    client = RecordingTradingClient(responses=[submitted], order_sequences={"entry-1": [submitted]})
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

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


def test_attached_stop_child_with_invalid_quantity_fails_closed():
    stop_leg = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=95.0, qty=5.0)
    submitted = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=1.0, filled_avg_price=100.0, order_class="oto", legs=[stop_leg])
    client = RecordingTradingClient(responses=[submitted], order_sequences={"entry-1": [submitted]})
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

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




# ── fractional equity entries (small budgets) ─────────────────────────────────


def _fractional_buy(alpaca, qty=0.0288, symbol="AAPL"):
    return alpaca.place_paper_trade(
        symbol=symbol,
        qty=qty,
        side="buy",
        asset_type="stock",
        mode="trade",
        stop_loss=340.0,
    )


@_requires_alpaca_sdk
def test_fractional_stock_buy_uses_day_entry_and_confirmed_day_stop():
    entry = _order(id="entry-1", symbol="AAPL", side="buy", status="filled", filled_qty=0.0288, filled_avg_price=347.0, order_class=None, legs=[])
    stop = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=340.0, qty=0.0288, time_in_force="day")
    client = RecordingTradingClient([entry, stop])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    assert alpaca.can_place_protected_buy("stock", allow_fractional=True)
    result = _fractional_buy(alpaca)

    entry_request, stop_request = client.orders
    assert entry_request.qty == 0.0288
    assert entry_request.time_in_force.value == "day"
    assert getattr(entry_request, "stop_loss", None) is None
    assert stop_request.qty == 0.0288
    assert stop_request.time_in_force.value == "day"
    assert stop_request.stop_price == 340.0
    assert result.success
    assert result.protection_active
    assert result.protective_order_id == "stop-1"
    assert result.protection_time_in_force == "day"
    assert result.requires_eod_exit
    assert result.counts_as_trade


def test_fractional_stock_buy_is_rejected_when_broker_asset_is_not_fractionable():
    client = RecordingTradingClient([], fractionable=False)
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = _fractional_buy(alpaca)

    assert not result.success
    assert result.status == "rejected_fractional_unsupported"
    assert client.orders == []


@_requires_alpaca_sdk
def test_whole_share_buy_still_uses_attached_gtc_route():
    stop_leg = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=340.0, qty=1.0)
    entry = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=1.0, filled_avg_price=347.0, order_class="oto", legs=[stop_leg])
    client = RecordingTradingClient([entry])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = _fractional_buy(alpaca, qty=1.0)

    assert client.orders[0].time_in_force.value == "gtc"
    assert client.orders[0].order_class.value == "oto"
    assert result.success
    assert result.protection_time_in_force is None
    assert not result.requires_eod_exit


@_requires_alpaca_sdk
def test_fractional_entry_unfilled_remainder_is_cancelled_before_any_stop():
    pending = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=0.0, order_class=None, legs=[])
    cancelled = _order(id="entry-1", symbol="AAPL", side="buy", status="canceled", filled_qty=0.0, order_class=None, legs=[])
    client = RecordingTradingClient(
        [pending],
        order_sequences={"entry-1": [pending, pending, pending, pending, cancelled]},
    )
    alpaca = _alpaca(client, paper=True, entry_fill_poll_attempts=3, cancel_poll_attempts=5)

    result = _fractional_buy(alpaca)

    assert client.cancelled_ids == ["entry-1"]
    assert len(client.orders) == 1  # no stop was created for a zero fill
    assert result.success
    assert result.status == "entry_canceled_no_fill"
    assert not result.counts_as_trade
    assert not result.protection_failed
    assert result.entry_cancel_attempted and result.entry_cancel_confirmed


@_requires_alpaca_sdk
def test_fractional_partial_fill_cancels_remainder_and_protects_only_filled_qty():
    partial = _order(id="entry-1", symbol="AAPL", side="buy", status="partially_filled", filled_qty=0.01, filled_avg_price=347.0, order_class=None, legs=[])
    settled = _order(id="entry-1", symbol="AAPL", side="buy", status="canceled", filled_qty=0.01, filled_avg_price=347.0, order_class=None, legs=[])
    stop = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=340.0, qty=0.01, time_in_force="day")
    client = RecordingTradingClient(
        [partial, stop],
        order_sequences={"entry-1": [partial, partial, partial, partial, settled]},
    )
    alpaca = _alpaca(client, paper=True, entry_fill_poll_attempts=3, cancel_poll_attempts=5)

    result = _fractional_buy(alpaca)

    assert client.cancelled_ids == ["entry-1"]
    stop_request = client.orders[1]
    assert stop_request.qty == 0.01
    assert stop_request.time_in_force.value == "day"
    assert result.success
    assert result.filled_qty == 0.01
    assert result.protection_active
    assert result.requires_eod_exit


@_requires_alpaca_sdk
def test_fractional_entry_that_never_settles_fails_closed():
    pending = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=0.0, order_class=None, legs=[])
    client = RecordingTradingClient([pending], order_sequences={"entry-1": [pending]})
    alpaca = _alpaca(client, paper=True, entry_fill_poll_attempts=2, cancel_poll_attempts=2)

    result = _fractional_buy(alpaca)

    assert not result.success
    assert result.status == "entry_state_ambiguous"
    assert client.cancelled_ids == ["entry-1"]
    assert len(client.orders) == 1
    assert "CRITICAL" in (result.message or "")
    # The order may still fill, so it reserves its trade slot, cash and exposure.
    assert result.counts_as_trade
    assert result.protection_failed


@_requires_alpaca_sdk
def test_fractional_day_stop_that_is_rejected_by_broker_is_a_protection_failure():
    entry = _order(id="entry-1", symbol="AAPL", side="buy", status="filled", filled_qty=0.0288, filled_avg_price=347.0, order_class=None, legs=[])
    rejected_stop = _order(id="stop-1", symbol="AAPL", side="sell", status="rejected", stop_price=340.0, qty=0.0288, time_in_force="day")
    client = RecordingTradingClient([entry, rejected_stop])
    alpaca = _alpaca(client, paper=True, stop_confirmation_poll_attempts=2)

    result = _fractional_buy(alpaca)

    assert not result.success
    assert result.status == "protection_failed"
    assert result.protection_failed
    assert result.counts_as_trade
    assert "CRITICAL" in (result.message or "")


@_requires_alpaca_sdk
def test_fractional_stop_placement_failure_is_surfaced_clearly():
    entry = _order(id="entry-1", symbol="AAPL", side="buy", status="filled", filled_qty=0.0288, filled_avg_price=347.0, order_class=None, legs=[])
    client = RecordingTradingClient([entry, RuntimeError("fractional stop rejected")])
    alpaca = _alpaca(client, paper=True)

    result = _fractional_buy(alpaca)

    assert not result.success
    assert result.status == "protection_failed"
    assert result.requires_eod_exit
    assert "fractional stop rejected" in (result.message or "")


@_requires_alpaca_sdk
def test_partial_sell_of_fractional_position_replaces_protection_with_day_stop():
    old_stop = _order(id="stop-old", symbol="AAPL", side="sell", qty=0.03, stop_price=340.0, status="new", time_in_force="day")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=0.01, filled_qty=0.01, filled_avg_price=350.0, status="filled", order_class=None, legs=[])
    replacement_stop = _order(id="stop-new", symbol="AAPL", side="sell", qty=0.02, stop_price=340.0, status="new", time_in_force="day")
    client = RecordingTradingClient(
        responses=[sell_order, replacement_stop],
        open_orders=[old_stop],
        positions=[_order(symbol="AAPL", qty="0.02", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(
        symbol="AAPL",
        qty=0.01,
        side="sell",
        asset_type="stock",
        mode="trade",
        current_position_qty=0.03,
    )

    assert result.success, result.message
    assert result.cancelled_protective_order_ids == ["stop-old"]
    assert result.replacement_protective_order_id == "stop-new"
    assert client.orders[0].time_in_force.value == "day"
    assert client.orders[1].qty == 0.02
    assert client.orders[1].time_in_force.value == "day"


# ── fractional entry cutoff and end-of-day cleanup ────────────────────────────

def test_fractional_buy_is_blocked_inside_the_eod_window():
    client = RecordingTradingClient([], clock=_clock(minutes_to_close=20))
    alpaca = _alpaca(client, paper=True, fractional_eod_window_minutes=30)

    result = _fractional_buy(alpaca)

    assert not result.success
    assert result.status == "fractional_entry_after_eod_cutoff"
    assert "20 minutes remain" in result.message
    assert client.orders == []


def test_fractional_buy_is_blocked_when_market_closed_or_clock_unusable():
    closed = _alpaca(RecordingTradingClient([], clock=_clock(is_open=False)), paper=True)
    broken = _alpaca(RecordingTradingClient([], clock_error=RuntimeError("clock down")), paper=True)
    naive = _alpaca(RecordingTradingClient([], clock=SimpleNamespace(is_open=True, timestamp=datetime(2026, 8, 27, 14, 0), next_close=datetime(2026, 8, 27, 20, 0))), paper=True)
    no_clock_client = RecordingTradingClient([])
    del no_clock_client.clock
    no_clock_client.get_clock = None
    no_clock = _alpaca(no_clock_client, paper=True)
    no_clock._client = SimpleNamespace(get_asset=no_clock_client.get_asset)

    for alpaca in (closed, broken, naive, no_clock):
        result = _fractional_buy(alpaca)
        assert not result.success
        assert result.status == "fractional_entry_after_eod_cutoff"
        assert alpaca._client is no_clock._client or alpaca._client.orders == []


@_requires_alpaca_sdk
def test_whole_share_buy_is_not_subject_to_the_eod_window():
    stop_leg = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=340.0, qty=1.0)
    entry = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=1.0, filled_avg_price=347.0, order_class="oto", legs=[stop_leg])
    client = RecordingTradingClient([entry], clock=_clock(minutes_to_close=5))
    alpaca = _alpaca(client, paper=True)

    result = _fractional_buy(alpaca, qty=1.0)

    assert result.success
    assert client.orders[0].time_in_force.value == "gtc"


def test_eod_cleanup_window_classification_uses_only_the_broker_clock(monkeypatch):
    monkeypatch.setenv("FRACTIONAL_EOD_WINDOW_MINUTES", "45")
    assert _alpaca(RecordingTradingClient([], clock=_clock(minutes_to_close=46)), paper=True).eod_cleanup_window()["state"] == "before_window"
    assert _alpaca(RecordingTradingClient([], clock=_clock(minutes_to_close=45)), paper=True).eod_cleanup_window()["state"] == "in_window"
    assert _alpaca(RecordingTradingClient([], clock=_clock(is_open=False)), paper=True).eod_cleanup_window()["state"] == "closed"
    assert _alpaca(RecordingTradingClient([], clock=_clock(minutes_to_close=-1)), paper=True).eod_cleanup_window()["state"] == "closed"
    assert _alpaca(RecordingTradingClient([], clock_error=RuntimeError("down")), paper=True).eod_cleanup_window()["state"] == "unavailable"
    assert _alpaca(RecordingTradingClient([], clock=SimpleNamespace(is_open="yes", timestamp=_CLOCK_NOW, next_close=_CLOCK_NOW)), paper=True).eod_cleanup_window()["state"] == "unavailable"
    # Explicit constructor values win over the environment and are floored at one minute.
    assert _alpaca(RecordingTradingClient([]), paper=True, fractional_eod_window_minutes=0).fractional_eod_window_minutes == 1


def test_list_positions_strict_raises_instead_of_reading_as_flat():
    class BrokenPositions(RecordingTradingClient):
        def get_all_positions(self):
            raise RuntimeError("positions endpoint down")

    alpaca = _alpaca(BrokenPositions([]), paper=True)
    assert alpaca.list_positions() == []
    with pytest.raises(RuntimeError):
        alpaca.list_positions_strict()
    with pytest.raises(RuntimeError):
        AlpacaClient(trading_client=None, paper=True).list_positions_strict()


def test_close_position_for_eod_rejects_unsafe_inputs_without_touching_the_broker():
    client = RecordingTradingClient([], positions=[_order(symbol="AAPL", qty="0.03", side="long")])
    alpaca = _alpaca(client, paper=True)

    assert alpaca.close_position_for_eod("BTC/USD", 0.01, "crypto", 0.01).status == "rejected_not_equity"
    assert alpaca.close_position_for_eod("AAPL", 0.05, "stock", 0.03).status == "rejected_invalid_qty"
    assert alpaca.close_position_for_eod("AAPL", 0.0, "stock", 0.03).status == "rejected_invalid_qty"
    assert _alpaca(RecordingTradingClient([]), paper=False).close_position_for_eod("AAPL", 0.03, "stock", 0.03).status == "rejected_live_disabled"
    assert AlpacaClient(trading_client=None, paper=True).close_position_for_eod("AAPL", 0.03, "stock", 0.03).status == "skipped"
    assert client.orders == []
    assert client.cancelled_ids == []


@_requires_alpaca_sdk
def test_close_position_for_eod_cancels_day_stop_then_confirms_full_exit():
    day_stop = _order(id="stop-day", symbol="AAPL", side="sell", qty=0.0288, stop_price=340.0, status="new", time_in_force="day")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=0.0288, filled_qty=0.0288, filled_avg_price=350.0, status="filled", order_class=None, legs=[])
    client = RecordingTradingClient(
        responses=[sell_order],
        open_orders=[day_stop],
        positions=[_order(symbol="AAPL", qty="0.0288", side="long")],
        on_submit=lambda order, response: client.positions.clear(),
    )
    alpaca = _alpaca(client, paper=True)

    result = alpaca.close_position_for_eod("AAPL", 0.0288, "stock", current_position_qty=0.0288)

    assert result.success, result.message
    assert result.eod_exit
    assert result.counts_as_trade
    assert result.filled_qty == 0.0288
    assert result.cancelled_protective_order_ids == ["stop-day"]
    assert client.cancelled_ids == ["stop-day"]
    assert len(client.orders) == 1
    assert client.orders[0].side.value == "sell"
    assert client.orders[0].time_in_force.value == "day"
    assert result.actual_remaining_position_qty == 0.0
    assert result.protection_reconciled


@_requires_alpaca_sdk
def test_close_position_for_eod_unfilled_sell_is_cancelled_before_protection_is_restored():
    day_stop = _order(id="stop-day", symbol="AAPL", side="sell", qty=0.03, stop_price=340.0, status="new", time_in_force="day")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=0.03, filled_qty=0.0, status="accepted", order_class=None, legs=[])
    restored_stop = _order(id="stop-restored", symbol="AAPL", side="sell", qty=0.03, stop_price=340.0, status="new", time_in_force="day")
    client = RecordingTradingClient(
        responses=[sell_order, restored_stop],
        open_orders=[day_stop],
        positions=[_order(symbol="AAPL", qty="0.03", side="long")],
        order_sequences={
            "sell-1": [
                _order(id="sell-1", symbol="AAPL", side="sell", qty=0.03, filled_qty=0.0, status="accepted"),
                _order(id="sell-1", symbol="AAPL", side="sell", qty=0.03, filled_qty=0.0, status="accepted"),
                _order(id="sell-1", symbol="AAPL", side="sell", qty=0.03, filled_qty=0.0, status="pending_cancel"),
                _order(id="sell-1", symbol="AAPL", side="sell", qty=0.03, filled_qty=0.0, status="canceled"),
            ]
        },
    )
    alpaca = _alpaca(client, paper=True, exit_fill_poll_attempts=2)

    result = alpaca.close_position_for_eod("AAPL", 0.03, "stock", current_position_qty=0.03)

    assert not result.success
    assert result.status == "sell_failed_protection_restored"
    assert client.cancelled_ids == ["stop-day", "sell-1"]  # the SELL is cancelled and confirmed before any stop returns
    assert result.exit_poll_attempts >= 3
    assert result.protection_active
    assert result.protection_restored
    assert result.restored_protective_order_id == "stop-restored"
    assert client.orders[1].time_in_force.value == "day"
    assert client.orders[1].qty == 0.03


@_requires_alpaca_sdk
def test_close_position_for_eod_ambiguous_sell_state_fails_closed_without_stacking_a_stop():
    day_stop = _order(id="stop-day", symbol="AAPL", side="sell", qty=0.03, stop_price=340.0, status="new", time_in_force="day")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=0.03, filled_qty=0.0, status="accepted", order_class=None, legs=[])
    client = RecordingTradingClient(
        responses=[sell_order],
        open_orders=[day_stop],
        positions=[_order(symbol="AAPL", qty="0.03", side="long")],
        order_sequences={"sell-1": [_order(id="sell-1", symbol="AAPL", side="sell", qty=0.03, filled_qty=0.0, status="accepted")]},
    )
    alpaca = _alpaca(client, paper=True, exit_fill_poll_attempts=1, cancel_poll_attempts=2)

    result = alpaca.close_position_for_eod("AAPL", 0.03, "stock", current_position_qty=0.03)

    assert not result.success
    assert result.status == "critical_unprotected_position"
    assert result.protection_failed
    assert "did not reach a terminal state" in result.message
    assert len(client.orders) == 1  # no replacement stop while the SELL may still execute
    assert "sell-1" in client.cancelled_ids


@_requires_alpaca_sdk
def test_close_position_for_eod_partial_fill_is_reported_as_incomplete_even_when_re_protected():
    day_stop = _order(id="stop-day", symbol="AAPL", side="sell", qty=0.03, stop_price=340.0, status="new", time_in_force="day")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=0.03, filled_qty=0.01, filled_avg_price=350.0, status="canceled", order_class=None, legs=[])
    replacement_stop = _order(id="stop-new", symbol="AAPL", side="sell", qty=0.02, stop_price=340.0, status="new", time_in_force="day")
    positions = [_order(symbol="AAPL", qty="0.03", side="long")]

    def on_submit(order, response):
        if getattr(response, "id", None) == "sell-1":
            positions[0].qty = "0.02"

    client = RecordingTradingClient(responses=[sell_order, replacement_stop], open_orders=[day_stop], positions=positions, on_submit=on_submit)
    alpaca = _alpaca(client, paper=True)

    result = alpaca.close_position_for_eod("AAPL", 0.03, "stock", current_position_qty=0.03)

    assert not result.success
    assert result.status == "eod_exit_incomplete"
    assert result.counts_as_trade
    assert result.filled_qty == 0.01
    assert result.actual_remaining_position_qty == 0.02
    assert result.protection_active
    assert result.replacement_protective_order_id == "stop-new"
    assert "expires at the close" in result.message


# ── review follow-ups: entry/stop state handling ──────────────────────────────

@_requires_alpaca_sdk
def test_fractional_request_that_fills_to_whole_shares_gets_a_gtc_stop():
    partial = _order(id="entry-1", symbol="AAPL", side="buy", status="partially_filled", filled_qty=1.0, filled_avg_price=347.0, order_class=None, legs=[])
    settled = _order(id="entry-1", symbol="AAPL", side="buy", status="canceled", filled_qty=1.0, filled_avg_price=347.0, order_class=None, legs=[])
    stop = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=340.0, qty=1.0, time_in_force="gtc")
    client = RecordingTradingClient([partial, stop], order_sequences={"entry-1": [partial, partial, partial, settled]})
    alpaca = _alpaca(client, paper=True, entry_fill_poll_attempts=3, cancel_poll_attempts=5)

    result = _fractional_buy(alpaca, qty=1.5)

    assert result.success, result.message
    assert client.orders[1].qty == 1.0
    assert client.orders[1].time_in_force.value == "gtc"
    assert result.protection_time_in_force == "gtc"
    assert not result.requires_eod_exit
    assert result.protection_active


@_requires_alpaca_sdk
def test_fractional_entry_cancel_is_sent_after_the_last_fill_poll():
    pending = _order(id="entry-1", symbol="AAPL", side="buy", status="accepted", filled_qty=0.0, order_class=None, legs=[])
    cancelled = _order(id="entry-1", symbol="AAPL", side="buy", status="canceled", filled_qty=0.0, order_class=None, legs=[])
    client = RecordingTradingClient([pending], order_sequences={"entry-1": [pending, pending, cancelled]})
    # One confirmation attempt is enough: the cancel goes out after the second (last) fill poll.
    alpaca = _alpaca(client, paper=True, entry_fill_poll_attempts=2, cancel_poll_attempts=1)

    result = _fractional_buy(alpaca)

    assert client.cancelled_ids == ["entry-1"]
    assert result.success
    assert result.status == "entry_canceled_no_fill"
    assert result.entry_poll_attempts == 3


@_requires_alpaca_sdk
def test_fractional_day_stop_is_not_confirmed_while_pending_new():
    entry = _order(id="entry-1", symbol="AAPL", side="buy", status="filled", filled_qty=0.0288, filled_avg_price=347.0, order_class=None, legs=[])
    pending_stop = _order(id="stop-1", symbol="AAPL", side="sell", status="pending_new", stop_price=340.0, qty=0.0288, time_in_force="day")
    rejected_stop = _order(id="stop-1", symbol="AAPL", side="sell", status="rejected", stop_price=340.0, qty=0.0288, time_in_force="day")
    client = RecordingTradingClient([entry, pending_stop], order_sequences={"stop-1": [pending_stop, rejected_stop]})
    alpaca = _alpaca(client, paper=True, stop_confirmation_poll_attempts=3)

    result = _fractional_buy(alpaca)

    assert not result.success
    assert result.status == "protection_failed"
    assert not result.protection_active

    live_stop = _order(id="stop-2", symbol="AAPL", side="sell", status="new", stop_price=340.0, qty=0.0288, time_in_force="day")
    client = RecordingTradingClient([entry, pending_stop], order_sequences={"stop-1": [pending_stop, live_stop]})
    alpaca = _alpaca(client, paper=True, stop_confirmation_poll_attempts=3)
    result = _fractional_buy(alpaca)
    assert result.success and result.protection_active
    assert result.stop_confirmation_poll_attempts == 2


@_requires_alpaca_sdk
def test_eod_sell_whose_submission_raised_but_was_accepted_is_recovered_not_double_protected():
    day_stop = _order(id="stop-day", symbol="AAPL", side="sell", qty=0.03, stop_price=340.0, status="new", time_in_force="day")
    accepted_sell = _order(id="sell-1", symbol="AAPL", side="sell", qty=0.03, filled_qty=0.03, filled_avg_price=350.0, status="filled", order_class=None, legs=[])
    class TimeoutThenAcceptedClient(RecordingTradingClient):
        def submit_order(self, order):
            self.orders.append(order)
            if len(self.orders) == 1:
                accepted_sell.client_order_id = order.client_order_id
                self._register(accepted_sell)
                self.positions.clear()  # the broker filled the SELL even though the response was lost
                raise TimeoutError("read timed out")
            return super().submit_order(order)

    client = TimeoutThenAcceptedClient(responses=[], open_orders=[day_stop], positions=[_order(symbol="AAPL", qty="0.03", side="long")])
    alpaca = _alpaca(client, paper=True)

    result = alpaca.close_position_for_eod("AAPL", 0.03, "stock", current_position_qty=0.03)

    assert result.success, result.message
    assert result.filled_qty == 0.03
    assert result.entry_order_id == "sell-1"
    assert len(client.orders) == 1  # no restored stop on top of the live SELL


@_requires_alpaca_sdk
def test_eod_sell_submission_error_with_unreliable_lookup_fails_closed_without_a_stop():
    day_stop = _order(id="stop-day", symbol="AAPL", side="sell", qty=0.03, stop_price=340.0, status="new", time_in_force="day")
    client = RecordingTradingClient(responses=[TimeoutError("read timed out")], open_orders=[day_stop], positions=[_order(symbol="AAPL", qty="0.03", side="long")])
    client.client_lookup_error = RuntimeError("orders endpoint down")
    alpaca = _alpaca(client, paper=True)

    result = alpaca.close_position_for_eod("AAPL", 0.03, "stock", current_position_qty=0.03)

    assert not result.success
    assert result.status == "critical_unprotected_position"
    assert "NOT restored" in result.message
    assert len(client.orders) == 1
    assert result.cancelled_protective_order_ids == ["stop-day"]


@_requires_alpaca_sdk
def test_sell_submission_error_confirmed_not_accepted_still_restores_protection():
    day_stop = _order(id="stop-day", symbol="AAPL", side="sell", qty=0.03, stop_price=340.0, status="new", time_in_force="day")
    restored = _order(id="stop-restored", symbol="AAPL", side="sell", qty=0.03, stop_price=340.0, status="new", time_in_force="day")
    client = RecordingTradingClient(responses=[RuntimeError("rejected by broker"), restored], open_orders=[day_stop], positions=[_order(symbol="AAPL", qty="0.03", side="long")])
    alpaca = _alpaca(client, paper=True)

    result = alpaca.close_position_for_eod("AAPL", 0.03, "stock", current_position_qty=0.03)

    assert not result.success
    assert result.status == "sell_failed_protection_restored"
    assert result.restored_protective_order_id == "stop-restored"
    assert client.orders[1].time_in_force.value == "day"


# ── review follow-ups: BUY submission recovery and DAY-protection discovery ───

@_requires_alpaca_sdk
def test_fractional_buy_whose_submission_raised_but_was_accepted_is_recovered_and_protected():
    entry = _order(id="entry-1", symbol="AAPL", side="buy", status="filled", filled_qty=0.0288, filled_avg_price=347.0, order_class=None, legs=[])
    stop = _order(id="stop-1", symbol="AAPL", side="sell", status="new", stop_price=340.0, qty=0.0288, time_in_force="day")

    class TimeoutThenAcceptedClient(RecordingTradingClient):
        def submit_order(self, order):
            if len(self.orders) == 0:
                self.orders.append(order)
                entry.client_order_id = order.client_order_id
                self._register(entry)
                raise TimeoutError("read timed out")
            return super().submit_order(order)

    client = TimeoutThenAcceptedClient([stop])
    alpaca = _alpaca(client, paper=True)

    result = _fractional_buy(alpaca)

    assert result.success, result.message
    assert result.entry_order_id == "entry-1"
    assert result.protection_active and result.protective_order_id == "stop-1"
    assert client.orders[0].client_order_id.startswith("paper-buy-aapl-")


@_requires_alpaca_sdk
def test_buy_submission_error_with_unreliable_lookup_is_a_counted_ambiguous_entry():
    for prefer_attached, qty in ((True, 1.0), (True, 0.0288)):
        client = RecordingTradingClient([TimeoutError("read timed out")])
        client.client_lookup_error = RuntimeError("orders endpoint down")
        alpaca = _alpaca(client, paper=True, prefer_attached_stops=prefer_attached)

        result = _fractional_buy(alpaca, qty=qty)

        assert not result.success
        assert result.status == "entry_state_ambiguous"
        assert result.counts_as_trade and result.protection_failed
        assert "could not confirm" in result.message
        assert len(client.orders) == 1


@_requires_alpaca_sdk
def test_buy_submission_error_confirmed_not_accepted_is_a_plain_error():
    client = RecordingTradingClient([RuntimeError("insufficient buying power")])
    alpaca = _alpaca(client, paper=True)

    result = _fractional_buy(alpaca, qty=1.0)

    assert not result.success
    assert result.status == "error"
    assert not result.counts_as_trade
    assert "insufficient buying power" in result.message


@_requires_alpaca_sdk
def test_has_day_protection_detects_expiring_stops_and_raises_on_listing_errors():
    day_stop = _order(id="stop-day", symbol="MSFT", side="sell", qty=1.0, stop_price=400.0, status="new", time_in_force="day", type="stop")
    gtc_stop = _order(id="stop-gtc", symbol="AAPL", side="sell", qty=1.0, stop_price=340.0, status="new", time_in_force="gtc", type="stop")
    client = RecordingTradingClient([], open_orders=[day_stop, gtc_stop])
    alpaca = _alpaca(client, paper=True)

    assert alpaca.has_day_protection("MSFT")
    assert not alpaca.has_day_protection("AAPL")
    assert not alpaca.has_day_protection("NVDA")

    class BrokenOrders(RecordingTradingClient):
        def get_orders(self, filter=None):
            raise RuntimeError("orders endpoint down")

    with pytest.raises(RuntimeError, match="orders endpoint down"):
        _alpaca(BrokenOrders([]), paper=True).has_day_protection("MSFT")
    with pytest.raises(RuntimeError):
        AlpacaClient(trading_client=None, paper=True).has_day_protection("MSFT")


class _LaggingOrderListClient(RecordingTradingClient):
    """Open-orders listing keeps showing cancelled orders for a while, as Alpaca's can.

    By-id lookups stay authoritative. ``extra_after_sell`` orders appear in the listing (and by-id)
    only once the SELL has been submitted, modelling a stop the pre-SELL reconciliation never saw.
    """

    def __init__(self, *args, lagged_listings=0, extra_after_sell=None, unknown_by_id=None, fail_listings_once_extra_seen=False, failing_post_sell_listings=0, listing_failures_once_extra_seen=0, **kwargs):
        super().__init__(*args, **kwargs)
        # The next N listing requests made after the SELL is submitted raise.
        self.failing_post_sell_listings = failing_post_sell_listings
        # The next N listing requests made once an extra order has been listed raise, then listings recover.
        self.listing_failures_once_extra_seen = listing_failures_once_extra_seen
        self.lagged_listings = lagged_listings
        self.unknown_by_id = set(unknown_by_id or [])
        # Once an extra order has been listed, every later listing request raises.
        self.fail_listings_once_extra_seen = fail_listings_once_extra_seen
        self._extra_ids = {str(getattr(order, "id", "")) for order in (extra_after_sell or [])}
        self._extra_listed = False
        self.extra_after_sell = list(extra_after_sell or [])
        self.get_orders_calls = 0

    def submit_order(self, order):
        response = super().submit_order(order)
        for extra in self.extra_after_sell:
            self._register(extra, include_in_open=True)
        self.extra_after_sell = []
        return response

    def get_order_by_id(self, order_id, filter=None):
        if str(order_id) in self.unknown_by_id:
            return None
        return super().get_order_by_id(order_id, filter)

    def get_orders(self, filter=None):
        self.get_orders_calls += 1
        if self.fail_listings_once_extra_seen and self._extra_listed:
            raise RuntimeError("orders endpoint unavailable")
        if self._extra_listed and self.listing_failures_once_extra_seen > 0:
            self.listing_failures_once_extra_seen -= 1
            raise RuntimeError("orders endpoint unavailable")
        if self.orders and self.failing_post_sell_listings > 0:
            self.failing_post_sell_listings -= 1
            raise RuntimeError("orders endpoint unavailable")
        orders = super().get_orders(filter)
        if any(str(getattr(order, "id", "")) in self._extra_ids for order in orders):
            self._extra_listed = True
        if self.lagged_listings > 0:
            for order_id in self.cancelled_ids:
                lagged = self.lookup.get(order_id)
                if lagged is not None and lagged not in orders:
                    # The stale listing still reports the status the order had before cancellation.
                    orders.append(SimpleNamespace(**{**vars(lagged), "status": "new"}))
            if self.cancelled_ids:
                self.lagged_listings -= 1
        return orders


def _eod_exit_setup(**client_kwargs):
    day_stop = _order(id="stop-day", symbol="AAPL", side="sell", qty=0.0105, stop_price=325.75, status="new", time_in_force="day")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=0.0105, filled_qty=0.0105, filled_avg_price=330.93, status="filled", order_class=None, legs=[])
    client = _LaggingOrderListClient(
        responses=[sell_order],
        open_orders=[day_stop],
        positions=[_order(symbol="AAPL", qty="0.0105", side="long")],
        **client_kwargs,
    )
    client.on_submit = lambda order, response: client.positions.clear()
    sleeps = []
    alpaca = AlpacaClient(trading_client=client, sleep_fn=sleeps.append, paper=True)
    return client, alpaca, sleeps


@_requires_alpaca_sdk
def test_eod_exit_is_not_failed_by_a_listing_that_lags_a_verified_cancellation():
    # The listing still shows the cancelled stop for longer than the poll budget, but the by-id
    # lookup reports it cancelled, so the flat position is reconciled instead of flagged stale.
    client, alpaca, _ = _eod_exit_setup(lagged_listings=50)

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert result.success, result.message
    assert result.protection_reconciled
    assert not result.protection_failed
    assert result.cancelled_protective_order_ids == ["stop-day"]
    assert result.actual_remaining_position_qty == 0.0


@_requires_alpaca_sdk
def test_eod_exit_with_a_genuinely_open_stop_fails_closed_and_names_the_orders():
    stray_stop = _order(id="stop-stray", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="new", time_in_force="day")
    client, alpaca, sleeps = _eod_exit_setup(extra_after_sell=[stray_stop])

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert not result.success
    assert result.protection_failed
    assert not result.protection_reconciled
    assert result.status == "protection_failed"
    assert "stop-stray (status new)" in result.message
    assert "Cancelled before the SELL: stop-day" in result.message
    assert f"after {alpaca.cancel_poll_attempts} checks" in result.message
    # Nothing is cancelled or sold beyond the original reconciliation.
    assert client.cancelled_ids == ["stop-day"]
    assert len(client.orders) == 1
    assert "stop-stray" not in client.cancelled_ids
    assert len(sleeps) >= alpaca.cancel_poll_attempts - 1


@_requires_alpaca_sdk
def test_eod_exit_fails_closed_when_a_listed_stop_cannot_be_looked_up():
    unknown_stop = _order(id="stop-unknown", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="new", time_in_force="day")
    # The listing returns the stop, but the by-id lookup finds nothing: that is not proof it is closed.
    client, alpaca, _ = _eod_exit_setup(extra_after_sell=[unknown_stop], unknown_by_id=["stop-unknown"])

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert not result.success
    assert result.protection_failed
    assert "stop-unknown" in result.message


@_requires_alpaca_sdk
def test_full_sell_reconciles_when_only_the_listing_lags_the_cancelled_stop():
    stop_order = _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=5.0, filled_qty=5.0, filled_avg_price=101.0, status="filled", order_class=None, legs=[])
    client = _LaggingOrderListClient(responses=[sell_order], open_orders=[stop_order], lagged_listings=2)
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(symbol="AAPL", qty=5.0, side="sell", asset_type="stock", mode="trade", current_position_qty=5.0)

    assert result.success, result.message
    assert result.protection_reconciled
    assert client.cancelled_ids == ["stop-1"]


@_requires_alpaca_sdk
@pytest.mark.parametrize(
    "by_id_responses, expected_status",
    [
        pytest.param("live", "new", id="stop-still-live-by-id"),
        pytest.param("unknown", "new", id="stop-unresolvable-by-id"),
    ],
)
def test_eod_exit_keeps_an_observed_stop_unresolved_when_later_listings_fail(by_id_responses, expected_status):
    # The stop is listed once as open; every later listing errors, which list_open_orders reports
    # as an empty list. That empty list must not clear a stop that was never confirmed terminal.
    stray_stop = _order(id="stop-stray", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="new", time_in_force="day")
    client, alpaca, _ = _eod_exit_setup(
        extra_after_sell=[stray_stop],
        fail_listings_once_extra_seen=True,
        unknown_by_id=["stop-stray"] if by_id_responses == "unknown" else None,
    )

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert client._extra_listed
    assert not result.success
    assert result.protection_failed
    assert not result.protection_reconciled
    assert f"stop-stray (status {expected_status})" in result.message
    assert client.cancelled_ids == ["stop-day"]
    assert len(client.orders) == 1


@_requires_alpaca_sdk
def test_eod_exit_clears_an_observed_stop_only_once_its_by_id_lookup_is_terminal():
    # Listed open on the first check, then a listing error, then listings recover without it: the
    # retained stop is refreshed by id and the exit reconciles once that lookup reports it cancelled.
    stray_stop = _order(id="stop-stray", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="new", time_in_force="day")
    cancelled_stray = _order(id="stop-stray", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="canceled", time_in_force="day")
    client, alpaca, _ = _eod_exit_setup(extra_after_sell=[stray_stop], listing_failures_once_extra_seen=1)
    client.order_sequences["stop-stray"] = [stray_stop, cancelled_stray]

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert client._extra_listed
    assert client.listing_failures_once_extra_seen == 0
    assert result.success, result.message
    assert result.protection_reconciled
    assert not result.protection_failed


@_requires_alpaca_sdk
def test_eod_exit_keeps_an_observed_non_protective_sell_unresolved_when_later_listings_fail():
    # A non-protective open SELL is seen once after the exit; every later listing errors. It must
    # stay tracked by id rather than being dropped with the warning, and the exit fails closed.
    stray_sell = _order(id="sell-stray", symbol="AAPL", side="sell", qty=0.0105, status="new", order_class=None, legs=[])
    client, alpaca, _ = _eod_exit_setup(extra_after_sell=[stray_sell], fail_listings_once_extra_seen=True)

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert client._extra_listed
    assert not result.success
    assert result.protection_failed
    assert not result.protection_reconciled
    assert "non-protective open sell order(s) remained after closing AAPL: sell-stray (status new)" in result.message
    assert client.cancelled_ids == ["stop-day"]
    assert len(client.orders) == 1


@_requires_alpaca_sdk
def test_eod_exit_clears_a_lagging_non_protective_sell_once_its_by_id_lookup_is_terminal():
    # The listing briefly shows a SELL that the by-id lookup then reports filled (for example the
    # exit order itself lagging in the listing): it is cleared instead of failing the cleanup.
    lagging_sell = _order(id="sell-lagging", symbol="AAPL", side="sell", qty=0.0105, status="new", order_class=None, legs=[])
    filled_sell = _order(id="sell-lagging", symbol="AAPL", side="sell", qty=0.0105, status="filled", order_class=None, legs=[])
    client, alpaca, _ = _eod_exit_setup(extra_after_sell=[lagging_sell])
    client.order_sequences["sell-lagging"] = [lagging_sell, filled_sell]

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert client._extra_listed
    assert result.success, result.message
    assert result.protection_reconciled
    assert not result.protection_failed


@_requires_alpaca_sdk
def test_eod_exit_retries_a_failed_first_listing_instead_of_treating_it_as_no_orders():
    # The first post-exit listing errors (read as an empty list by list_open_orders). The check must
    # retry rather than reconcile, and the next listing reveals a live stray stop.
    stray_stop = _order(id="stop-stray", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="new", time_in_force="day")
    client, alpaca, _ = _eod_exit_setup(extra_after_sell=[stray_stop], failing_post_sell_listings=1)

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert client.failing_post_sell_listings == 0
    assert client._extra_listed
    assert not result.success
    assert result.protection_failed
    assert "stop-stray (status new)" in result.message


@_requires_alpaca_sdk
def test_eod_exit_reconciles_after_a_failed_first_listing_once_a_clean_listing_is_obtained():
    client, alpaca, _ = _eod_exit_setup(failing_post_sell_listings=1)

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert client.failing_post_sell_listings == 0
    assert result.success, result.message
    assert result.protection_reconciled


@_requires_alpaca_sdk
def test_eod_exit_fails_closed_when_no_reliable_listing_is_ever_obtained():
    client, alpaca, _ = _eod_exit_setup(failing_post_sell_listings=10_000)

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert not result.success
    assert result.protection_failed
    assert not result.protection_reconciled
    assert "open orders for AAPL could not be listed reliably" in result.message
    assert client.cancelled_ids == ["stop-day"]
    assert len(client.orders) == 1


@_requires_alpaca_sdk
def test_eod_exit_fails_closed_when_a_stray_fill_flips_the_position_short():
    # A stray stop is seen open after the exit, then fills while the check polls. Its by-id status is
    # terminal, but the fill left the account short, so the exit must not be reported as flat.
    stray_stop = _order(id="stop-stray", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="new", time_in_force="day")
    filled_stray = _order(id="stop-stray", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="filled", time_in_force="day")
    client, alpaca, _ = _eod_exit_setup(extra_after_sell=[stray_stop])
    client.order_sequences["stop-stray"] = [stray_stop, filled_stray]
    by_id = client.get_order_by_id

    def get_order_by_id_with_fill(order_id, filter=None):
        order = by_id(order_id, filter)
        if str(order_id) == "stop-stray" and getattr(order, "status", None) == "filled":
            client.positions[:] = [_order(symbol="AAPL", qty="-0.0105", side="short")]
        return order

    client.get_order_by_id = get_order_by_id_with_fill

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert client._extra_listed
    assert not result.success
    assert result.protection_failed
    assert not result.protection_reconciled
    assert "not flat after the exit (signed quantity -0.0105)" in result.message


def _with_position_reads(alpaca, reads):
    """Make the post-exit signed position check return ``reads`` in turn (the last one repeats)."""
    remaining = list(reads)
    calls = []

    def signed_position_qty(symbol):
        calls.append(symbol)
        return remaining.pop(0) if len(remaining) > 1 else remaining[0]

    alpaca._signed_position_qty = signed_position_qty
    return calls


@_requires_alpaca_sdk
def test_eod_exit_retries_a_long_position_read_that_lags_the_exit_fill():
    # The position endpoint briefly still shows the sold long quantity; that is lag, not a stray
    # fill (a SELL fill can only move the position down), so the check retries and reconciles.
    client, alpaca, _ = _eod_exit_setup()
    calls = _with_position_reads(alpaca, [0.0105, 0.0])

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert len(calls) == 2
    assert result.success, result.message
    assert result.protection_reconciled


@_requires_alpaca_sdk
def test_eod_exit_fails_closed_when_a_long_position_never_reads_flat():
    client, alpaca, _ = _eod_exit_setup()
    calls = _with_position_reads(alpaca, [0.0105])

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert len(calls) == alpaca.cancel_poll_attempts
    assert not result.success
    assert result.protection_failed
    assert f"is not flat after the exit (signed quantity 0.0105) after {alpaca.cancel_poll_attempts} checks" in result.message


@_requires_alpaca_sdk
def test_eod_exit_fails_closed_when_the_position_cannot_be_read():
    client, alpaca, _ = _eod_exit_setup()
    calls = _with_position_reads(alpaca, [None])

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert len(calls) == alpaca.cancel_poll_attempts
    assert not result.success
    assert result.protection_failed
    assert "broker position for AAPL could not be verified flat after the exit" in result.message


@_requires_alpaca_sdk
def test_eod_exit_treats_a_replaced_order_as_done():
    # A tracked stop is replaced during the check: its old id can no longer fill, so it is done.
    stray_stop = _order(id="stop-stray", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="new", time_in_force="day")
    replaced_stray = _order(id="stop-stray", symbol="AAPL", side="sell", qty=0.0105, stop_price=320.0, status="replaced", time_in_force="day")
    client, alpaca, _ = _eod_exit_setup(extra_after_sell=[stray_stop])
    client.order_sequences["stop-stray"] = [stray_stop, replaced_stray]

    result = alpaca.close_position_for_eod("AAPL", 0.0105, "stock", current_position_qty=0.0105)

    assert client._extra_listed
    assert result.success, result.message
    assert result.protection_reconciled


def test_signed_position_qty_keeps_shorts_negative_and_reports_unreadable_positions():
    class Positions:
        def __init__(self, positions=None, error=None):
            self.positions = positions or []
            self.error = error

        def get_open_position(self, symbol):
            raise self.error or RuntimeError("position not found")

        def get_all_positions(self):
            if self.error:
                raise self.error
            return list(self.positions)

    short = _order(symbol="BTCUSD", qty="-0.5", side="short")
    assert AlpacaClient(trading_client=Positions([short]), paper=True)._signed_position_qty("BTC/USD") == -0.5
    assert AlpacaClient(trading_client=Positions([short]), paper=True).get_position_qty("BTC/USD") == 0.0
    assert AlpacaClient(trading_client=Positions(), paper=True)._signed_position_qty("AAPL") == 0.0
    unreadable = AlpacaClient(trading_client=Positions(error=RuntimeError("positions endpoint down")), paper=True)
    assert unreadable._signed_position_qty("AAPL") is None
    assert unreadable.get_position_qty("AAPL") is None
    no_qty = AlpacaClient(trading_client=Positions([_order(symbol="BTCUSD", side="long")]), paper=True)
    assert no_qty._signed_position_qty("BTC/USD") is None
    assert no_qty.get_position_qty("BTC/USD") == 0.0


def test_get_position_skips_the_full_scan_for_a_flat_equity_but_not_for_crypto():
    class CountingPositions:
        def __init__(self):
            self.full_scans = 0

        def get_open_position(self, symbol):
            raise RuntimeError("position does not exist")

        def get_all_positions(self):
            self.full_scans += 1
            return [_order(symbol="BTCUSD", qty="0.1", side="long")]

    client = CountingPositions()
    alpaca = AlpacaClient(trading_client=client, paper=True)

    assert alpaca.get_position("AAPL") is None
    assert client.full_scans == 0
    assert alpaca.get_position("BTC/USD").qty == "0.1"
    assert client.full_scans == 1


@_requires_alpaca_sdk
def test_sell_is_blocked_when_open_orders_cannot_be_listed_before_the_exit():
    class BrokenListing(RecordingTradingClient):
        def get_orders(self, filter=None):
            raise RuntimeError("orders endpoint unavailable")

    stop_order = _order(id="stop-1", symbol="AAPL", side="sell", qty=5.0, stop_price=95.0, status="new")
    client = BrokenListing(responses=[], open_orders=[stop_order])
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(symbol="AAPL", qty=5.0, side="sell", asset_type="stock", mode="trade", current_position_qty=5.0)

    assert not result.success
    assert result.status == "protection_reconciliation_failed"
    assert "could not be listed reliably" in result.message
    assert client.orders == []
    assert client.cancelled_ids == []


@_requires_alpaca_sdk
def test_is_order_open_counts_a_failed_listing_as_open():
    class BrokenListing(RecordingTradingClient):
        def get_orders(self, filter=None):
            raise RuntimeError("orders endpoint unavailable")

    assert _alpaca(BrokenListing(), paper=True)._is_order_open("stop-1", "AAPL")
    assert not _alpaca(RecordingTradingClient(), paper=True)._is_order_open("stop-1", "AAPL")


@_requires_alpaca_sdk
def test_partial_sell_fails_closed_when_stacked_stops_cannot_be_ruled_out():
    class ListingFailsAfterReplacement(RecordingTradingClient):
        def get_orders(self, filter=None):
            if len(self.orders) >= 2:
                raise RuntimeError("orders endpoint unavailable")
            return super().get_orders(filter)

    old_stop = _order(id="stop-old", symbol="AAPL", side="sell", qty=10.0, stop_price=95.0, status="new")
    sell_order = _order(id="sell-1", symbol="AAPL", side="sell", qty=4.0, filled_qty=4.0, filled_avg_price=101.0, status="filled", order_class=None, legs=[])
    replacement_stop = _order(id="stop-new", symbol="AAPL", side="sell", qty=6.0, stop_price=95.0, status="new")
    client = ListingFailsAfterReplacement(
        responses=[sell_order, replacement_stop],
        open_orders=[old_stop],
        positions=[_order(symbol="AAPL", qty="6", side="long")],
    )
    alpaca = _alpaca(client, paper=True, prefer_attached_stops=True)

    result = alpaca.place_paper_trade(symbol="AAPL", qty=4.0, side="sell", asset_type="stock", mode="trade", current_position_qty=10.0)

    assert len(client.orders) == 2
    assert not result.success
    assert result.protection_failed
    assert result.status == "critical_unprotected_position"
    assert "stacked stops cannot be ruled out" in result.message
