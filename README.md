# AI-Alpaca-Day-Trading-Paper-Bot

AI-powered Alpaca **paper-trading** bot using Python, risk management, structured AI decisions, and automated trade analytics.

**$10,000 configured paper portfolio · 10 symbols · fail-closed safety checks · GitHub Actions trade/report schedules**

> This repository remains **Alpaca paper-trading only**. No supported path in this repo enables Alpaca live trading.

---

## 🏗️ Architecture

```text
Market Data (fresh Alpaca snapshots only for trade mode)
    → Strategy Rules
    → AI Agent Decision
    → Centralized Risk Manager
    → Protected Alpaca Paper Execution
    → Trade Log / Portfolio State / Dashboard / Email Report
```

The AI agent returns **structured decisions only** — it never places orders directly.
Order placement is allowed only when `--mode trade` is active.

## 📁 Project Structure

```text
ai-alpaca-day-trading-paper-bot/
├── .github/workflows/ci.yml            ← Push / PR tests only
├── .github/workflows/daily_trade.yml   ← Scheduled/manual paper bot runs
├── .env.example
├── requirements.txt
├── config/
│   └── watchlist.json                  ← 10 symbols + risk config
├── src/
│   ├── main.py                         ← Orchestrator
│   ├── market_data.py                  ← Alpaca data API (real prices)
│   ├── strategy.py                     ← Momentum signal generation
│   ├── ai_agent.py                     ← Structured decision builder
│   ├── risk_manager.py                 ← Rule enforcement
│   ├── portfolio.py                    ← Live P&L from Alpaca account
│   ├── dashboard.py                    ← README dashboard generator
│   ├── alpaca_client.py                ← Alpaca trading client wrapper
│   └── logger.py                       ← CSV + markdown logging
├── data/
│   ├── trade_log.csv
│   └── portfolio_state.json
└── reports/
    └── daily_summary.md
```

## 🎯 Watchlist — 10 Symbols

> The active 10 symbols are refreshed automatically once per ISO week from a larger universe,
> ranked by market value (market cap for stocks/crypto, total assets fallback for ETFs).

|  # | Symbol  | Name                |  Type  |
|---:|:--------|:--------------------|:------:|
|  1 | AAPL    | Apple Inc.          | STOCK  |
|  2 | NVDA    | NVIDIA Corp.        | STOCK  |
|  3 | TSLA    | Tesla Inc.          | STOCK  |
|  4 | MSFT    | Microsoft Corp.     | STOCK  |
|  5 | AMZN    | Amazon.com Inc.     | STOCK  |
|  6 | META    | Meta Platforms Inc. | STOCK  |
|  7 | SPY     | SPDR S&P 500 ETF    |  ETF   |
|  8 | BTC/USD | Bitcoin             | CRYPTO |
|  9 | ETH/USD | Ethereum            | CRYPTO |
| 10 | SOL/USD | Solana              | CRYPTO |

## 🛡️ Safety Controls

| Rule | Policy |
|:-----|:-------|
| Trading venue | Alpaca **paper** account only |
| Runtime modes | `trade` may place orders; `report` can never place orders |
| Watchlist refresh | Weekly top-10 by market value |
| Entry logic | Existing strategy / AI logic preserved, but enforced through fail-closed risk checks |
| Min AI confidence | `MIN_CONFIDENCE=0.70` |
| Max account risk per trade | `MAX_RISK_PERCENT=1`, applied to `min(PORTFOLIO_SIZE, live account equity)` |
| Portfolio budget | `PORTFOLIO_SIZE=10000` |
| Max position size | `MAX_POSITION_PERCENT=10` (default $1,000 per symbol) |
| Max total gross exposure | `MAX_TOTAL_EXPOSURE_PERCENT=80` (default $8,000) |
| Daily trade cap | `MAX_DAILY_TRADES=3` across the whole bot |
| Per-symbol trade cap | Max 1 executed trade per symbol per trading day |
| Daily loss circuit breaker | `MAX_DAILY_LOSS_PERCENT=2` blocks new BUYs after the threshold is hit |
| Margin | `ALLOW_MARGIN=false` |
| Shorts | `ALLOW_SHORTS=false` |
| Protective stop policy | New long stock/ETF BUYs must have broker-side `GTC` broker-side stop protection or the entry is rejected |
| Crypto BUY safety | Rejected whenever reliable broker-side protective stops cannot be guaranteed |
| Market-data safety | Fallback/demo prices are **never** eligible for paper-order execution |
| Scheduled automation idempotency | Scheduled trade/report runs persist once-per-Eastern-trading-day markers |
| Logging | Every decision is logged, including execution status, protection state, order IDs, and rejection reasons |

