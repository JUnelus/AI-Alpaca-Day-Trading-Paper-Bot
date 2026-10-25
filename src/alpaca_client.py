from __future__ import annotations

import math
import os
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from .execution_models import ExecutionResult
from .risk_manager import uses_fractional_quantity

_EQUITY_ASSET_TYPES = {"stock", "etf"}
# Alpaca only accepts fractional equity orders as DAY orders, so a fractional entry's
# protective stop expires at the close instead of persisting like the GTC whole-share stop.
_FRACTIONAL_ENTRY_ACTIVE_STATUSES = {"accepted", "new", "pending_new", "partially_filled", "held", "open"}
_FRACTIONAL_ENTRY_CANCEL_PENDING_STATUSES = {"pending_cancel"}
_FRACTIONAL_ENTRY_NO_FILL_TERMINAL_STATUSES = {"canceled", "cancelled", "rejected", "expired"}
_EXIT_TERMINAL_STATUSES = {"filled", "canceled", "cancelled", "rejected", "expired"}
# Only these broker statuses prove a standalone stop is resting at the broker; transitional
# (pending_new / pending_cancel) or missing statuses keep polling instead of counting as protection.
_ACTIVE_STOP_STATUSES = {"accepted", "new", "held", "open", "partially_filled"}
# Minutes before the exchange close in which the EOD cleanup acts and new fractional entries are
# refused: an entry accepted inside it has no later cleanup run, so its DAY stop would expire naked.
DEFAULT_FRACTIONAL_EOD_WINDOW_MINUTES = 30

try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.enums import OrderClass, OrderSide, QueryOrderStatus, TimeInForce
    from alpaca.trading.requests import (
        GetOrderByIdRequest,
        GetOrdersRequest,
        MarketOrderRequest,
        StopLossRequest,
        StopOrderRequest,
    )
except Exception:  # pragma: no cover - import guarded for local runs without deps
    TradingClient = None
    OrderClass = None
    OrderSide = None
    QueryOrderStatus = None
    TimeInForce = None
    GetOrderByIdRequest = None
    GetOrdersRequest = None
    MarketOrderRequest = None
    StopLossRequest = None
    StopOrderRequest = None


@dataclass
class AccountSnapshot:
    equity: float
    cash: float
    buying_power: float = 0.0  # actual available buying power — may differ from cash


@dataclass
class BrokerAsset:
    symbol: str
    tradable: bool = False
    fractionable: bool = False


@dataclass
class MarketClock:
    is_open: bool
    timestamp: datetime
    next_close: datetime

    @property
    def minutes_to_close(self) -> float:
        return (self.next_close - self.timestamp).total_seconds() / 60.0


def _clock_datetime(value: object) -> Optional[datetime]:
    """Accept only an unambiguous timezone-aware broker clock instant."""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        return None
    return value


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        return int(float(raw))
    except (TypeError, ValueError):
        return default


