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

> 🕐 **Last updated:** 2026-10-02 13:51 UTC &nbsp;|&nbsp; **Trades today:** 0 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🧭 Configured Strategy Budget | `$10,000.00` |
| 🛡️ Strategy Max Gross Exposure | `$8,000.00` |
| 💵 Alpaca Paper Account Equity | `$118,727.61` |
| 💸 Broker Cash Available | `$-118,533.96` |
| 🧾 Broker Buying Power | `$123,117.66` |
| 📦 Actual Broker Gross Exposure | `$237,259.89` |
| 🟢 Broker Position P&L | `+$30,624.72` &nbsp; `(+306.25%)` |
| 📆 Daily P&L (final equity - start of day) | `$-3.64` |

### ⚠️ LEGACY PAPER ACCOUNT STATE

The current Alpaca paper account contains positions created before the present `$10,000` risk controls were enforced.

Current broker equity/P&L should not be interpreted as performance of the current hardened strategy.

The bot will warn, block additional BUY exposure, and continue allowing valid risk-reducing SELLs.

### ⚠️ Safety Warnings

- Current gross exposure $237259.89 exceeds the configured limit of $8000.00. New BUY orders are blocked until exposure is reduced.
- LEGACY PAPER ACCOUNT STATE: current broker equity/P&L may reflect positions created before the hardened $10,000 strategy controls were enforced.
- Existing AAPL position value $23213.05 exceeds the configured per-position limit of $1000.00.
- Existing AMZN position value $15114.00 exceeds the configured per-position limit of $1000.00.
- Existing AVGO position value $7407.65 exceeds the configured per-position limit of $1000.00.
- Existing BTC/USD position value $17803.68 exceeds the configured per-position limit of $1000.00.
- Existing ETH/USD position value $1723.84 exceeds the configured per-position limit of $1000.00.
- Existing GOOGL position value $11679.34 exceeds the configured per-position limit of $1000.00.
- Existing LLY position value $52960.26 exceeds the configured per-position limit of $1000.00.
- Existing META position value $21904.55 exceeds the configured per-position limit of $1000.00.
- Existing MSFT position value $16520.32 exceeds the configured per-position limit of $1000.00.
- Existing NVDA position value $42933.20 exceeds the configured per-position limit of $1000.00.
- Existing SOL/USD position value $1894.97 exceeds the configured per-position limit of $1000.00.
- Existing SPY position value $4627.74 exceeds the configured per-position limit of $1000.00.
- Existing TSLA position value $8868.23 exceeds the configured per-position limit of $1000.00.
- Existing VTI position value $10609.06 exceeds the configured per-position limit of $1000.00.

### 📝 Daily Trade Summary

- **Broker position P&L:** `+$30,624.72` (+306.25%)
- **Daily P&L:** `$-3.64`
- **Executed today:** No buy/sell orders were approved in this run.

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $331.62 | $23,213.05 | 🟢 +$1,683.44 | +7.82% |
| **AMZN** | STOCK | 60.00 | $249.93 | $251.90 | $15,114.00 | 🟢 +$118.10 | +0.79% |
| **AVGO** | STOCK | 21.00 | $379.32 | $352.75 | $7,407.65 | 🔴 $-558.13 | -7.01% |
| **BTC/USD** | CRYPTO | 0.2054 | $3,347.26 | $86,680.22 | $17,803.68 | 🟢 +$17,116.17 | +2489.59% |
| **ETH/USD** | CRYPTO | 0.6272 | N/A | $2,748.30 | $1,723.84 | 🟢 +$1,723.84 | 0.00% |
| **GOOGL** | STOCK | 34.00 | $350.77 | $343.51 | $11,679.34 | 🔴 $-246.98 | -2.07% |
| **LLY** | STOCK | 46.00 | $1,179.52 | $1,151.31 | $52,960.26 | 🔴 $-1,297.52 | -2.39% |
| **META** | STOCK | 30.00 | $595.70 | $730.15 | $21,904.55 | 🟢 +$4,033.52 | +22.57% |
| **MSFT** | STOCK | 32.00 | $416.49 | $516.26 | $16,520.32 | 🟢 +$3,192.69 | +23.96% |
| **NVDA** | STOCK | 181.00 | $214.73 | $237.20 | $42,933.20 | 🟢 +$4,067.01 | +10.46% |
| **SOL/USD** | CRYPTO | 15.42 | N/A | $122.90 | $1,894.97 | 🟢 +$1,894.97 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $771.29 | $4,627.74 | 🟢 +$155.08 | +3.47% |
| **TSLA** | STOCK | 24.00 | $432.23 | $369.51 | $8,868.23 | 🔴 $-1,505.34 | -14.51% |
| **VTI** | ETF | 28.00 | $370.04 | $378.89 | $10,609.06 | 🟢 +$247.86 | +2.39% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $237.22 | 🟢 +2.67% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $331.63 | 🟢 +0.36% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $343.52 | 🟢 +1.52% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $516.14 | 🟢 +0.67% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $251.90 | 🟢 +1.46% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $378.86 | 🟢 +0.98% | HOLD | — |
| 7 | **META** | Meta Platforms Inc. | STOCK | $730.30 | 🟢 +0.63% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $86,680.22 | 🟢 +2.16% | HOLD | — |
| 9 | **AVGO** | Broadcom Inc. | STOCK | $352.75 | 🟢 +2.60% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,152.60 | 🟢 +0.17% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 68% | Extreme gain today (+2.67%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.36%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.52%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.67%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.46%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.98%) — continuation expected |
| 7 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.63%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+2.16%) — continuation expected |
| 9 | **AVGO** | Broadcom Inc. | **SELL** | 68% | Extreme gain today (+2.60%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.17%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
