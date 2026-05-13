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


def _fmt_pct(value: float) -> str:
    prefix = "+" if value > 0 else ""
    return f"{prefix}{value:.2f}%"


def _qty_str(qty: float) -> str:
    return f"{qty:.4f}" if qty < 10 else f"{qty:.2f}"


# ── core ───────────────────────────────────────────────────────────────────────

def generate_dashboard(
    state: PortfolioState,
    watchlist: List[dict],
    signal_map: Optional[Dict[str, dict]] = None,
) -> str:
    """Return the markdown content that sits between the two marker comments."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pnl_icon = _icon(state.total_pnl)

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
        f"| 🏦 Starting Balance  | `$10,000.00` |",
        f"| 💵 Current Equity    | `${state.account_equity:,.2f}` |",
        f"| 💸 Cash Available    | `${state.cash:,.2f}` |",
        f"| {pnl_icon} Total P&L | `{_fmt_usd(state.total_pnl, sign=True)}` "
        f"&nbsp; `({_fmt_pct(state.total_pnl_pct)})` |",
        "",
    ]

    # ── open positions ─────────────────────────────────────────────────────────
    lines.append("### 📈 Open Positions")
    lines.append("")
    if state.positions:
        lines += [
            "| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |",
            "|:-------|:----:|----:|---------:|------:|----------:|---------------:|------:|",
        ]
        for pos in state.positions:
            icon = _icon(pos.unrealized_pnl)
            lines.append(
                f"| **{pos.symbol}** | {pos.asset_type.upper()} "
                f"| {_qty_str(pos.qty)} "
                f"| ${pos.avg_entry_price:,.2f} "
                f"| ${pos.current_price:,.2f} "
                f"| ${pos.market_value:,.2f} "
                f"| {icon} {_fmt_usd(pos.unrealized_pnl, sign=True)} "
                f"| {_fmt_pct(pos.unrealized_pnl_pct)} |"
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