### Default Safety Configuration

These values live in `config/watchlist.json` and can be overridden in `.env`:

```dotenv
PORTFOLIO_SIZE=10000
MAX_POSITION_PERCENT=10
MAX_DAILY_LOSS_PERCENT=2
MAX_DAILY_TRADES=3
MAX_TOTAL_EXPOSURE_PERCENT=80
ALLOW_MARGIN=false
ALLOW_SHORTS=false
MIN_CONFIDENCE=0.70
MAX_RISK_PERCENT=1
```

### Protective Stop Behavior

- For new long **stock/ETF BUY** orders, the bot submits broker-side protection through Alpaca-supported attached stop logic using **`GTC`** protection so the stop can persist beyond the current session.
- Attached OTO protection is only treated as active after bounded polling confirms an actual stop child with a valid child order ID, stop price, side, and quantity.
- If the bot cannot reliably create that protective stop, it **rejects the BUY** instead of placing an unprotected entry.
- If an entry is accepted/executed but protection confirmation fails, the run records a **critical protection failure** and does not treat the trade as safely protected.
- Normal long **SELL-to-close** orders do not create a new entry-style stop.

### Protective Stop Reconciliation on SELL

- Before a long **SELL-to-close**, the bot discovers any active broker-side protective stop(s) for that symbol.
- For a **full exit**, it cancels and verifies the protective stop(s) before submitting the close order.
- If the close SELL fails after cancellation, the bot attempts to **restore the original protective stop** for the verified remaining broker position.
- For a **partial exit**, it cancels the prior protection, executes the SELL, then replaces protection for the **verified broker-side remaining long quantity** using the existing stop price when that can be determined safely.
- Cancellation verification and attached-stop confirmation both use **bounded broker-state polling** so normal asynchronous broker updates such as `pending_cancel` do not cause unsafe duplicate actions.
- If the bot cannot safely identify, cancel, verify, or replace protection, it fails to close and returns a structured warning/failure instead of risking a stale stop that could create an unintended short.

### Risk Base

- `MAX_RISK_PERCENT` is calculated against:

```text
min(PORTFOLIO_SIZE, current account equity)
```

- Example: if `PORTFOLIO_SIZE=10000` and Alpaca paper equity is `$108,000`, a `1%` max-risk policy still limits allowed trade risk to `$100`.
- If live paper equity falls below the configured budget, the bot becomes even more conservative and uses the lower equity value instead.

### Daily P&L Consistency

- The persisted daily P&L invariant is:

```text
daily_pnl = final account equity - start_of_day_equity
```

- `start_of_day_equity` is established on the first valid run of a new `America/New_York` trading day and preserved on later runs that same Eastern day.
- The dashboard, JSON state, summary report, and daily-loss circuit breaker all use that same authoritative final equity relationship.

### Market Data Safety

- `trade` mode requires fresh Alpaca market data.
- If fresh data is missing for a symbol, that symbol is not traded.
- If the overall market-data service is unavailable, the bot places **zero** orders.
- Hard-coded fallback/demo prices are limited to tests and explicit local reporting/simulation flows such as `--mode report --allow-fallback-data`.

### Email Failure and State Persistence

- Broker execution state is persisted before email delivery is treated as complete.
- If email delivery fails, the bot preserves `data/trade_log.csv`, `data/portfolio_state.json`, `reports/daily_summary.md`, and `README.md` so reruns still see the recorded trade state.
- If `EMAIL_REQUIRED=true`, the bot may still fail the run **after** state persistence, so the notification problem is surfaced without erasing execution history.

### Broker Data Quality

- Broker cost basis and unrealized P&L fields are used directly when Alpaca provides them.
- If cost basis or unrealized P&L cannot be verified reliably for a position, the bot shows **`N/A`** instead of treating market value as profit.
- Broker portfolio P&L is marked **partial** whenever one or more positions lack reliable cost-basis/P&L data.

