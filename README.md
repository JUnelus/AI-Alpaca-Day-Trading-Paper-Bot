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

> 🕐 **Last updated:** 2026-08-27 23:23 UTC &nbsp;|&nbsp; **Trades today:** 0 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🧭 Configured Strategy Budget | `$10,000.00` |
| 🛡️ Strategy Max Gross Exposure | `$8,000.00` |
| 💵 Alpaca Paper Account Equity | `$109,813.67` |
| 💸 Broker Cash Available | `$-123,214.77` |
| 🧾 Broker Buying Power | `$91,998.83` |
| 📦 Actual Broker Gross Exposure | `$233,028.44` |
| 🟢 Broker Position P&L | `+$22,422.69` &nbsp; `(+224.23%)` |
| 📆 Daily P&L (final equity - start of day) | `$-0.05` |

### ⚠️ LEGACY PAPER ACCOUNT STATE

The current Alpaca paper account contains positions created before the present `$10,000` risk controls were enforced.

Current broker equity/P&L should not be interpreted as performance of the current hardened strategy.

The bot will warn, block additional BUY exposure, and continue allowing valid risk-reducing SELLs.

### ⚠️ Safety Warnings

- Current gross exposure $233028.44 exceeds the configured limit of $8000.00. New BUY orders are blocked until exposure is reduced.
- LEGACY PAPER ACCOUNT STATE: current broker equity/P&L may reflect positions created before the hardened $10,000 strategy controls were enforced.
- Existing AAPL position value $22021.02 exceeds the configured per-position limit of $1000.00.
- Existing AMZN position value $15389.98 exceeds the configured per-position limit of $1000.00.
- Existing AVGO position value $8546.80 exceeds the configured per-position limit of $1000.00.
- Existing BTC/USD position value $18452.89 exceeds the configured per-position limit of $1000.00.
- Existing ETH/USD position value $1578.32 exceeds the configured per-position limit of $1000.00.
- Existing GOOGL position value $11579.72 exceeds the configured per-position limit of $1000.00.
- Existing LLY position value $54088.18 exceeds the configured per-position limit of $1000.00.
- Existing META position value $18861.48 exceeds the configured per-position limit of $1000.00.
- Existing MSFT position value $16114.88 exceeds the configured per-position limit of $1000.00.
- Existing NVDA position value $40927.72 exceeds the configured per-position limit of $1000.00.
- Existing SOL/USD position value $1688.51 exceeds the configured per-position limit of $1000.00.
- Existing SPY position value $4619.63 exceeds the configured per-position limit of $1000.00.
- Existing TSLA position value $8508.11 exceeds the configured per-position limit of $1000.00.
- Existing VTI position value $10651.20 exceeds the configured per-position limit of $1000.00.

### 📝 Daily Trade Summary

- **Broker position P&L:** `+$22,422.69` (+224.23%)
- **Daily P&L:** `$-0.05`
- **Executed today:** No buy/sell orders were approved in this run.

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $314.59 | $22,021.02 | 🟢 +$491.41 | +2.28% |
| **AMZN** | STOCK | 60.00 | $249.93 | $256.50 | $15,389.98 | 🟢 +$394.08 | +2.63% |
| **AVGO** | STOCK | 23.00 | $379.55 | $371.60 | $8,546.80 | 🔴 $-182.75 | -2.09% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $80,371.48 | $18,452.89 | 🟢 +$16,204.74 | +720.81% |
| **ETH/USD** | CRYPTO | 0.6272 | N/A | $2,516.30 | $1,578.32 | 🟢 +$1,578.32 | 0.00% |
| **GOOGL** | STOCK | 34.00 | $350.77 | $340.58 | $11,579.72 | 🔴 $-346.60 | -2.91% |
| **LLY** | STOCK | 46.00 | $1,179.52 | $1,175.83 | $54,088.18 | 🔴 $-169.60 | -0.31% |
| **META** | STOCK | 33.00 | $591.43 | $571.56 | $18,861.48 | 🔴 $-655.71 | -3.36% |
| **MSFT** | STOCK | 32.00 | $416.49 | $503.59 | $16,114.88 | 🟢 +$2,787.25 | +20.91% |
| **NVDA** | STOCK | 181.00 | $214.73 | $226.12 | $40,927.72 | 🟢 +$2,061.53 | +5.30% |
| **SOL/USD** | CRYPTO | 15.42 | N/A | $109.51 | $1,688.51 | 🟢 +$1,688.51 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $769.94 | $4,619.63 | 🟢 +$146.97 | +3.29% |
| **TSLA** | STOCK | 24.00 | $432.23 | $354.50 | $8,508.11 | 🔴 $-1,865.46 | -17.98% |
| **VTI** | ETF | 28.00 | $370.04 | $380.40 | $10,651.20 | 🟢 +$290.00 | +2.80% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $228.17 | 🟢 +8.77% | **SELL** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $314.54 | 🟢 +0.34% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $340.59 | 🔴 -0.43% | **BUY** | 75% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $504.98 | 🟢 +1.74% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $256.15 | 🔴 -1.57% | **BUY** | 95% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $380.63 | 🟢 +0.63% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $371.22 | 🟢 +4.40% | **SELL** | 100% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $80,371.48 | 🟢 +1.71% | HOLD | — |
| 9 | **META** | Meta Platforms Inc. | STOCK | $571.03 | 🔴 -0.91% | **BUY** | 83% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,175.64 | 🔴 -1.15% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 78% | Extreme gain today (+8.77%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.34%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 66% | Moderate negative momentum (-0.43%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.74%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 84% | Moderate negative momentum (-1.57%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.63%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 77% | Extreme gain today (+4.40%) — mean reversion pullback likely |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.71%) — continuation expected |
| 9 | **META** | Meta Platforms Inc. | **SELL** | 73% | Moderate negative momentum (-0.91%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 75% | Moderate negative momentum (-1.15%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
