from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

TRADING_TIMEZONE = ZoneInfo("America/New_York")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def trading_datetime(now: datetime | None = None) -> datetime:
    return ensure_aware(now or utc_now()).astimezone(TRADING_TIMEZONE)


def trading_day(now: datetime | None = None) -> str:
    return trading_datetime(now).date().isoformat()


def parse_iso_datetime(value: str) -> datetime | None:
    if not value:
        return None

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

    return ensure_aware(parsed)


def iso_to_trading_day(value: str) -> str | None:
    parsed = parse_iso_datetime(value)
    if parsed is None:
        return None
    return parsed.astimezone(TRADING_TIMEZONE).date().isoformat()



