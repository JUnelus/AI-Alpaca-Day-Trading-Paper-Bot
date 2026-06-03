from datetime import date

from src.watchlist_manager import _week_key, select_top_symbols


def test_select_top_symbols_by_market_value():
    universe = [
        {"symbol": "AAA", "name": "A", "type": "stock"},
        {"symbol": "BBB", "name": "B", "type": "stock"},
        {"symbol": "CCC", "name": "C", "type": "stock"},
    ]
    values = {"AAA": 100.0, "BBB": 350.0, "CCC": 200.0}

    selected = select_top_symbols(universe, values, limit=2)

    assert [item["symbol"] for item in selected] == ["BBB", "CCC"]


def test_select_top_symbols_fills_when_values_missing():
    universe = [
        {"symbol": "AAA", "name": "A", "type": "stock"},
        {"symbol": "BBB", "name": "B", "type": "stock"},
    ]

    selected = select_top_symbols(universe, {}, limit=2)

    assert len(selected) == 2
    assert selected[0]["symbol"] == "AAA"


def test_week_key_format():
    assert _week_key(date(2026, 6, 3)) == "2026-W23"