## ⚙️ GitHub Actions Setup

1. Go to **Settings → Secrets and variables → Actions** in your repo.
2. Add your repository secrets:
   - `ALPACA_API_KEY`
   - `ALPACA_SECRET_KEY`
   - `SENDER_EMAIL`
   - `SENDER_PASSWORD`
   - `RECIPIENT_EMAIL`
3. Workflow behavior is split for safety:
   - `.github/workflows/ci.yml`
     - runs on `push` and `pull_request`
     - installs dependencies and runs `python -m pytest -q`
     - **never** places broker orders
   - `.github/workflows/daily_trade.yml`
      - scheduled morning run: `python -m src.main --mode trade --scheduled-run`
      - scheduled afternoon run: `python -m src.main --mode report --scheduled-run`
     - manual runs require an explicit mode choice and default to `report`
     - every bot run forces `ALPACA_PAPER=true`
      - state-mutating bot runs are serialized with GitHub Actions concurrency (`alpaca-paper-trading-bot`)
      - state commit steps still run after bot-step failures, so email issues cannot prevent execution-state commits
      - native GitHub schedule timezone is `America/New_York`
      - scheduled trade/report runs use persisted once-per-trading-day markers so accidental reruns become no-ops

> The scheduled workflow runs at **9:45 AM America/New_York** for trade mode and **4:15 PM America/New_York** for report mode through both EST and EDT using native GitHub timezone scheduling.

