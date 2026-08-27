from datetime import datetime, timezone

from src.time_utils import scheduled_mode_matches, trading_datetime


def test_august_trade_schedule_matches_1345_utc_but_not_1445_utc():
    edt_trade = datetime(2026, 8, 27, 13, 45, tzinfo=timezone.utc)
    wrong_candidate = datetime(2026, 8, 27, 14, 45, tzinfo=timezone.utc)

    assert trading_datetime(edt_trade).strftime("%Z") == "EDT"
    assert scheduled_mode_matches("trade", edt_trade)
    assert not scheduled_mode_matches("trade", wrong_candidate)


def test_january_trade_schedule_matches_1445_utc_but_not_1345_utc():
    est_trade = datetime(2026, 1, 15, 14, 45, tzinfo=timezone.utc)
    wrong_candidate = datetime(2026, 1, 15, 13, 45, tzinfo=timezone.utc)

    assert trading_datetime(est_trade).strftime("%Z") == "EST"
    assert scheduled_mode_matches("trade", est_trade)
    assert not scheduled_mode_matches("trade", wrong_candidate)


def test_august_report_schedule_matches_2015_utc_but_not_2115_utc():
    edt_report = datetime(2026, 8, 27, 20, 15, tzinfo=timezone.utc)
    wrong_candidate = datetime(2026, 8, 27, 21, 15, tzinfo=timezone.utc)

    assert scheduled_mode_matches("report", edt_report)
    assert not scheduled_mode_matches("report", wrong_candidate)


def test_january_report_schedule_matches_2115_utc_but_not_2015_utc():
    est_report = datetime(2026, 1, 15, 21, 15, tzinfo=timezone.utc)
    wrong_candidate = datetime(2026, 1, 15, 20, 15, tzinfo=timezone.utc)

    assert scheduled_mode_matches("report", est_report)
    assert not scheduled_mode_matches("report", wrong_candidate)

