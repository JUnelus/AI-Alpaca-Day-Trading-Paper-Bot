"""Generate and inject the portfolio dashboard into README.md."""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .portfolio import PortfolioState

README_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "README.md")
)
DASHBOARD_START = "<!-- PORTFOLIO_DASHBOARD_START -->"
DASHBOARD_END = "<!-- PORTFOLIO_DASHBOARD_END -->"


# ── helpers ────────────────────────────────────────────────────────────────────

def _icon(value: float) -> str:
    return "🟢" if value > 0 else ("🔴" if value < 0 else "⚪")


def _fmt_usd(value: float, sign: bool = False) -> str:
    prefix = "+" if sign and value > 0 else ""
    return f"{prefix}${value:,.2f}"


def _fmt_optional_usd(value: Optional[float], sign: bool = False) -> str:
    if value is None:
        return "N/A"
    return _fmt_usd(value, sign=sign)


def _fmt_pct(value: float) -> str:
    prefix = "+" if value > 0 else ""
    return f"{prefix}{value:.2f}%"


def _fmt_optional_pct(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return _fmt_pct(value)


def _qty_str(qty: float) -> str:
    return f"{qty:.4f}" if qty < 10 else f"{qty:.2f}"


# ── core ───────────────────────────────────────────────────────────────────────

def generate_dashboard(
    state: PortfolioState,
    watchlist: List[dict],
    signal_map: Optional[Dict[str, dict]] = None,
    run_results: Optional[List[dict]] = None,
) -> str:
    """Return the markdown content that sits between the two marker comments."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pnl_icon = _icon(state.total_pnl)
    legacy_account_state = state.gross_exposure > state.max_total_exposure + 1e-9 if state.max_total_exposure else False
    broker_pnl_label = "Broker Position P&L (partial)" if not state.pnl_data_complete else "Broker Position P&L"

    lines: List[str] = [
        "",
        "## 📊 Live Portfolio Dashboard",
        "",
        f"> 🕐 **Last updated:** {now} &nbsp;|&nbsp; "
        f"**Trades today:** {state.trades_today} &nbsp;|&nbsp; "
        f"🧪 Paper trading only — not financial advice",
        "",
        "---",
        "",
        "### 💰 Account Summary",
        "",
        "| Metric | Value |",
        "|:-------|------:|",
        f"| 🧭 Configured Strategy Budget | `${state.starting_balance:,.2f}` |",
        f"| 🛡️ Strategy Max Gross Exposure | `${state.max_total_exposure:,.2f}` |",
        f"| 💵 Alpaca Paper Account Equity | `${state.account_equity:,.2f}` |",
        f"| 💸 Broker Cash Available | `${state.cash:,.2f}` |",
        f"| 🧾 Broker Buying Power | `${state.buying_power:,.2f}` |",
        f"| 📦 Actual Broker Gross Exposure | `${state.gross_exposure:,.2f}` |",
        f"| {pnl_icon} {broker_pnl_label} | `{_fmt_usd(state.total_pnl, sign=True)}` "
        f"&nbsp; `({_fmt_pct(state.total_pnl_pct)})` |",
        f"| 📆 Daily P&L (final equity - start of day) | `{_fmt_usd(state.daily_pnl, sign=True)}` |",
        "",
    ]

    if legacy_account_state:
        lines += [
            "### ⚠️ LEGACY PAPER ACCOUNT STATE",
            "",
            "The current Alpaca paper account contains positions created before the present "
            "`$10,000` risk controls were enforced.",
            "",
            "Current broker equity/P&L should not be interpreted as performance of the current hardened strategy.",
            "",
            "The bot will warn, block additional BUY exposure, and continue allowing valid risk-reducing SELLs.",
            "",
        ]

    if state.warnings:
        lines += [
            "### ⚠️ Safety Warnings",
            "",
        ]
        lines.extend(f"- {warning}" for warning in state.warnings)
        if not state.pnl_data_complete:
            lines.append(
                f"- Broker position P&L is partial because cost basis or unrealized P&L is unavailable for {state.unknown_position_pnl_count} position(s)."
            )
        lines.append("")

    # ── written summary ─────────────────────────────────────────────────────────
    lines += [
        "### 📝 Daily Trade Summary",
        "",
        f"- **Broker position P&L:** `{_fmt_usd(state.total_pnl, sign=True)}` ({_fmt_pct(state.total_pnl_pct)})",
        f"- **Daily P&L:** `{_fmt_usd(state.daily_pnl, sign=True)}`",
    ]

    if not state.pnl_data_complete:
        lines.append(
            f"- **P&L data quality:** Partial — cost basis or unrealized P&L is unavailable for {state.unknown_position_pnl_count} position(s)."
        )

    executed = []
    for result in run_results or []:
        decision = result.get("decision", {})
        action = str(decision.get("action", "hold")).lower()
        order_result = result.get("order_result") or {}
        if action in {"buy", "sell"} and order_result.get("counts_as_trade"):
            executed.append(result)

    if executed:
        lines += [
            "- **Executed today (with AI reasoning):**",
            "",
            "| Symbol | Action | Confidence | AI Reasoning |",
            "|:-------|:------:|-----------:|:-------------|",
        ]
        for result in executed:
            decision = result.get("decision", {})
            symbol = result.get("symbol", "?")
            action = str(decision.get("action", "?")).upper()
            confidence = float(decision.get("confidence", 0.0))
            reasoning = str(decision.get("reason", "No reasoning provided")).replace("\n", " ").strip()
            lines.append(
                f"| **{symbol}** | {action} | {confidence:.0%} | {reasoning} |"
            )
    else:
        lines.append("- **Executed today:** No buy/sell orders were approved in this run.")

    lines.append("")

    # ── open positions ─────────────────────────────────────────────────────────
    lines.append("### 📈 Open Positions")
    lines.append("")
    if state.positions:
        lines += [
            "| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |",
            "|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|",
        ]
        for pos in state.positions:
            icon = _icon(pos.unrealized_pnl or 0.0)
            position_label = f"{pos.asset_type.upper()} {'📉 SHORT' if pos.qty < 0 else ''}" .strip()
            lines.append(
                f"| **{pos.symbol}** | {position_label} "
                f"| {_qty_str(pos.qty)} "
                f"| {_fmt_optional_usd(pos.avg_entry_price)} "
                f"| {_fmt_optional_usd(pos.current_price)} "
                f"| {_fmt_optional_usd(pos.market_value)} "
                f"| {icon} {_fmt_optional_usd(pos.unrealized_pnl, sign=True)} "
                f"| {_fmt_optional_pct(pos.unrealized_pnl_pct)} |"
            )
    else:
        lines.append("*No open positions.*")
    lines.append("")

    # ── watchlist ──────────────────────────────────────────────────────────────
    lines += [
        "### 🎯 Watchlist — 10 Symbols",
        "",
        "| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |",
        "|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|",
    ]
    for i, sym_cfg in enumerate(watchlist, 1):
        sym = sym_cfg["symbol"]
        sig = (signal_map or {}).get(sym)
        if sig:
            action = sig.get("action", "hold")
            conf = float(sig.get("confidence", 0))
            price = float(sig.get("last_price", 0))
            day_chg = float(sig.get("day_change_percent", 0))
            chg_icon = _icon(day_chg)
            signal_str = f"**{action.upper()}**" if action != "hold" else "HOLD"
            conf_str = f"{conf:.0%}" if action != "hold" else "—"
            price_str = f"${price:,.2f}"
            day_chg_str = f"{chg_icon} {_fmt_pct(day_chg)}"
        else:
            signal_str = "—"
            conf_str = "—"
            price_str = "—"
            day_chg_str = "—"
        lines.append(
            f"| {i} | **{sym}** | {sym_cfg['name']} | {sym_cfg['type'].upper()} "
            f"| {price_str} | {day_chg_str} | {signal_str} | {conf_str} |"
        )

    lines += [
        "",
        "---",
        "",
        "### 🔮 Tomorrow's Predictions",
        "",
        "> _Momentum-based forecast only — not financial advice. "
        "Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._",
        "",
        "| # | Symbol | Name | Predicted Action | Confidence | Basis |",
        "|--:|:-------|:-----|:----------------:|-----------:|:------|",
    ]
    for i, sym_cfg in enumerate(watchlist, 1):
        sym = sym_cfg["symbol"]
        sig = (signal_map or {}).get(sym)
        pred = (sig or {}).get("prediction") if sig else None
        if pred:
            p_act = str(pred.get("predicted_action", "HOLD"))
            p_conf = float(pred.get("predicted_confidence", 0.5))
            p_basis = str(pred.get("basis", "—"))
            act_fmt = f"**{p_act}**" if p_act != "HOLD" else "HOLD"
            conf_fmt = f"{p_conf:.0%}"
        else:
            act_fmt = "—"
            conf_fmt = "—"
            p_basis = "—"
        lines.append(
            f"| {i} | **{sym}** | {sym_cfg['name']} | {act_fmt} | {conf_fmt} | {p_basis} |"
        )

    lines += [
        "",
        "---",
        "",
        "_Dashboard auto-updated by "
        "[GitHub Actions](.github/workflows/daily_trade.yml) · "
        "Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_",
        "",
    ]
    return "\n".join(lines)


def update_readme(content: str, readme_path: str = README_PATH) -> None:
    """Replace or append the dashboard section in README.md."""
    if not os.path.exists(readme_path):
        return

    with open(readme_path, encoding="utf-8") as f:
        readme = f.read()

    new_block = f"{DASHBOARD_START}\n{content}\n{DASHBOARD_END}"
    pattern = rf"{re.escape(DASHBOARD_START)}.*?{re.escape(DASHBOARD_END)}"

    if re.search(pattern, readme, re.DOTALL):
        updated = re.sub(pattern, new_block, readme, flags=re.DOTALL)
    else:
        updated = readme.rstrip() + f"\n\n{new_block}\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated)

