from types import SimpleNamespace

from src.alpaca_client import AlpacaClient


class RecordingTradingClient:
    def __init__(self, responses=None, open_orders=None, cancel_fail_ids=None, order_sequences=None, positions=None):
        self.responses = list(responses or [])
        self.orders = []
        self.lookup = {}
        self.open_orders = []
        self.cancelled_ids = []
        self.cancel_fail_ids = set(cancel_fail_ids or [])
        self.order_sequences = {str(order_id): list(sequence) for order_id, sequence in (order_sequences or {}).items()}
        self.positions = list(positions or [])

        for order in open_orders or []:
            self._register(order, include_in_open=True)

    def submit_order(self, order):
        self.orders.append(order)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response

        if getattr(response, "symbol", None) is None:
            response.symbol = getattr(order, "symbol", None)
        if getattr(response, "qty", None) is None:
            response.qty = getattr(order, "qty", None)
        if getattr(response, "side", None) is None:
            response.side = getattr(order, "side", None)
        if getattr(response, "stop_price", None) is None and getattr(order, "stop_price", None) is not None:
            response.stop_price = getattr(order, "stop_price")

        self._register(response)
        return response

    def get_order_by_id(self, order_id, filter=None):
        sequence = self.order_sequences.get(str(order_id))
        if sequence:
            if len(sequence) > 1:
                return sequence.pop(0)
            return sequence[0]
        return self.lookup.get(str(order_id))

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


