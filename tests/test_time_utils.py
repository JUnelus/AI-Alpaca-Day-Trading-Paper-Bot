from datetime import datetime, timezone

from src.time_utils import trading_datetime, trading_day


def test_august_conversion_uses_edt():
    dt = datetime(2026, 8, 27, 13, 45, tzinfo=timezone.utc)
    local = trading_datetime(dt)

    assert local.strftime("%Z") == "EDT"
    assert local.hour == 9
    assert local.minute == 45


def test_january_conversion_uses_est():
    dt = datetime(2026, 1, 15, 14, 45, tzinfo=timezone.utc)
    local = trading_datetime(dt)

    assert local.strftime("%Z") == "EST"
    assert local.hour == 9
    assert local.minute == 45


def test_midnight_utc_can_still_be_previous_eastern_trading_day():
    dt = datetime(2026, 8, 28, 0, 30, tzinfo=timezone.utc)
    assert trading_day(dt) == "2026-08-27"


def test_new_eastern_trading_day_rolls_after_local_midnight():
    dt = datetime(2026, 8, 28, 5, 0, tzinfo=timezone.utc)
    assert trading_day(dt) == "2026-08-28"

