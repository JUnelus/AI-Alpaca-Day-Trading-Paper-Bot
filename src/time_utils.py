from __future__ import annotations

from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo

TRADING_TIMEZONE = ZoneInfo("America/New_York")
DEFAULT_SCHEDULE_TOLERANCE_MINUTES = 3
SCHEDULE_TARGETS = {
    "trade": time(hour=9, minute=45),
    "report": time(hour=16, minute=15),
}


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


def scheduled_mode_matches(
    mode: str,
    now: datetime | None = None,
    tolerance_minutes: int = DEFAULT_SCHEDULE_TOLERANCE_MINUTES,
) -> bool:
    target = SCHEDULE_TARGETS.get(mode)
    if target is None:
        raise ValueError(f"Unsupported scheduled mode: {mode}")

    local_now = trading_datetime(now)
    target_dt = local_now.replace(
        hour=target.hour,
        minute=target.minute,
        second=0,
        microsecond=0,
    )
    delta_seconds = abs((local_now - target_dt).total_seconds())
    return delta_seconds <= max(0, tolerance_minutes) * 60


def scheduled_skip_reason(
    mode: str,
    now: datetime | None = None,
    tolerance_minutes: int = DEFAULT_SCHEDULE_TOLERANCE_MINUTES,
) -> str:
    local_now = trading_datetime(now)
    target = SCHEDULE_TARGETS[mode]
    return (
        f"Scheduled {mode} run skipped: current America/New_York time "
        f"{local_now.strftime('%Y-%m-%d %H:%M:%S %Z')} is outside the "
        f"{target.strftime('%H:%M')} ET execution window (±{tolerance_minutes} min)."
    )


