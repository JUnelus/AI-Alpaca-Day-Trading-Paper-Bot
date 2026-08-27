from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from .execution_models import ExecutionResult

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


class AlpacaClient:
    def __init__(self, trading_client: Optional[Any] = None, paper: Optional[bool] = None, prefer_attached_stops: bool = True) -> None:
        api_key = os.getenv("ALPACA_API_KEY")
        secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.paper = paper if paper is not None else os.getenv("ALPACA_PAPER", "true").lower() == "true"
        self.prefer_attached_stops = prefer_attached_stops
        self._client: Optional[Any] = trading_client

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

    def can_place_protected_buy(self, asset_type: str) -> bool:
        if asset_type not in {"stock", "etf"}:
            return False
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

        full_order = self._refresh_order(self._order_identifier(submitted_order), nested=True) or submitted_order
        entry_order_id = self._order_identifier(full_order) or self._order_identifier(submitted_order)
        stop_leg = self._extract_stop_leg(full_order)
        protective_order_id = self._order_identifier(stop_leg)
        filled_qty = max(self._safe_float(getattr(submitted_order, "filled_qty", 0.0)), self._safe_float(getattr(full_order, "filled_qty", 0.0)))
        filled_avg_price = self._safe_optional_float(
            getattr(full_order, "filled_avg_price", None),
            fallback=getattr(submitted_order, "filled_avg_price", None),
        )
        order_class = self._order_class_value(full_order) or self._order_class_value(submitted_order)
        status = self._status_value(full_order) or self._status_value(submitted_order) or "accepted"
        protection_active = stop_leg is not None or order_class in {"oto", "bracket"}

        if not protection_active:
            exposed_qty = filled_qty if filled_qty > 0 else qty
            message = (
                f"CRITICAL: protective stop submission could not be confirmed for {symbol}; "
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
                message=message,
                stop_price=stop_loss,
                asset_type=asset_type,
                order_class=order_class,
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
        )

    def _place_entry_then_stop_buy(self, symbol: str, qty: float, stop_loss: float, asset_type: str) -> ExecutionResult:
        client = self._client
        if client is None:
            return ExecutionResult(False, symbol, "buy", qty, status="skipped", message="No Alpaca client available.", asset_type=asset_type, stop_price=stop_loss)
        assert client is not None
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
            )

        entry_order_id = self._order_identifier(submitted_entry)
        refreshed_entry = self._refresh_order(entry_order_id, nested=False) or submitted_entry
        filled_qty = max(
            self._safe_float(getattr(submitted_entry, "filled_qty", 0.0)),
            self._safe_float(getattr(refreshed_entry, "filled_qty", 0.0)),
        )
        filled_avg_price = self._safe_optional_float(
            getattr(refreshed_entry, "filled_avg_price", None),
            fallback=getattr(submitted_entry, "filled_avg_price", None),
        )
        entry_status = self._status_value(refreshed_entry) or self._status_value(submitted_entry) or "accepted"

        if filled_qty <= 0.0:
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

        stop_qty = min(qty, filled_qty)
        stop_order = StopOrderRequest(
            symbol=symbol,
            qty=stop_qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC,
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
            )

        refreshed_stop = self._refresh_order(self._order_identifier(submitted_stop), nested=False) or submitted_stop
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
            message="Entry filled and protective stop submitted to Alpaca.",
            stop_price=stop_loss,
            asset_type=asset_type,
            order_class="simple",
        )

    def _place_exit_sell(self, symbol: str, qty: float, asset_type: str, current_position_qty: float = 0.0) -> ExecutionResult:
        client = self._client
        if client is None:
            return ExecutionResult(False, symbol, "sell", qty, status="skipped", message="No Alpaca client available.", asset_type=asset_type)
        assert client is not None

        protective_orders, discovery_warning = self.find_protective_orders(symbol)
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
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="sell",
                requested_qty=qty,
                status="protection_reconciliation_failed",
                message=message,
                asset_type=asset_type,
                cancelled_protective_order_ids=cancellation_result["cancelled_ids"],
                remaining_position_qty=current_position_qty,
                protection_reconciled=False,
            )

        tif = TimeInForce.GTC if asset_type == "crypto" or "/" in symbol else TimeInForce.DAY
        order = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=tif,
        )
        try:
            submitted_order = client.submit_order(order)
        except Exception as exc:
            message = (
                f"CRITICAL: SELL submission failed for {symbol} after protective stop reconciliation; "
                f"remaining position may be unprotected. error={exc}"
            )
            print(message)
            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="sell",
                requested_qty=qty,
                status="protection_reconciliation_failed",
                message=message,
                asset_type=asset_type,
                cancelled_protective_order_ids=cancellation_result["cancelled_ids"],
                remaining_position_qty=current_position_qty,
                protection_reconciled=False,
            )

        refreshed_order = self._refresh_order(self._order_identifier(submitted_order), nested=False) or submitted_order
        status = self._status_value(refreshed_order) or self._status_value(submitted_order) or "accepted"
        filled_qty = max(
            self._safe_float(getattr(submitted_order, "filled_qty", 0.0)),
            self._safe_float(getattr(refreshed_order, "filled_qty", 0.0)),
        )
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
            protection_reconciled=not protective_orders,
        )

        if filled_qty <= 0.0:
            base_result.success = False
            base_result.protection_failed = bool(protective_orders)
            base_result.protection_reconciled = not protective_orders
            base_result.status = "protection_reconciliation_pending"
            base_result.message = (
                f"CRITICAL: SELL for {symbol} was accepted without a confirmed fill quantity after protection was reconciled; remaining position is uncertain."
            )
            print(base_result.message)
            return base_result

        if remaining_position_qty <= 0.0:
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
        replacement_result = self._submit_replacement_stop(symbol, remaining_position_qty, replacement_stop_price)
        base_result.replacement_protective_order_id = replacement_result["order_id"]
        base_result.protective_order_id = replacement_result["order_id"]
        base_result.stop_price = replacement_stop_price
        base_result.protection_active = replacement_result["ok"]
        base_result.protection_reconciled = replacement_result["ok"]

        if not replacement_result["ok"]:
            message = replacement_result["message"]
            print(message)
            base_result.success = False
            base_result.protection_failed = True
            base_result.status = "protection_failed"
            base_result.message = message
            return base_result

        stale_qty = self._open_protective_qty(symbol)
        if stale_qty > remaining_position_qty + 1e-9:
            message = (
                f"CRITICAL: replacement protective stop quantity for {symbol} ({stale_qty:g}) exceeds the remaining long position ({remaining_position_qty:g})."
            )
            print(message)
            base_result.success = False
            base_result.protection_failed = True
            base_result.protection_reconciled = False
            base_result.status = "protection_failed"
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
            return {"ok": True, "cancelled_ids": [], "message": None}

        cancelled_ids: list[str] = []
        for order in protective_orders:
            order_id = self._order_identifier(order)
            if not order_id:
                return {
                    "ok": False,
                    "cancelled_ids": cancelled_ids,
                    "message": f"CRITICAL: protective stop for {symbol} could not be identified for cancellation.",
                }
            if not self._cancel_and_verify(order_id):
                return {
                    "ok": False,
                    "cancelled_ids": cancelled_ids,
                    "message": f"CRITICAL: protective stop cancellation failed for {symbol} on order {order_id}.",
                }
            cancelled_ids.append(order_id)

        return {"ok": True, "cancelled_ids": cancelled_ids, "message": None}

    def _cancel_and_verify(self, order_id: str) -> bool:
        if not self._client:
            return False
        client = self._client
        assert client is not None
        try:
            client.cancel_order_by_id(order_id)
        except Exception:
            return False

        refreshed = self._refresh_order(order_id, nested=False)
        return self._status_value(refreshed) in {"canceled", "cancelled"}

    def _submit_replacement_stop(self, symbol: str, qty: float, stop_price: float) -> dict[str, Any]:
        client = self._client
        if client is None:
            return {"ok": False, "order_id": None, "message": f"CRITICAL: no Alpaca client available to replace protection for {symbol}."}
        assert client is not None
        try:
            stop_order = StopOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.GTC,
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
        return {"ok": True, "order_id": order_id, "message": None}

    def _open_protective_qty(self, symbol: str) -> float:
        protective_orders, warning = self.find_protective_orders(symbol)
        if warning:
            return float("inf")
        return sum(self._safe_float(getattr(order, "qty", 0.0)) for order in protective_orders)

    def _refresh_order(self, order_id: Optional[str], nested: bool):
        if not self._client or not order_id or not GetOrderByIdRequest:
            return None
        client = self._client
        assert client is not None
        try:
            return client.get_order_by_id(order_id, GetOrderByIdRequest(nested=nested))
        except Exception:
            return None

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
    def _order_class_value(order) -> Optional[str]:
        order_class = getattr(order, "order_class", None)
        if order_class is None:
            return None
        return getattr(order_class, "value", str(order_class)).lower()

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
        side = getattr(order, "side", None)
        if side is None:
            return None
        return getattr(side, "value", str(side)).lower()

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

