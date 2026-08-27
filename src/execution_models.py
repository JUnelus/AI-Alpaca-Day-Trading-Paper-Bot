from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class ExecutionResult:
    success: bool
    symbol: str
    side: str
    requested_qty: float
    filled_qty: float = 0.0
    filled_avg_price: float | None = None
    entry_order_id: str | None = None
    protective_order_id: str | None = None
    protection_active: bool = False
    protection_failed: bool = False
    counts_as_trade: bool = False
    status: str = "skipped"
    message: str | None = None
    stop_price: float | None = None
    asset_type: str = "stock"
    order_class: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