## 🚀 Local Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env          # then fill in your keys
python -m pytest -q                  # run tests
python -m src.main --mode report     # safe default: reporting/dashboard only
python -m src.main --mode trade      # paper-trading run with risk checks and broker orders
python -m src.main --mode trade --scheduled-run       # scheduled-trade idempotency markers enabled
python -m src.main --mode report --scheduled-run      # scheduled-report idempotency markers enabled
python -m src.main --mode report --allow-fallback-data   # explicit local simulation/reporting only
```

## 📌 Execution Notes

- Existing strategy logic, AI decisioning, dashboard updates, email reporting, trade logging, and weekly watchlist refresh are preserved.
- The hardened risk layer prevents DCA logic from bypassing per-position or total-exposure limits.
- Existing oversized paper positions are **not** auto-liquidated. The bot warns, blocks additional exposure, and still allows risk-reducing exits.
- Existing oversized paper positions continue to use the new sell-side protective-order reconciliation when they are reduced or closed.

---

<!-- PORTFOLIO_DASHBOARD_START -->

## 📊 Live Portfolio Dashboard

> 🕐 **Last updated:** 2026-09-15 20:23 UTC &nbsp;|&nbsp; **Trades today:** 0 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🧭 Configured Strategy Budget | `$10,000.00` |
| 🛡️ Strategy Max Gross Exposure | `$8,000.00` |
| 💵 Alpaca Paper Account Equity | `$107,101.68` |
| 💸 Broker Cash Available | `$-121,950.33` |
| 🧾 Broker Buying Power | `$89,481.22` |
| 📦 Actual Broker Gross Exposure | `$229,052.01` |
| 🟢 Broker Position P&L | `+$19,551.20` &nbsp; `(+195.51%)` |
| 📆 Daily P&L (final equity - start of day) | `$-1,491.99` |

### ⚠️ LEGACY PAPER ACCOUNT STATE

The current Alpaca paper account contains positions created before the present `$10,000` risk controls were enforced.

Current broker equity/P&L should not be interpreted as performance of the current hardened strategy.

The bot will warn, block additional BUY exposure, and continue allowing valid risk-reducing SELLs.

### ⚠️ Safety Warnings

- Current gross exposure $229052.01 exceeds the configured limit of $8000.00. New BUY orders are blocked until exposure is reduced.
- LEGACY PAPER ACCOUNT STATE: current broker equity/P&L may reflect positions created before the hardened $10,000 strategy controls were enforced.
- Existing AAPL position value $23201.89 exceeds the configured per-position limit of $1000.00.
- Existing AMZN position value $14910.60 exceeds the configured per-position limit of $1000.00.
- Existing AVGO position value $7803.90 exceeds the configured per-position limit of $1000.00.
- Existing BTC/USD position value $17422.51 exceeds the configured per-position limit of $1000.00.
- Existing ETH/USD position value $1509.52 exceeds the configured per-position limit of $1000.00.
- Existing GOOGL position value $11720.82 exceeds the configured per-position limit of $1000.00.
- Existing LLY position value $52261.06 exceeds the configured per-position limit of $1000.00.
- Existing META position value $20797.90 exceeds the configured per-position limit of $1000.00.
- Existing MSFT position value $15924.75 exceeds the configured per-position limit of $1000.00.
- Existing NVDA position value $38438.97 exceeds the configured per-position limit of $1000.00.
- Existing SOL/USD position value $1502.39 exceeds the configured per-position limit of $1000.00.
- Existing SPY position value $4548.30 exceeds the configured per-position limit of $1000.00.
- Existing TSLA position value $8558.40 exceeds the configured per-position limit of $1000.00.
- Existing VTI position value $10451.00 exceeds the configured per-position limit of $1000.00.
- Daily loss circuit breaker triggered: Start-of-day equity: $108593.67; Current equity: $107101.68; Daily P&L: $-1491.99; Limit: -$200.00.

### 📝 Daily Trade Summary

- **Broker position P&L:** `+$19,551.20` (+195.51%)
- **Daily P&L:** `$-1,491.99`
- **Executed today:** No buy/sell orders were approved in this run.

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $331.46 | $23,201.89 | 🟢 +$1,672.29 | +7.77% |
| **AMZN** | STOCK | 60.00 | $249.93 | $248.51 | $14,910.60 | 🔴 $-85.30 | -0.57% |
| **AVGO** | STOCK | 23.00 | $379.55 | $339.30 | $7,803.90 | 🔴 $-925.65 | -10.60% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $75,883.70 | $17,422.51 | 🟢 +$15,174.37 | +674.97% |
| **ETH/USD** | CRYPTO | 0.6272 | N/A | $2,406.60 | $1,509.52 | 🟢 +$1,509.52 | 0.00% |
| **GOOGL** | STOCK | 34.00 | $350.77 | $344.73 | $11,720.82 | 🔴 $-205.50 | -1.72% |
| **LLY** | STOCK | 46.00 | $1,179.52 | $1,136.11 | $52,261.06 | 🔴 $-1,996.72 | -3.68% |
| **META** | STOCK | 31.00 | $593.94 | $670.90 | $20,797.90 | 🟢 +$2,385.64 | +12.96% |
| **MSFT** | STOCK | 32.00 | $416.49 | $497.65 | $15,924.75 | 🟢 +$2,597.12 | +19.49% |
| **NVDA** | STOCK | 181.00 | $214.73 | $212.37 | $38,438.97 | 🔴 $-427.22 | -1.10% |
| **SOL/USD** | CRYPTO | 15.42 | N/A | $97.44 | $1,502.39 | 🟢 +$1,502.39 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $758.05 | $4,548.30 | 🟢 +$75.64 | +1.69% |
| **TSLA** | STOCK | 24.00 | $432.23 | $356.60 | $8,558.40 | 🔴 $-1,815.17 | -17.50% |
| **VTI** | ETF | 28.00 | $370.04 | $373.25 | $10,451.00 | 🟢 +$89.80 | +0.87% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $212.16 | 🟢 +0.55% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $331.33 | 🔴 -0.50% | **BUY** | 77% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $344.98 | 🔴 -1.28% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $497.11 | 🔴 -1.70% | **BUY** | 98% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $248.45 | 🔴 -2.00% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $372.75 | 🔴 -0.51% | **BUY** | 76% |
| 7 | **META** | Meta Platforms Inc. | STOCK | $670.49 | 🟢 +0.73% | HOLD | — |
| 8 | **AVGO** | Broadcom Inc. | STOCK | $339.30 | 🔴 -1.55% | **BUY** | 94% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $75,883.70 | 🔴 -2.93% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,136.71 | 🔴 -0.14% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+0.55%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 68% | Moderate negative momentum (-0.50%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.28%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.70%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.00%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 66% | Moderate negative momentum (-0.51%) — continuation expected |
| 7 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.73%) — continuation expected |
| 8 | **AVGO** | Broadcom Inc. | **SELL** | 83% | Moderate negative momentum (-1.55%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 70% | Extreme loss today (-2.93%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.14%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
