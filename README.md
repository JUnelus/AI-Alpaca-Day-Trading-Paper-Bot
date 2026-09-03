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

> 🕐 **Last updated:** 2026-09-03 20:23 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🧭 Configured Strategy Budget | `$10,000.00` |
| 🛡️ Strategy Max Gross Exposure | `$8,000.00` |
| 💵 Alpaca Paper Account Equity | `$112,511.54` |
| 💸 Broker Cash Available | `$-122,597.89` |
| 🧾 Broker Buying Power | `$99,382.75` |
| 📦 Actual Broker Gross Exposure | `$235,109.43` |
| 🟢 Broker Position P&L | `+$25,095.12` &nbsp; `(+250.95%)` |
| 📆 Daily P&L (final equity - start of day) | `+$1,653.33` |

### ⚠️ LEGACY PAPER ACCOUNT STATE

The current Alpaca paper account contains positions created before the present `$10,000` risk controls were enforced.

Current broker equity/P&L should not be interpreted as performance of the current hardened strategy.

The bot will warn, block additional BUY exposure, and continue allowing valid risk-reducing SELLs.

### ⚠️ Safety Warnings

- Current gross exposure $235109.43 exceeds the configured limit of $8000.00. New BUY orders are blocked until exposure is reduced.
- LEGACY PAPER ACCOUNT STATE: current broker equity/P&L may reflect positions created before the hardened $10,000 strategy controls were enforced.
- Existing AAPL position value $22950.90 exceeds the configured per-position limit of $1000.00.
- Existing AMZN position value $15537.60 exceeds the configured per-position limit of $1000.00.
- Existing AVGO position value $8214.45 exceeds the configured per-position limit of $1000.00.
- Existing BTC/USD position value $18695.73 exceeds the configured per-position limit of $1000.00.
- Existing ETH/USD position value $1573.09 exceeds the configured per-position limit of $1000.00.
- Existing GOOGL position value $11645.00 exceeds the configured per-position limit of $1000.00.
- Existing LLY position value $53341.60 exceeds the configured per-position limit of $1000.00.
- Existing META position value $19530.00 exceeds the configured per-position limit of $1000.00.
- Existing MSFT position value $16303.68 exceeds the configured per-position limit of $1000.00.
- Existing NVDA position value $41353.21 exceeds the configured per-position limit of $1000.00.
- Existing SOL/USD position value $1622.67 exceeds the configured per-position limit of $1000.00.
- Existing SPY position value $4635.24 exceeds the configured per-position limit of $1000.00.
- Existing TSLA position value $9044.88 exceeds the configured per-position limit of $1000.00.
- Existing VTI position value $10661.37 exceeds the configured per-position limit of $1000.00.

### 📝 Daily Trade Summary

- **Broker position P&L:** `+$25,095.12` (+250.95%)
- **Daily P&L:** `+$1,653.33`
- **Executed today:** No buy/sell orders were approved in this run.

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $327.87 | $22,950.90 | 🟢 +$1,421.29 | +6.60% |
| **AMZN** | STOCK | 60.00 | $249.93 | $258.96 | $15,537.60 | 🟢 +$541.70 | +3.61% |
| **AVGO** | STOCK | 23.00 | $379.55 | $357.15 | $8,214.45 | 🔴 $-515.10 | -5.90% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $81,429.20 | $18,695.73 | 🟢 +$16,447.59 | +731.61% |
| **ETH/USD** | CRYPTO | 0.6272 | N/A | $2,507.96 | $1,573.09 | 🟢 +$1,573.09 | 0.00% |
| **GOOGL** | STOCK | 34.00 | $350.77 | $342.50 | $11,645.00 | 🔴 $-281.32 | -2.36% |
| **LLY** | STOCK | 46.00 | $1,179.52 | $1,159.60 | $53,341.60 | 🔴 $-916.18 | -1.69% |
| **META** | STOCK | 32.00 | $591.43 | $610.31 | $19,530.00 | 🟢 +$604.24 | +3.19% |
| **MSFT** | STOCK | 32.00 | $416.49 | $509.49 | $16,303.68 | 🟢 +$2,976.05 | +22.33% |
| **NVDA** | STOCK | 181.00 | $214.73 | $228.47 | $41,353.21 | 🟢 +$2,487.02 | +6.40% |
| **SOL/USD** | CRYPTO | 15.42 | N/A | $105.24 | $1,622.67 | 🟢 +$1,622.67 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $772.54 | $4,635.24 | 🟢 +$162.58 | +3.64% |
| **TSLA** | STOCK | 24.00 | $432.23 | $376.87 | $9,044.88 | 🔴 $-1,328.69 | -12.81% |
| **VTI** | ETF | 28.00 | $370.04 | $380.76 | $10,661.37 | 🟢 +$300.17 | +2.90% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $228.54 | 🟢 +1.83% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $328.22 | 🟢 +0.98% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $342.39 | 🟢 +1.56% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $510.15 | 🟢 +2.70% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $258.93 | 🟢 +1.58% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $380.97 | 🟢 +1.08% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $357.19 | 🔴 -2.80% | **BUY** | 100% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $81,429.20 | 🟢 +5.32% | **SELL** | 100% |
| 9 | **META** | Meta Platforms Inc. | STOCK | $610.68 | 🟢 +2.99% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,159.54 | 🔴 -0.02% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.83%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.98%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.56%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 68% | Extreme gain today (+2.70%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.58%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.08%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 69% | Extreme loss today (-2.80%) — mean reversion pullback likely |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 78% | Extreme gain today (+5.32%) — mean reversion pullback likely |
| 9 | **META** | Meta Platforms Inc. | **SELL** | 70% | Extreme gain today (+2.99%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.02%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