class AlpacaClient:
    def __init__(
        self,
        trading_client: Optional[Any] = None,
        paper: Optional[bool] = None,
        prefer_attached_stops: bool = True,
        sleep_fn: Optional[Any] = None,
        cancel_poll_attempts: int = 5,
        stop_confirmation_poll_attempts: int = 5,
        protection_retries: int = 3,
        poll_delay_seconds: float = 0.5,
        entry_fill_poll_attempts: int = 3,
        exit_fill_poll_attempts: int = 3,
        fractional_eod_window_minutes: Optional[int] = None,
    ) -> None:
        api_key = os.getenv("ALPACA_API_KEY")
        secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.paper = paper if paper is not None else os.getenv("ALPACA_PAPER", "true").lower() == "true"
        self.prefer_attached_stops = prefer_attached_stops
        self._client: Optional[Any] = trading_client
        self.sleep_fn = sleep_fn or time.sleep
        self.cancel_poll_attempts = max(1, int(cancel_poll_attempts))
        self.stop_confirmation_poll_attempts = max(1, int(stop_confirmation_poll_attempts))
        # Bounded fill window for a fractional DAY entry before any unfilled remainder is cancelled.
        self.entry_fill_poll_attempts = max(1, int(entry_fill_poll_attempts))
        # Bounded fill window for an EOD market SELL before it is cancelled and its terminal state confirmed.
        self.exit_fill_poll_attempts = max(1, int(exit_fill_poll_attempts))
        if fractional_eod_window_minutes is None:
            fractional_eod_window_minutes = _env_int("FRACTIONAL_EOD_WINDOW_MINUTES", DEFAULT_FRACTIONAL_EOD_WINDOW_MINUTES)
        self.fractional_eod_window_minutes = max(1, int(fractional_eod_window_minutes))
        self.protection_retries = max(1, int(protection_retries))
        self.poll_delay_seconds = max(0.0, float(poll_delay_seconds))

        if self._client is None and TradingClient and api_key and secret_key and self.paper:
            self._client = TradingClient(api_key, secret_key, paper=True)

    @property
    def is_ready(self) -> bool:
        return self._client is not None

    def get_account_snapshot(self) -> AccountSnapshot:
        if not self._client:
            # Safe fallback for local dry runs.
            return AccountSnapshot(equity=10000.0, cash=10000.0, buying_power=10000.0)

        client = self._client
        assert client is not None
        account = client.get_account()
        return AccountSnapshot(
            equity=float(account.equity),
            cash=float(account.cash),
            buying_power=float(account.buying_power),
        )

    def list_positions(self) -> list:
        if not self._client:
            return []
        client = self._client
        assert client is not None
        try:
            return list(client.get_all_positions())
        except Exception:
            return []

    def list_positions_strict(self) -> list:
        """Return broker positions or raise; destructive EOD work must distinguish errors from flat."""
        if not self._client:
            raise RuntimeError("No Alpaca client available for position discovery.")
        return list(self._client.get_all_positions())

    def get_market_clock(self) -> MarketClock:
        """Read Alpaca's market clock; any unusable value raises so callers fail closed."""
        if not self._client or not hasattr(self._client, "get_clock"):
            raise RuntimeError("Alpaca market clock is unavailable.")
        clock = self._client.get_clock()
        is_open = getattr(clock, "is_open", None)
        timestamp = _clock_datetime(getattr(clock, "timestamp", None))
        next_close = _clock_datetime(getattr(clock, "next_close", None))
        if not isinstance(is_open, bool) or timestamp is None or next_close is None:
            raise RuntimeError("Alpaca market clock did not provide a usable is_open flag, timestamp and next_close.")
        return MarketClock(is_open=is_open, timestamp=timestamp, next_close=next_close)

    def eod_cleanup_window(self) -> dict[str, Any]:
        """Classify now against the pre-close cleanup window using only the broker's clock.

        ``state`` is ``in_window`` (act now), ``before_window`` (too early; a later run covers it),
        ``closed`` (the session is over, nothing can be sold safely) or ``unavailable`` (the clock
        could not be read, which proves nothing and must be treated as a failure).
        """
        try:
            clock = self.get_market_clock()
        except Exception as exc:
            return {"state": "unavailable", "minutes_to_close": None, "message": f"Alpaca market clock could not be read: {exc}"}
        if not clock.is_open:
            return {
                "state": "closed",
                "minutes_to_close": None,
                "message": "The exchange is closed, so a DAY market SELL could not execute before this session's DAY stops expire.",
            }
        minutes_to_close = clock.minutes_to_close
        if minutes_to_close <= 0:
            return {"state": "closed", "minutes_to_close": minutes_to_close, "message": "Alpaca reports the session close has already passed."}
        if minutes_to_close > self.fractional_eod_window_minutes:
            return {
                "state": "before_window",
                "minutes_to_close": minutes_to_close,
                "message": (
                    f"{minutes_to_close:.0f} minutes remain before the close, outside the "
                    f"{self.fractional_eod_window_minutes}-minute EOD cleanup window."
                ),
            }
        return {"state": "in_window", "minutes_to_close": minutes_to_close, "message": None}

    def _fractional_entry_cutoff_error(self) -> Optional[str]:
        """Refuse a fractional DAY entry too close to the exchange close to be cleaned up.

        Fractional equity is protected by a DAY stop that expires at the close and relies on the EOD
        cleanup run to exit it. Inside the cleanup's pre-close window no later run exists, so the
        entry would be left unprotected overnight. An unreadable clock cannot prove otherwise.
        """
        window = self.eod_cleanup_window()
        state = window["state"]
        if state == "unavailable":
            return f"Fractional entry blocked: {window['message']} EOD cleanup coverage cannot be proven."
        if state == "closed":
            return "Fractional entry blocked: the exchange is closed, so this day's EOD cleanup can no longer exit a DAY stop."
        if state == "in_window":
            return (
                f"Fractional entry blocked: only {window['minutes_to_close']:.0f} minutes remain before the exchange close, "
                f"inside the {self.fractional_eod_window_minutes}-minute EOD cleanup window, so its expiring DAY "
                "stop would not be exited."
            )
        return None

    def get_position(self, symbol: str):
        if not self._client:
            return None
        client = self._client
        assert client is not None
        try:
            return client.get_open_position(symbol)
        except Exception:
            try:
                for position in list(client.get_all_positions()):
                    if self._normalize_symbol(getattr(position, "symbol", "")) == self._normalize_symbol(symbol):
                        return position
            except Exception:
                return False
            return None

    def get_position_qty(self, symbol: str) -> Optional[float]:
        position = self.get_position(symbol)
        if position is False:
            return None
        if position is None:
            return 0.0

        qty = self._safe_float(getattr(position, "qty", 0.0))
        side = self._enum_or_value(getattr(position, "side", None))
        if side == "short":
            qty = -abs(qty)
        return max(0.0, qty)

    def get_asset(self, symbol: str) -> BrokerAsset:
        """Broker view of an asset; any lookup failure reads as not tradable / not fractionable (fail closed)."""
        if not self._client:
            return BrokerAsset(symbol=symbol)
        try:
            asset = self._client.get_asset(symbol)
        except Exception:
            return BrokerAsset(symbol=symbol)
        return BrokerAsset(
            symbol=symbol,
            tradable=bool(getattr(asset, "tradable", False)),
            fractionable=bool(getattr(asset, "fractionable", False)),
        )

    def can_place_protected_buy(self, asset_type: str, allow_fractional: bool = False) -> bool:
        if asset_type not in _EQUITY_ASSET_TYPES:
            return False
        if allow_fractional:
            # Fractional equity entries cannot use the attached GTC/OTO route; they need the
            # simple market entry followed by a standalone DAY stop.
            return all((self.paper, self.is_ready, MarketOrderRequest, StopOrderRequest, GetOrderByIdRequest, TimeInForce, OrderSide))
        if self.prefer_attached_stops:
            return all((self.paper, self.is_ready, MarketOrderRequest, OrderClass, StopLossRequest, GetOrderByIdRequest))
        return all((self.paper, self.is_ready, MarketOrderRequest, StopOrderRequest, GetOrderByIdRequest))

    def place_paper_trade(
        self,
        symbol: str,
        qty: float,
        side: str,
        asset_type: str,
        mode: str = "trade",
        stop_loss: Optional[float] = None,
        current_position_qty: float = 0.0,
    ) -> ExecutionResult:
        side_normalized = side.lower()

        if mode != "trade":
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side=side_normalized,
                requested_qty=qty,
                status="blocked_mode",
                message="Report mode cannot place broker orders.",
                asset_type=asset_type,
                stop_price=stop_loss,
            )

        if not self.paper:
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side=side_normalized,
                requested_qty=qty,
                status="rejected_live_disabled",
                message="Paper trading is required for this bot.",
                asset_type=asset_type,
                stop_price=stop_loss,
            )

        if not self._client:
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side=side_normalized,
                requested_qty=qty,
                status="skipped",
                message="No Alpaca credentials available; dry-run only.",
                asset_type=asset_type,
                stop_price=stop_loss,
            )

        if side_normalized == "buy":
            if asset_type not in {"stock", "etf"}:
                return ExecutionResult(
                    success=False,
                    symbol=symbol,
                    side=side_normalized,
                    requested_qty=qty,
                    status="rejected_unprotected_asset",
                    message="BUY rejected: unable to guarantee Alpaca protective stop support for this asset type.",
                    asset_type=asset_type,
                    stop_price=stop_loss,
                )
            if stop_loss is None or stop_loss <= 0:
                return ExecutionResult(
                    success=False,
                    symbol=symbol,
                    side=side_normalized,
                    requested_qty=qty,
                    status="rejected_invalid_stop",
                    message="BUY rejected: a valid protective stop price is required.",
                    asset_type=asset_type,
                    stop_price=stop_loss,
                )
            if uses_fractional_quantity(asset_type, qty):
                if not self.get_asset(symbol).fractionable:
                    return ExecutionResult(
                        success=False,
                        symbol=symbol,
                        side=side_normalized,
                        requested_qty=qty,
                        status="rejected_fractional_unsupported",
                        message="BUY rejected: Alpaca does not report this asset as fractionable, so a fractional entry cannot be placed.",
                        asset_type=asset_type,
                        stop_price=stop_loss,
                    )
                cutoff_error = self._fractional_entry_cutoff_error()
                if cutoff_error:
                    return ExecutionResult(
                        success=False,
                        symbol=symbol,
                        side=side_normalized,
                        requested_qty=qty,
                        status="fractional_entry_after_eod_cutoff",
                        message=cutoff_error,
                        asset_type=asset_type,
                        stop_price=stop_loss,
                    )
                return self._place_fractional_entry_then_day_stop_buy(symbol=symbol, qty=qty, stop_loss=stop_loss, asset_type=asset_type)
            if self.prefer_attached_stops and all((MarketOrderRequest, OrderClass, StopLossRequest, GetOrderByIdRequest)):
                return self._place_attached_protected_buy(symbol=symbol, qty=qty, stop_loss=stop_loss, asset_type=asset_type)
            return self._place_entry_then_stop_buy(symbol=symbol, qty=qty, stop_loss=stop_loss, asset_type=asset_type)

        if side_normalized == "sell":
            return self._place_exit_sell(
                symbol=symbol,
                qty=qty,
                asset_type=asset_type,
                current_position_qty=current_position_qty,
            )

        return ExecutionResult(
            success=False,
            symbol=symbol,
            side=side_normalized,
            requested_qty=qty,
            status="rejected_invalid_side",
            message=f"Unsupported trade side: {side}.",
            asset_type=asset_type,
            stop_price=stop_loss,
        )

    def _place_attached_protected_buy(self, symbol: str, qty: float, stop_loss: float, asset_type: str) -> ExecutionResult:
        client = self._client
        if client is None:
            return ExecutionResult(False, symbol, "buy", qty, status="skipped", message="No Alpaca client available.", asset_type=asset_type, stop_price=stop_loss)
        assert client is not None
        order = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC,
            order_class=OrderClass.OTO,
            stop_loss=StopLossRequest(stop_price=stop_loss),
        )
        try:
            submitted_order = client.submit_order(order)
        except Exception as exc:
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="buy",
                requested_qty=qty,
                status="error",
                message=str(exc),
                asset_type=asset_type,
                stop_price=stop_loss,
            )

        confirmation = self._poll_for_attached_stop(
            order_id=self._order_identifier(submitted_order),
            symbol=symbol,
            expected_stop_price=stop_loss,
            expected_max_qty=qty,
        )
        full_order = confirmation["order"] or submitted_order
        entry_order_id = self._order_identifier(full_order) or self._order_identifier(submitted_order)
        stop_leg = confirmation["stop_leg"]
        protective_order_id = self._order_identifier(stop_leg)
        filled_qty = max(self._safe_float(getattr(submitted_order, "filled_qty", 0.0)), self._safe_float(getattr(full_order, "filled_qty", 0.0)))
        filled_avg_price = self._safe_optional_float(
            getattr(full_order, "filled_avg_price", None),
            fallback=getattr(submitted_order, "filled_avg_price", None),
        )
        order_class = self._order_class_value(full_order) or self._order_class_value(submitted_order)
        status = self._status_value(full_order) or self._status_value(submitted_order) or "accepted"
        protection_active = confirmation["ok"] and stop_leg is not None and protective_order_id is not None

        if not protection_active:
            exposed_qty = filled_qty if filled_qty > 0 else qty
            message = (
                f"CRITICAL: BUY filled but protective stop could not be confirmed for {symbol}; "
                f"exposed quantity={exposed_qty:g}; stop_price={stop_loss:.2f}."
            )
            print(message)
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="buy",
                requested_qty=qty,
                filled_qty=filled_qty,
                filled_avg_price=filled_avg_price,
                entry_order_id=entry_order_id,
                protective_order_id=protective_order_id,
                protection_active=False,
                protection_failed=True,
                counts_as_trade=self._counts_as_trade(status) or filled_qty > 0.0,
                status="protection_failed",
                message=confirmation["message"] or message,
                stop_price=stop_loss,
                asset_type=asset_type,
                order_class=order_class,
                stop_confirmation_poll_attempts=confirmation["attempts"],
            )

        return ExecutionResult(
            success=True,
            symbol=symbol,
            side="buy",
            requested_qty=qty,
            filled_qty=filled_qty,
            filled_avg_price=filled_avg_price,
            entry_order_id=entry_order_id,
            protective_order_id=protective_order_id,
            protection_active=True,
            protection_failed=False,
            counts_as_trade=self._counts_as_trade(status),
            status=status,
            message="Protected BUY submitted to Alpaca with broker-side stop loss.",
            stop_price=stop_loss,
            asset_type=asset_type,
            order_class=order_class,
            stop_confirmation_poll_attempts=confirmation["attempts"],
        )

    def _place_fractional_entry_then_day_stop_buy(self, symbol: str, qty: float, stop_loss: float, asset_type: str) -> ExecutionResult:
        """Fractional equities cannot use Alpaca's GTC/OTO route; the DAY stop expires at the close."""
        if not all((MarketOrderRequest, StopOrderRequest, TimeInForce, OrderSide)):
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="buy",
                requested_qty=qty,
                status="rejected_unprotected_asset",
                message="BUY rejected: Alpaca order primitives for a fractional DAY entry with a protective stop are unavailable.",
                asset_type=asset_type,
                stop_price=stop_loss,
            )
        return self._place_entry_then_stop_buy(
            symbol=symbol,
            qty=qty,
            stop_loss=stop_loss,
            asset_type=asset_type,
            stop_time_in_force=TimeInForce.DAY,
            requires_eod_exit=True,
        )

    def _place_entry_then_stop_buy(
        self,
        symbol: str,
        qty: float,
        stop_loss: float,
        asset_type: str,
        stop_time_in_force=None,
        requires_eod_exit: bool = False,
    ) -> ExecutionResult:
        client = self._client
        if client is None:
            return ExecutionResult(False, symbol, "buy", qty, status="skipped", message="No Alpaca client available.", asset_type=asset_type, stop_price=stop_loss)
        assert client is not None
        stop_time_in_force = stop_time_in_force or TimeInForce.GTC
        protection_tif = "day" if requires_eod_exit else "gtc"
        entry_order = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
        )
        try:
            submitted_entry = client.submit_order(entry_order)
        except Exception as exc:
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="buy",
                requested_qty=qty,
                status="error",
                message=str(exc),
                stop_price=stop_loss,
                asset_type=asset_type,
                protection_time_in_force=protection_tif,
                requires_eod_exit=requires_eod_exit,
            )

        entry_order_id = self._order_identifier(submitted_entry)
        if requires_eod_exit:
            entry_completion = self._await_fractional_entry_terminal(entry_order_id, symbol, submitted_entry)
        else:
            refreshed = self._refresh_order(entry_order_id, nested=False) or submitted_entry
            entry_completion = {
                "ok": True, "order": refreshed, "attempts": 1, "cancel_attempted": False,
                "cancel_confirmed": False, "terminal_status": self._status_value(refreshed), "message": None,
            }
        refreshed_entry = entry_completion["order"] or submitted_entry
        filled_qty = max(
            self._safe_float(getattr(submitted_entry, "filled_qty", 0.0)),
            self._safe_float(getattr(refreshed_entry, "filled_qty", 0.0)),
        )
        filled_avg_price = self._safe_optional_float(
            getattr(refreshed_entry, "filled_avg_price", None),
            fallback=getattr(submitted_entry, "filled_avg_price", None),
        )
        entry_status = (
            entry_completion["terminal_status"]
            or self._status_value(refreshed_entry)
            or self._status_value(submitted_entry)
            or "accepted"
        )

        if not entry_completion["ok"]:
            print(entry_completion["message"])
            # The order may still execute, so it must reserve its trade slot, cash and exposure
            # as if the full requested quantity had filled; otherwise later BUYs in the same run
            # could exceed the daily, cash or exposure limits once it fills.
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="buy",
                requested_qty=qty,
                filled_qty=filled_qty,
                filled_avg_price=filled_avg_price,
                entry_order_id=entry_order_id,
                protection_active=False,
                protection_failed=True,
                counts_as_trade=True,
                status="entry_state_ambiguous",
                message=entry_completion["message"],
                stop_price=stop_loss,
                asset_type=asset_type,
                order_class="simple",
                protection_time_in_force=protection_tif,
                requires_eod_exit=requires_eod_exit,
                entry_poll_attempts=entry_completion["attempts"],
                entry_cancel_attempted=entry_completion["cancel_attempted"],
                entry_cancel_confirmed=entry_completion["cancel_confirmed"],
                terminal_entry_status=entry_status,
            )

        if filled_qty <= 0.0:
            if not requires_eod_exit:
                message = (
                    f"CRITICAL: entry for {symbol} was accepted without a fill quantity, so the protective stop could not be created."
                )
                print(message)
                return ExecutionResult(
                    success=False,
                    symbol=symbol,
                    side="buy",
                    requested_qty=qty,
                    filled_qty=filled_qty,
                    filled_avg_price=filled_avg_price,
                    entry_order_id=entry_order_id,
                    protection_active=False,
                    protection_failed=True,
                    counts_as_trade=self._counts_as_trade(entry_status),
                    status="protection_failed",
                    message=message,
                    stop_price=stop_loss,
                    asset_type=asset_type,
                    order_class="simple",
                )
            deliberate_cancel = (
                entry_status in {"canceled", "cancelled"}
                and entry_completion["cancel_attempted"]
                and entry_completion["cancel_confirmed"]
            )
            message = (
                "Fractional entry was deliberately cancelled with zero fill; no protective stop was required."
                if deliberate_cancel
                else f"CRITICAL: fractional entry for {symbol} reached terminal status '{entry_status}' with zero fill."
            )
            if not deliberate_cancel:
                print(message)
            return ExecutionResult(
                success=deliberate_cancel,
                symbol=symbol,
                side="buy",
                requested_qty=qty,
                filled_qty=filled_qty,
                filled_avg_price=filled_avg_price,
                entry_order_id=entry_order_id,
                protection_active=False,
                protection_failed=entry_status in {"rejected", "expired"},
                counts_as_trade=False,
                status="entry_canceled_no_fill" if deliberate_cancel else f"entry_{entry_status}",
                message=message,
                stop_price=stop_loss,
                asset_type=asset_type,
                order_class="simple",
                protection_time_in_force=protection_tif,
                requires_eod_exit=requires_eod_exit,
                entry_poll_attempts=entry_completion["attempts"],
                entry_cancel_attempted=entry_completion["cancel_attempted"],
                entry_cancel_confirmed=entry_completion["cancel_confirmed"],
                terminal_entry_status=entry_status,
            )

        stop_qty = min(qty, filled_qty)
        fractional_entry = requires_eod_exit
        if fractional_entry and not uses_fractional_quantity(asset_type, stop_qty):
            # A fractional request that filled to a whole-share quantity can carry a GTC stop like
            # any whole-share position, so it is not left to the EOD cleanup's quantity filter.
            stop_time_in_force = TimeInForce.GTC
            protection_tif = "gtc"
            requires_eod_exit = False
        stop_order = StopOrderRequest(
            symbol=symbol,
            qty=stop_qty,
            side=OrderSide.SELL,
            time_in_force=stop_time_in_force,
            stop_price=stop_loss,
        )
        try:
            submitted_stop = client.submit_order(stop_order)
        except Exception as exc:
            message = (
                f"CRITICAL: protective stop placement failed for {symbol}; exposed quantity={stop_qty:g}; error={exc}"
            )
            print(message)
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="buy",
                requested_qty=qty,
                filled_qty=filled_qty,
                filled_avg_price=filled_avg_price,
                entry_order_id=entry_order_id,
                protection_active=False,
                protection_failed=True,
                counts_as_trade=True,
                status="protection_failed",
                message=message,
                stop_price=stop_loss,
                asset_type=asset_type,
                order_class="simple",
                protection_time_in_force=protection_tif,
                requires_eod_exit=requires_eod_exit,
                entry_poll_attempts=entry_completion["attempts"],
                terminal_entry_status=entry_status,
            )

        if fractional_entry:
            # A DAY stop is the only protection a fractional position gets, so confirm the
            # broker actually holds it before reporting the entry as protected.
            confirmation = self._poll_for_standalone_stop(
                order_id=self._order_identifier(submitted_stop),
                expected_stop_price=stop_loss,
                expected_qty=stop_qty,
                expected_time_in_force=protection_tif,
            )
            refreshed_stop = confirmation["order"] or submitted_stop
            if not confirmation["ok"]:
                print(confirmation["message"])
                return ExecutionResult(
                    success=False,
                    symbol=symbol,
                    side="buy",
                    requested_qty=qty,
                    filled_qty=filled_qty,
                    filled_avg_price=filled_avg_price,
                    entry_order_id=entry_order_id,
                    protective_order_id=self._order_identifier(refreshed_stop) or self._order_identifier(submitted_stop),
                    protection_active=False,
                    protection_failed=True,
                    counts_as_trade=True,
                    status="protection_failed",
                    message=confirmation["message"],
                    stop_price=stop_loss,
                    asset_type=asset_type,
                    order_class="simple",
                    protection_time_in_force=protection_tif,
                    requires_eod_exit=requires_eod_exit,
                    stop_confirmation_poll_attempts=confirmation["attempts"],
                    entry_poll_attempts=entry_completion["attempts"],
                    terminal_entry_status=entry_status,
                )
            stop_confirmation_attempts = confirmation["attempts"]
            message = (
                "Fractional entry filled and DAY protective stop confirmed with Alpaca; the stop expires at the close."
                if requires_eod_exit
                else "Fractional request filled to a whole-share quantity; GTC protective stop confirmed with Alpaca."
            )
        else:
            refreshed_stop = self._refresh_order(self._order_identifier(submitted_stop), nested=False) or submitted_stop
            stop_confirmation_attempts = 0
            message = "Entry filled and protective stop submitted to Alpaca."
        return ExecutionResult(
            success=True,
            symbol=symbol,
            side="buy",
            requested_qty=qty,
            filled_qty=filled_qty,
            filled_avg_price=filled_avg_price,
            entry_order_id=entry_order_id,
            protective_order_id=self._order_identifier(refreshed_stop) or self._order_identifier(submitted_stop),
            protection_active=True,
            protection_failed=False,
            counts_as_trade=True,
            status=entry_status,
            message=message,
            stop_price=stop_loss,
            asset_type=asset_type,
            order_class="simple",
            protection_time_in_force=protection_tif,
            requires_eod_exit=requires_eod_exit,
            stop_confirmation_poll_attempts=stop_confirmation_attempts,
            entry_poll_attempts=entry_completion["attempts"],
            terminal_entry_status=entry_status,
        )

    def _await_fractional_entry_terminal(self, order_id: Optional[str], symbol: str, submitted_order: Any) -> dict[str, Any]:
        """Never create DAY protection while an entry remainder could still fill.

        A fractional market BUY is briefly ``accepted`` or ``pending_new`` before it fills, so it
        gets a bounded fill window first. After that window any still-active remainder is
        cancelled, and only a confirmed terminal broker state lets the stop be sized.
        """
        latest = submitted_order
        attempts = 0
        cancel_attempted = False
        cancel_error = None
        fill_window = self.entry_fill_poll_attempts
        for attempts in range(1, fill_window + self.cancel_poll_attempts + 1):
            refreshed = self._refresh_order(order_id, nested=False)
            if refreshed is not None:
                latest = refreshed
            status = self._status_value(latest) or "unknown"
            if status == "filled" or status in _FRACTIONAL_ENTRY_NO_FILL_TERMINAL_STATUSES:
                return {
                    "ok": True, "order": latest, "attempts": attempts, "cancel_attempted": cancel_attempted,
                    "cancel_confirmed": status in {"canceled", "cancelled"}, "terminal_status": status, "message": None,
                }
            if status in _FRACTIONAL_ENTRY_CANCEL_PENDING_STATUSES:
                self._sleep_between_polls()
                continue
            if status not in _FRACTIONAL_ENTRY_ACTIVE_STATUSES:
                return {
                    "ok": False, "order": latest, "attempts": attempts, "cancel_attempted": cancel_attempted,
                    "cancel_confirmed": False, "terminal_status": status,
                    "message": f"CRITICAL: fractional entry for {symbol} has ambiguous broker status '{status}'; protection and further submission are blocked.",
                }
            if attempts >= fill_window and not cancel_attempted:
                # Cancel right after the last fill-window poll so every cancel_poll_attempts
                # iteration can observe the cancellation instead of consuming one to send it.
                cancel_attempted = True
                try:
                    self._client.cancel_order_by_id(order_id)
                except Exception as exc:
                    # A cancel error can race a fill; broker state, not the exception, decides safety.
                    cancel_error = exc
            self._sleep_between_polls()
        status = self._status_value(latest) or "unknown"
        suffix = f" cancel error={cancel_error}" if cancel_error is not None else ""
        return {
            "ok": False, "order": latest, "attempts": attempts, "cancel_attempted": cancel_attempted,
            "cancel_confirmed": False, "terminal_status": status,
            "message": f"CRITICAL: fractional entry for {symbol} did not reach a confirmed terminal state after cancellation; unfilled remainder may still execute.{suffix}",
        }

    def _poll_for_standalone_stop(self, order_id: Optional[str], expected_stop_price: float, expected_qty: float, expected_time_in_force: str = "gtc") -> dict[str, Any]:
        last_order = None
        for attempt in range(1, self.stop_confirmation_poll_attempts + 1):
            last_order = self._refresh_order(order_id, nested=False)
            if (
                self._is_valid_stop_order(last_order, expected_stop_price, expected_qty, expected_time_in_force)
                and self._status_value(last_order) in _ACTIVE_STOP_STATUSES
            ):
                return {"ok": True, "order": last_order, "attempts": attempt, "message": None}
            self._sleep_between_polls()
        return {
            "ok": False,
            "order": last_order,
            "attempts": self.stop_confirmation_poll_attempts,
            "message": "CRITICAL: standalone protective stop could not be confirmed after bounded polling.",
        }

    def close_position_for_eod(self, symbol: str, qty: float, asset_type: str, current_position_qty: float) -> ExecutionResult:
        """Market-sell a fractional equity holding before its DAY stop expires at the close.

        The protective stop is cancelled and verified first, the SELL is given a bounded fill
        window and confirmed terminal before any reconciliation, and a residual quantity is
        re-protected but still reported as a failure because its DAY stop expires at the close.
        """
        if not self.paper:
            return ExecutionResult(False, symbol, "sell", qty, status="rejected_live_disabled", message="Paper trading is required for this bot.", asset_type=asset_type, eod_exit=True)
        if not self._client:
            return ExecutionResult(False, symbol, "sell", qty, status="skipped", message="No Alpaca credentials available; EOD cleanup cannot exit the position.", asset_type=asset_type, eod_exit=True)
        if asset_type not in _EQUITY_ASSET_TYPES:
            return ExecutionResult(False, symbol, "sell", qty, status="rejected_not_equity", message="EOD cleanup only exits stock/ETF positions.", asset_type=asset_type, eod_exit=True)
        if qty <= 0 or current_position_qty <= 0 or qty > current_position_qty + 1e-9:
            return ExecutionResult(False, symbol, "sell", qty, status="rejected_invalid_qty", message="EOD cleanup quantity must be positive and within the verified long position.", asset_type=asset_type, remaining_position_qty=current_position_qty, eod_exit=True)

        result = self._place_exit_sell(symbol, qty, asset_type, current_position_qty=current_position_qty, confirm_terminal_fill=True)
        result.eod_exit = True
        if result.filled_qty > 0:
            # A SELL cancelled after a partial fill still traded; the log and daily counts must see it.
            result.counts_as_trade = True
        remaining = result.actual_remaining_position_qty
        if remaining is not None and remaining > 1e-9 and (result.success or result.filled_qty > 0) and not result.protection_failed:
            # A partial exit left shares whose only protection is a DAY stop that expires at the close.
            result.success = False
            result.status = "eod_exit_incomplete"
            protection_note = "re-protected by a DAY stop that expires at the close" if result.protection_active else "UNPROTECTED"
            result.message = f"EOD cleanup for {symbol} filled {result.filled_qty:g} of {qty:g}; {remaining:g} remains ({protection_note})."
            print(result.message)
        return result

    def _await_exit_terminal(self, order_id: Optional[str], symbol: str, submitted_order: Any) -> dict[str, Any]:
        """Give an EOD market SELL a short fill window, then cancel and confirm its terminal state."""
        latest = submitted_order
        active_statuses = _FRACTIONAL_ENTRY_ACTIVE_STATUSES | _FRACTIONAL_ENTRY_CANCEL_PENDING_STATUSES
        for attempt in range(1, self.exit_fill_poll_attempts + 1):
            latest = self._refresh_order(order_id, nested=False) or latest
            status = self._status_value(latest) or "unknown"
            if status in _EXIT_TERMINAL_STATUSES:
                return {"ok": True, "order": latest, "attempts": attempt, "message": None}
            if status not in active_statuses:
                return {"ok": False, "order": latest, "attempts": attempt, "message": f"CRITICAL: EOD SELL for {symbol} has ambiguous status '{status}'."}
            self._sleep_between_polls()
        try:
            self._client.cancel_order_by_id(order_id)
        except Exception:
            pass  # A cancellation error can race a fill; only subsequent broker state is authoritative.
        for cancel_attempt in range(1, self.cancel_poll_attempts + 1):
            latest = self._refresh_order(order_id, nested=False) or latest
            status = self._status_value(latest) or "unknown"
            attempts = self.exit_fill_poll_attempts + cancel_attempt
            if status in _EXIT_TERMINAL_STATUSES:
                return {"ok": True, "order": latest, "attempts": attempts, "message": None}
            if status not in active_statuses:
                return {"ok": False, "order": latest, "attempts": attempts, "message": f"CRITICAL: EOD SELL for {symbol} has ambiguous status '{status}' after cancellation."}
            self._sleep_between_polls()
        return {
            "ok": False,
            "order": latest,
            "attempts": self.exit_fill_poll_attempts + self.cancel_poll_attempts,
            "message": f"CRITICAL: EOD SELL for {symbol} did not reach a terminal state after cancellation; it may still execute while no protective stop exists.",
        }

    def _place_exit_sell(
        self,
        symbol: str,
        qty: float,
        asset_type: str,
        current_position_qty: float = 0.0,
        confirm_terminal_fill: bool = False,
    ) -> ExecutionResult:
        client = self._client
        if client is None:
            return ExecutionResult(False, symbol, "sell", qty, status="skipped", message="No Alpaca client available.", asset_type=asset_type)
        assert client is not None

        protective_orders, discovery_warning = self.find_protective_orders(symbol)
        protective_snapshots = self._capture_protective_orders_snapshot(protective_orders)
        if discovery_warning:
            message = f"SELL blocked for {symbol}: {discovery_warning}"
            print(message)
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="sell",
                requested_qty=qty,
                status="protection_reconciliation_failed",
                message=message,
                asset_type=asset_type,
                remaining_position_qty=current_position_qty,
                protection_reconciled=False,
            )

        cancellation_result = self._cancel_protective_orders(symbol, protective_orders)
        if not cancellation_result["ok"]:
            message = cancellation_result["message"]
            print(message)
            status = "position_closed_by_protective_stop" if cancellation_result.get("position_closed_by_stop") else cancellation_result.get("status", "protection_reconciliation_failed")
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="sell",
                requested_qty=qty,
                status=status,
                message=message,
                asset_type=asset_type,
                cancelled_protective_order_ids=cancellation_result["cancelled_ids"],
                remaining_position_qty=current_position_qty,
                actual_remaining_position_qty=cancellation_result.get("actual_remaining_position_qty"),
                protection_reconciled=bool(cancellation_result.get("position_closed_by_stop")),
                cancel_poll_attempts=cancellation_result.get("poll_attempts", 0),
            )

        tif = TimeInForce.GTC if asset_type == "crypto" or "/" in symbol else TimeInForce.DAY
        # A stable client order ID lets a SELL whose submission raised (e.g. a response timeout)
        # be found again, so protection is never restored on top of an exit the broker accepted.
        client_order_id = f"paper-{'eod' if confirm_terminal_fill else 'sell'}-{self._normalize_symbol(symbol).lower()}-{uuid.uuid4().hex[:12]}"
        order = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=tif,
            client_order_id=client_order_id,
        )
        submission_error: Optional[Exception] = None
        submitted_order = None
        try:
            submitted_order = client.submit_order(order)
        except Exception as exc:
            submission_error = exc
            recovered_order, lookup_reliable = self._lookup_order_by_client_id(client_order_id)
            if recovered_order is not None:
                # The broker accepted the SELL despite the error; continue with it as submitted.
                submitted_order = recovered_order
            elif not lookup_reliable:
                message = (
                    f"CRITICAL: SELL submission for {symbol} raised ({exc}) and the broker could not confirm whether "
                    f"order {client_order_id} exists; protection was NOT restored because the SELL may still execute."
                )
                print(message)
                return ExecutionResult(
                    success=False,
                    symbol=symbol,
                    side="sell",
                    requested_qty=qty,
                    status="critical_unprotected_position",
                    message=message,
                    asset_type=asset_type,
                    cancelled_protective_order_ids=cancellation_result["cancelled_ids"],
                    protection_failed=bool(protective_orders),
                    protection_reconciled=False,
                    remaining_position_qty=current_position_qty,
                    actual_remaining_position_qty=self.get_position_qty(symbol),
                    cancel_poll_attempts=cancellation_result.get("poll_attempts", 0),
                )
        if submission_error is not None and submitted_order is None:
            exc = submission_error
            actual_remaining_qty = self.get_position_qty(symbol)
            restore_result = self._restore_original_protection(
                symbol=symbol,
                protective_snapshots=protective_snapshots,
                actual_remaining_qty=actual_remaining_qty,
            )
            if restore_result["ok"]:
                message = "SELL failed, but original protection was successfully restored."
                print(message)
                return ExecutionResult(
                    success=False,
                    symbol=symbol,
                    side="sell",
                    requested_qty=qty,
                    status="sell_failed_protection_restored",
                    message=message,
                    asset_type=asset_type,
                    cancelled_protective_order_ids=cancellation_result["cancelled_ids"],
                    protection_active=True,
                    protection_reconciled=True,
                    protection_restore_attempted=True,
                    protection_restored=True,
                    restored_protective_order_id=restore_result["order_id"],
                    protective_order_id=restore_result["order_id"],
                    protection_retry_count=restore_result["attempts"],
                    cancel_poll_attempts=cancellation_result.get("poll_attempts", 0),
                    remaining_position_qty=current_position_qty,
                    actual_remaining_position_qty=actual_remaining_qty,
                    stop_price=restore_result.get("stop_price"),
                )

            message = (
                f"CRITICAL: SELL submission failed for {symbol} after protective stop reconciliation; "
                f"remaining quantity={actual_remaining_qty if actual_remaining_qty is not None else 'unknown'}; "
                f"intended stop price={restore_result.get('stop_price', 'unknown')}; restore error={restore_result['message']}; sell error={exc}"
            )
            print(message)
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="sell",
                requested_qty=qty,
                status="critical_unprotected_position",
                message=message,
                asset_type=asset_type,
                cancelled_protective_order_ids=cancellation_result["cancelled_ids"],
                protection_failed=True,
                protection_reconciled=False,
                protection_restore_attempted=True,
                protection_restored=False,
                protection_retry_count=restore_result["attempts"],
                cancel_poll_attempts=cancellation_result.get("poll_attempts", 0),
                remaining_position_qty=current_position_qty,
                actual_remaining_position_qty=actual_remaining_qty,
                stop_price=restore_result.get("stop_price"),
            )

        exit_poll_attempts = 0
        if confirm_terminal_fill:
            # Protection is already cancelled, so the SELL must be proven terminal before any
            # stop is restored; otherwise a late fill plus a restored stop could create a short.
            completion = self._await_exit_terminal(self._order_identifier(submitted_order), symbol, submitted_order)
            exit_poll_attempts = completion["attempts"]
            refreshed_order = completion["order"] or submitted_order
            if not completion["ok"]:
                print(completion["message"])
                return ExecutionResult(
                    success=False,
                    symbol=symbol,
                    side="sell",
                    requested_qty=qty,
                    filled_qty=self._safe_float(getattr(refreshed_order, "filled_qty", 0.0)),
                    entry_order_id=self._order_identifier(refreshed_order) or self._order_identifier(submitted_order),
                    status="critical_unprotected_position",
                    message=completion["message"],
                    asset_type=asset_type,
                    cancelled_protective_order_ids=cancellation_result["cancelled_ids"],
                    protection_failed=bool(protective_orders),
                    protection_reconciled=False,
                    remaining_position_qty=current_position_qty,
                    actual_remaining_position_qty=self.get_position_qty(symbol),
                    cancel_poll_attempts=cancellation_result.get("poll_attempts", 0),
                    exit_poll_attempts=exit_poll_attempts,
                )
        else:
            refreshed_order = self._refresh_order(self._order_identifier(submitted_order), nested=False) or submitted_order
        status = self._status_value(refreshed_order) or self._status_value(submitted_order) or "accepted"
        filled_qty = max(
            self._safe_float(getattr(submitted_order, "filled_qty", 0.0)),
            self._safe_float(getattr(refreshed_order, "filled_qty", 0.0)),
        )
        actual_remaining_qty = self.get_position_qty(symbol)
        remaining_position_qty = max(0.0, current_position_qty - filled_qty)
        base_result = ExecutionResult(
            success=self._counts_as_trade(status),
            symbol=symbol,
            side="sell",
            requested_qty=qty,
            filled_qty=filled_qty,
            filled_avg_price=self._safe_optional_float(
                getattr(refreshed_order, "filled_avg_price", None),
                fallback=getattr(submitted_order, "filled_avg_price", None),
            ),
            entry_order_id=self._order_identifier(refreshed_order) or self._order_identifier(submitted_order),
            protective_order_id=None,
            protection_active=False,
            protection_failed=False,
            counts_as_trade=self._counts_as_trade(status),
            status=status,
            message="SELL-to-close submitted to Alpaca.",
            asset_type=asset_type,
            order_class=self._order_class_value(refreshed_order) or self._order_class_value(submitted_order),
            cancelled_protective_order_ids=cancellation_result["cancelled_ids"],
            remaining_position_qty=remaining_position_qty,
            actual_remaining_position_qty=actual_remaining_qty,
            protection_reconciled=not protective_orders,
            cancel_poll_attempts=cancellation_result.get("poll_attempts", 0),
            exit_poll_attempts=exit_poll_attempts,
        )

        if actual_remaining_qty is None:
            base_result.success = False
            base_result.protection_failed = bool(protective_orders)
            base_result.protection_reconciled = False
            base_result.status = "critical_unprotected_position"
            base_result.message = (
                f"CRITICAL: broker position quantity for {symbol} could not be verified after SELL execution; stop recovery cannot safely continue."
            )
            print(base_result.message)
            return base_result

        if filled_qty <= 0.0:
            if actual_remaining_qty <= 0.0:
                base_result.success = True
                base_result.protection_reconciled = True
                base_result.message = f"SELL execution left no remaining long position in {symbol}."
                return base_result

            if protective_snapshots:
                restore_result = self._restore_original_protection(
                    symbol=symbol,
                    protective_snapshots=protective_snapshots,
                    actual_remaining_qty=actual_remaining_qty,
                )
                base_result.protection_restore_attempted = True
                base_result.protection_retry_count = restore_result["attempts"]
                base_result.stop_price = restore_result.get("stop_price")
                if restore_result["ok"]:
                    base_result.success = False
                    base_result.protection_active = True
                    base_result.protection_reconciled = True
                    base_result.protection_restored = True
                    base_result.restored_protective_order_id = restore_result["order_id"]
                    base_result.protective_order_id = restore_result["order_id"]
                    base_result.status = "sell_failed_protection_restored"
                    base_result.message = (
                        f"SELL for {symbol} was not confirmed by fill quantity, but protection was restored for the verified remaining position."
                    )
                    return base_result

                base_result.success = False
                base_result.protection_failed = True
                base_result.protection_reconciled = False
                base_result.status = "critical_unprotected_position"
                base_result.message = restore_result["message"]
                print(base_result.message)
                return base_result

            base_result.success = False
            base_result.status = "sell_execution_uncertain"
            base_result.message = (
                f"SELL for {symbol} was accepted without a confirmed fill quantity and no protective order required reconciliation."
            )
            return base_result

        if actual_remaining_qty <= 0.0:
            stale_orders, stale_warning = self.find_protective_orders(symbol)
            if stale_warning or stale_orders:
                message = stale_warning or f"CRITICAL: stale protective order remained open after closing {symbol}."
                print(message)
                base_result.success = False
                base_result.protection_failed = True
                base_result.protection_reconciled = False
                base_result.status = "protection_failed"
                base_result.message = message
                return base_result

            base_result.protection_reconciled = True
            base_result.message = "SELL-to-close submitted after protective stop reconciliation."
            return base_result

        if not protective_orders:
            base_result.protection_reconciled = True
            base_result.message = "Partial SELL executed; no active protective stop existed to reconcile."
            return base_result

        stop_prices = {self._safe_float(getattr(order, "stop_price", None), 0.0) for order in protective_orders if getattr(order, "stop_price", None) is not None}
        stop_prices.discard(0.0)
        if len(stop_prices) != 1:
            message = (
                f"CRITICAL: partial SELL for {symbol} completed but a replacement stop could not be determined safely from the prior protection set."
            )
            print(message)
            base_result.success = False
            base_result.protection_failed = True
            base_result.protection_reconciled = False
            base_result.status = "protection_failed"
            base_result.message = message
            return base_result

        replacement_stop_price = next(iter(stop_prices))
        replacement_result = self._replace_protection_after_partial_sell(
            symbol=symbol,
            actual_remaining_qty=actual_remaining_qty,
            stop_price=replacement_stop_price,
        )
        base_result.replacement_protective_order_id = replacement_result["order_id"]
        base_result.protective_order_id = replacement_result["order_id"]
        base_result.stop_price = replacement_stop_price
        base_result.protection_active = replacement_result["ok"]
        base_result.protection_reconciled = replacement_result["ok"]
        base_result.protection_retry_count = replacement_result["attempts"]

        if not replacement_result["ok"]:
            message = (
                replacement_result["message"]
                or f"CRITICAL: replacement protective stop placement failed for {symbol}; remaining quantity={actual_remaining_qty:g}."
            )
            print(message)
            base_result.success = False
            base_result.protection_failed = True
            base_result.status = "critical_unprotected_position"
            base_result.message = message
            return base_result

        stale_qty = self._open_protective_qty(symbol)
        if stale_qty > actual_remaining_qty + 1e-9:
            message = (
                f"CRITICAL: replacement protective stop quantity for {symbol} ({stale_qty:g}) exceeds the verified remaining long position ({actual_remaining_qty:g})."
            )
            print(message)
            base_result.success = False
            base_result.protection_failed = True
            base_result.protection_reconciled = False
            base_result.status = "critical_unprotected_position"
            base_result.message = message
            return base_result

        base_result.message = "Partial SELL executed and protective stop was replaced for the remaining long quantity."
        return base_result

    def list_open_orders(self, symbol: Optional[str] = None):
        if not self._client or not GetOrdersRequest or not QueryOrderStatus:
            return []
        client = self._client
        assert client is not None
        try:
            order_filter = GetOrdersRequest(
                status=QueryOrderStatus.OPEN,
                nested=True,
                symbols=[symbol] if symbol else None,
            )
            return list(client.get_orders(order_filter))
        except Exception:
            return []

    def find_protective_orders(self, symbol: str) -> tuple[list, Optional[str]]:
        protective_orders: dict[str, Any] = {}
        ambiguous_sell_orders: list[str] = []
        for order in self.list_open_orders(symbol):
            for candidate in self._iter_order_candidates(order):
                if self._normalize_symbol(getattr(candidate, "symbol", "")) != self._normalize_symbol(symbol):
                    continue
                order_id = self._order_identifier(candidate)
                if not order_id:
                    continue
                side = self._side_value(candidate)
                if side != "sell":
                    continue
                if self._is_protective_stop(candidate):
                    protective_orders[order_id] = candidate
                else:
                    ambiguous_sell_orders.append(order_id)

        if ambiguous_sell_orders:
            return [], (
                f"unable to reconcile existing SELL orders for {symbol} because non-protective open sell order(s) were present: "
                f"{', '.join(sorted(ambiguous_sell_orders))}"
            )
        return list(protective_orders.values()), None

    def _cancel_protective_orders(self, symbol: str, protective_orders: list) -> dict[str, Any]:
        if not protective_orders:
            return {"ok": True, "cancelled_ids": [], "message": None, "poll_attempts": 0}

        cancelled_ids: list[str] = []
        total_attempts = 0
        for order in protective_orders:
            order_id = self._order_identifier(order)
            if not order_id:
                return {
                    "ok": False,
                    "cancelled_ids": cancelled_ids,
                    "message": f"CRITICAL: protective stop for {symbol} could not be identified for cancellation.",
                    "status": "protective_stop_cancel_failed",
                    "poll_attempts": total_attempts,
                }
            cancel_result = self._cancel_and_verify(order_id, symbol)
            total_attempts += cancel_result["attempts"]
            if not cancel_result["ok"]:
                return {
                    "ok": False,
                    "cancelled_ids": cancelled_ids,
                    "message": cancel_result["message"],
                    "status": cancel_result["status"],
                    "poll_attempts": total_attempts,
                    "position_closed_by_stop": cancel_result.get("position_closed_by_stop", False),
                    "actual_remaining_position_qty": cancel_result.get("actual_remaining_position_qty"),
                }
            cancelled_ids.append(order_id)

        return {"ok": True, "cancelled_ids": cancelled_ids, "message": None, "poll_attempts": total_attempts}

    def _cancel_and_verify(self, order_id: str, symbol: str) -> dict[str, Any]:
        if not self._client:
            return {
                "ok": False,
                "attempts": 0,
                "status": "protective_stop_cancel_failed",
                "message": f"CRITICAL: protective stop cancellation failed for {symbol} on order {order_id} because no Alpaca client was available.",
            }
        client = self._client
        assert client is not None
        try:
            client.cancel_order_by_id(order_id)
        except Exception as exc:
            return {
                "ok": False,
                "attempts": 0,
                "status": "protective_stop_cancel_failed",
                "message": f"CRITICAL: protective stop cancellation failed for {symbol} on order {order_id}: {exc}",
            }

        open_like_statuses = {"pending_cancel", "pending_replace", "new", "accepted", "partially_filled", "pending_new"}
        for attempt in range(1, self.cancel_poll_attempts + 1):
            refreshed = self._refresh_order(order_id, nested=False)
            status = self._status_value(refreshed)

            if status in {"canceled", "cancelled"}:
                return {"ok": True, "attempts": attempt, "status": status, "message": None}

            if status == "filled":
                actual_remaining_qty = self.get_position_qty(symbol)
                if actual_remaining_qty == 0.0:
                    return {
                        "ok": False,
                        "attempts": attempt,
                        "status": "position_closed_by_protective_stop",
                        "message": f"Protective stop for {symbol} filled while cancellation was in progress; no additional SELL was submitted.",
                        "position_closed_by_stop": True,
                        "actual_remaining_position_qty": 0.0,
                    }
                return {
                    "ok": False,
                    "attempts": attempt,
                    "status": "protective_stop_cancel_failed",
                    "message": f"CRITICAL: protective stop for {symbol} filled while cancellation was in progress; remaining position state is {actual_remaining_qty if actual_remaining_qty is not None else 'unknown'}.",
                    "position_closed_by_stop": False,
                    "actual_remaining_position_qty": actual_remaining_qty,
                }

            if status is None and not self._is_order_open(order_id, symbol):
                return {"ok": True, "attempts": attempt, "status": "canceled", "message": None}

            if status in open_like_statuses or (status is None and self._is_order_open(order_id, symbol)):
                self._sleep_between_polls()
                continue

            return {
                "ok": False,
                "attempts": attempt,
                "status": "protective_stop_cancel_failed",
                "message": f"CRITICAL: protective stop cancellation for {symbol} ended in unexpected status '{status}' for order {order_id}.",
            }

        if not self._is_order_open(order_id, symbol):
            return {"ok": True, "attempts": self.cancel_poll_attempts, "status": "canceled", "message": None}

        return {
            "ok": False,
            "attempts": self.cancel_poll_attempts,
            "status": "protective_stop_cancel_timeout",
            "message": f"CRITICAL: protective stop cancellation timed out for {symbol} on order {order_id}.",
        }

    def _submit_replacement_stop(self, symbol: str, qty: float, stop_price: float) -> dict[str, Any]:
        client = self._client
        if client is None:
            return {"ok": False, "order_id": None, "message": f"CRITICAL: no Alpaca client available to replace protection for {symbol}."}
        assert client is not None
        # Alpaca rejects GTC stops on fractional equity quantities; a fractional remainder keeps a DAY stop.
        fractional_qty = abs(qty - math.floor(max(0.0, qty))) > 1e-9
        expected_time_in_force = "day" if fractional_qty else "gtc"
        try:
            stop_order = StopOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY if fractional_qty else TimeInForce.GTC,
                stop_price=stop_price,
            )
            submitted_stop = client.submit_order(stop_order)
        except Exception as exc:
            return {
                "ok": False,
                "order_id": None,
                "message": f"CRITICAL: replacement protective stop placement failed for {symbol}; remaining quantity={qty:g}; error={exc}",
            }

        refreshed_stop = self._refresh_order(self._order_identifier(submitted_stop), nested=False) or submitted_stop
        order_id = self._order_identifier(refreshed_stop) or self._order_identifier(submitted_stop)
        if not order_id:
            return {
                "ok": False,
                "order_id": None,
                "message": f"CRITICAL: replacement protective stop for {symbol} could not be identified after submission.",
            }
        validated_order = self._refresh_order(order_id, nested=False) or refreshed_stop
        if not self._is_valid_stop_order(validated_order, stop_price, qty, expected_time_in_force):
            return {
                "ok": False,
                "order_id": order_id,
                "message": f"CRITICAL: replacement protective stop for {symbol} could not be validated after submission.",
            }
        return {"ok": True, "order_id": order_id, "message": None}

    def _open_protective_qty(self, symbol: str) -> float:
        protective_orders, warning = self.find_protective_orders(symbol)
        if warning:
            return float("inf")
        return sum(self._safe_float(getattr(order, "qty", 0.0)) for order in protective_orders)

    def _replace_protection_after_partial_sell(self, symbol: str, actual_remaining_qty: float, stop_price: float) -> dict[str, Any]:
        attempts = 0
        last_message = None
        order_id = None
        for attempt in range(1, self.protection_retries + 1):
            attempts = attempt
            refreshed_qty = self.get_position_qty(symbol)
            if refreshed_qty is None:
                return {
                    "ok": False,
                    "order_id": None,
                    "message": f"CRITICAL: broker position quantity for {symbol} could not be verified while replacing protection.",
                    "attempts": attempts,
                }
            if refreshed_qty <= 0.0:
                return {
                    "ok": False,
                    "order_id": None,
                    "message": f"CRITICAL: no remaining verified long position exists for {symbol}; replacement protection was not created.",
                    "attempts": attempts,
                }
            result = self._submit_replacement_stop(symbol, refreshed_qty, stop_price)
            if result["ok"]:
                result["attempts"] = attempts
                return result
            order_id = result.get("order_id")
            last_message = result["message"]
            self._sleep_between_polls()
        return {"ok": False, "order_id": order_id, "message": last_message, "attempts": attempts}

    def _restore_original_protection(self, symbol: str, protective_snapshots: list[dict], actual_remaining_qty: Optional[float]) -> dict[str, Any]:
        if actual_remaining_qty is None:
            return {
                "ok": False,
                "order_id": None,
                "message": f"CRITICAL: broker position quantity for {symbol} could not be verified while restoring protection.",
                "attempts": 0,
                "stop_price": None,
            }
        if actual_remaining_qty <= 0.0:
            return {"ok": True, "order_id": None, "message": None, "attempts": 0, "stop_price": None}
        blueprint = self._build_stop_blueprint(symbol, protective_snapshots)
        if not blueprint["ok"]:
            blueprint["attempts"] = 0
            return blueprint
        replacement = self._replace_protection_after_partial_sell(symbol, actual_remaining_qty, blueprint["stop_price"])
        replacement["stop_price"] = blueprint["stop_price"]
        return replacement

    @staticmethod
    def _capture_protective_orders_snapshot(protective_orders: list) -> list[dict]:
        snapshots: list[dict] = []
        for order in protective_orders:
            snapshots.append(
                {
                    "symbol": getattr(order, "symbol", None),
                    "order_id": getattr(order, "id", None),
                    "qty": getattr(order, "qty", None),
                    "stop_price": getattr(order, "stop_price", None),
                    "side": getattr(order, "side", None),
                    "order_type": getattr(order, "type", getattr(order, "order_type", None)),
                    "time_in_force": getattr(order, "time_in_force", None),
                }
            )
        return snapshots

    def _build_stop_blueprint(self, symbol: str, protective_snapshots: list[dict]) -> dict[str, Any]:
        if not protective_snapshots:
            return {
                "ok": False,
                "order_id": None,
                "message": f"CRITICAL: no original protective stop details were available to restore protection for {symbol}.",
                "stop_price": None,
            }
        stop_prices = {self._safe_float(snapshot.get("stop_price"), 0.0) for snapshot in protective_snapshots if snapshot.get("stop_price") is not None}
        stop_prices.discard(0.0)
        if len(stop_prices) != 1:
            return {
                "ok": False,
                "order_id": None,
                "message": f"CRITICAL: original protective stop details for {symbol} were ambiguous and could not be restored safely.",
                "stop_price": None,
            }
        return {"ok": True, "order_id": None, "message": None, "stop_price": next(iter(stop_prices))}

    def _lookup_order_by_client_id(self, client_order_id: str) -> tuple[Any, bool]:
        """Return (order, reliable). A confirmed "not found" is (None, True); any other failure is (None, False)."""
        client = self._client
        if client is None or not hasattr(client, "get_order_by_client_id"):
            return None, False
        try:
            order = client.get_order_by_client_id(client_order_id)
        except Exception as exc:
            status_code = getattr(exc, "status_code", None)
            if status_code == 404 or "not found" in str(exc).lower():
                return None, True
            return None, False
        if order is None:
            return None, True
        return order, True

    def _is_order_open(self, order_id: str, symbol: str) -> bool:
        for order in self.list_open_orders(symbol):
            for candidate in self._iter_order_candidates(order):
                if self._order_identifier(candidate) == order_id:
                    return True
        return False

    def _sleep_between_polls(self) -> None:
        if self.poll_delay_seconds > 0:
            self.sleep_fn(self.poll_delay_seconds)

    def _refresh_order(self, order_id: Optional[str], nested: bool):
        if not self._client or not order_id or not GetOrderByIdRequest:
            return None
        client = self._client
        assert client is not None
        try:
            return client.get_order_by_id(order_id, GetOrderByIdRequest(nested=nested))
        except Exception:
            return None

    def _poll_for_attached_stop(self, order_id: Optional[str], symbol: str, expected_stop_price: float, expected_max_qty: float) -> dict[str, Any]:
        last_order = None
        last_message = None
        for attempt in range(1, self.stop_confirmation_poll_attempts + 1):
            last_order = self._refresh_order(order_id, nested=True)
            stop_leg = self._extract_stop_leg(last_order)
            if stop_leg is not None:
                validation_error = self._validate_attached_stop_leg(stop_leg, expected_stop_price, expected_max_qty)
                if validation_error is None:
                    return {"ok": True, "order": last_order, "stop_leg": stop_leg, "attempts": attempt, "message": None}
                last_message = validation_error
            self._sleep_between_polls()

        return {
            "ok": False,
            "order": last_order,
            "stop_leg": self._extract_stop_leg(last_order),
            "attempts": self.stop_confirmation_poll_attempts,
            "message": last_message or f"CRITICAL: protective stop child for {symbol} could not be confirmed after bounded polling.",
        }

    def _validate_attached_stop_leg(self, stop_leg, expected_stop_price: float, expected_max_qty: float) -> Optional[str]:
        order_id = self._order_identifier(stop_leg)
        if order_id is None:
            return "CRITICAL: protective stop child exists but has no broker order ID."
        if self._side_value(stop_leg) != "sell":
            return "CRITICAL: protective stop child was not a SELL order."
        stop_price = self._safe_optional_float(getattr(stop_leg, "stop_price", None))
        if stop_price is None or abs(stop_price - expected_stop_price) > 0.01:
            return "CRITICAL: protective stop child stop price did not match the expected value."
        stop_qty = self._safe_float(getattr(stop_leg, "qty", 0.0))
        if stop_qty <= 0.0 or stop_qty > expected_max_qty + 1e-9:
            return "CRITICAL: protective stop child quantity was invalid for the requested BUY size."
        return None

    def _is_valid_stop_order(self, order, expected_stop_price: float, expected_qty: float, expected_time_in_force: str = "gtc") -> bool:
        if order is None:
            return False
        if self._order_identifier(order) is None:
            return False
        if self._side_value(order) != "sell":
            return False
        if self._time_in_force_value(order) not in {None, expected_time_in_force}:
            return False
        stop_price = self._safe_optional_float(getattr(order, "stop_price", None))
        qty = self._safe_float(getattr(order, "qty", 0.0))
        return stop_price is not None and abs(stop_price - expected_stop_price) <= 0.01 and 0.0 < qty <= expected_qty + 1e-9

    @staticmethod
    def _safe_float(value, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @classmethod
    def _safe_optional_float(cls, value, fallback=None) -> Optional[float]:
        if value is None and fallback is None:
            return None
        if value is None:
            value = fallback
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _counts_as_trade(status: Optional[str]) -> bool:
        return (status or "").lower() in {
            "accepted",
            "new",
            "partially_filled",
            "filled",
            "pending_new",
            "pending_replace",
        }

    @staticmethod
    def _status_value(order) -> Optional[str]:
        status = getattr(order, "status", None)
        if status is None:
            return None
        return getattr(status, "value", str(status)).lower()

    @staticmethod
    def _enum_or_value(value) -> Optional[str]:
        if value is None:
            return None
        return getattr(value, "value", str(value)).lower()

    @staticmethod
    def _order_class_value(order) -> Optional[str]:
        order_class = getattr(order, "order_class", None)
        if order_class is None:
            return None
        return getattr(order_class, "value", str(order_class)).lower()

    @classmethod
    def _time_in_force_value(cls, order) -> Optional[str]:
        if order is None:
            return None
        return cls._enum_or_value(getattr(order, "time_in_force", None))

    @staticmethod
    def _order_identifier(order) -> Optional[str]:
        if order is None:
            return None
        for attr in ("id", "client_order_id"):
            value = getattr(order, attr, None)
            if value:
                return str(value)
        return None

    @classmethod
    def _extract_stop_leg(cls, order):
        legs = getattr(order, "legs", None) or []
        for leg in legs:
            if getattr(leg, "stop_price", None) is not None:
                return leg
            if cls._status_value(leg) == "stopped":
                return leg
        return None

    @staticmethod
    def _side_value(order) -> Optional[str]:
        if order is None:
            return None
        side = getattr(order, "side", None)
        if side is not None:
            return AlpacaClient._enum_or_value(side)
        return AlpacaClient._enum_or_value(order)

    @classmethod
    def _is_protective_stop(cls, order) -> bool:
        return cls._side_value(order) == "sell" and getattr(order, "stop_price", None) is not None

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        return symbol.replace("/", "").upper()

    @staticmethod
    def _iter_order_candidates(order):
        yield order
        for leg in getattr(order, "legs", None) or []:
            yield leg

