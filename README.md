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
| Protective stop policy | New long stock/ETF BUYs must have broker-side stop protection or the entry is rejected |
| Crypto BUY safety | Rejected whenever reliable broker-side protective stops cannot be guaranteed |
| Market-data safety | Fallback/demo prices are **never** eligible for paper-order execution |
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
- If the bot cannot reliably create that protective stop, it **rejects the BUY** instead of placing an unprotected entry.
- If an entry is accepted/executed but protection confirmation fails, the run records a **critical protection failure** and does not treat the trade as safely protected.
- Normal long **SELL-to-close** orders do not create a new entry-style stop.

### Protective Stop Reconciliation on SELL

- Before a long **SELL-to-close**, the bot discovers any active broker-side protective stop(s) for that symbol.
- For a **full exit**, it cancels and verifies the protective stop(s) before submitting the close order.
- For a **partial exit**, it cancels the prior protection, executes the SELL, then replaces protection for the remaining long quantity using the existing stop price when that can be determined safely.
- If the bot cannot safely identify, cancel, verify, or replace protection, it fails closed and returns a structured warning/failure instead of risking a stale stop that could create an unintended short.

### Risk Base

- `MAX_RISK_PERCENT` is calculated against:

```text
min(PORTFOLIO_SIZE, current account equity)
```

- Example: if `PORTFOLIO_SIZE=10000` and Alpaca paper equity is `$108,000`, a `1%` max-risk policy still limits allowed trade risk to `$100`.
- If live paper equity falls below the configured budget, the bot becomes even more conservative and uses the lower equity value instead.

### Market Data Safety

- `trade` mode requires fresh Alpaca market data.
- If fresh data is missing for a symbol, that symbol is not traded.
- If the overall market-data service is unavailable, the bot places **zero** orders.
- Hard-coded fallback/demo prices are limited to tests and explicit local reporting/simulation flows such as `--mode report --allow-fallback-data`.

### Email Failure and State Persistence

- Broker execution state is persisted before email delivery is treated as complete.
- If email delivery fails, the bot preserves `data/trade_log.csv`, `data/portfolio_state.json`, `reports/daily_summary.md`, and `README.md` so reruns still see the recorded trade state.
- If `EMAIL_REQUIRED=true`, the bot may still fail the run **after** state persistence so the notification problem is surfaced without erasing execution history.

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
      - scheduled morning run: `python -m src.main --mode trade --enforce-schedule`
      - scheduled afternoon run: `python -m src.main --mode report --enforce-schedule`
     - manual runs require an explicit mode choice and default to `report`
     - every bot run forces `ALPACA_PAPER=true`
      - state-mutating bot runs are serialized with GitHub Actions concurrency (`alpaca-paper-trading-bot`)
      - state commit steps still run after bot-step failures so email issues cannot prevent execution-state commits

> GitHub cron uses UTC, so the workflow schedules both EDT and EST candidate UTC times and the bot performs a strict `America/New_York` runtime check. Only the correct local `9:45 AM ET` trade window or `4:15 PM ET` report window is allowed to continue.

## 🚀 Local Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env          # then fill in your keys
python -m pytest -q                  # run tests
python -m src.main --mode report     # safe default: reporting/dashboard only
python -m src.main --mode trade      # paper-trading run with risk checks and broker orders
python -m src.main --mode trade --enforce-schedule    # scheduled-trade safety guard
python -m src.main --mode report --enforce-schedule   # scheduled-report safety guard
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

> 🕐 **Last updated:** 2026-08-27 17:30 UTC &nbsp;|&nbsp; **Trades today:** 0 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$110,917.68` |
| 💸 Cash Available    | `$-123,214.77` |
| 🧾 Buying Power      | `$94,838.03` |
| 🟢 Total P&L | `+$23,526.71` &nbsp; `(+235.27%)` |

### ⚠️ Safety Warnings

- Current gross exposure $234132.45 exceeds the configured limit of $8000.00. New BUY orders are blocked until exposure is reduced.
- Existing AAPL position value $22065.40 exceeds the configured per-position limit of $1000.00.
- Existing AMZN position value $15347.40 exceeds the configured per-position limit of $1000.00.
- Existing AVGO position value $8481.94 exceeds the configured per-position limit of $1000.00.
- Existing BTC/USD position value $18542.61 exceeds the configured per-position limit of $1000.00.
- Existing ETH/USD position value $1586.00 exceeds the configured per-position limit of $1000.00.
- Existing GOOGL position value $11598.76 exceeds the configured per-position limit of $1000.00.
- Existing LLY position value $54617.18 exceeds the configured per-position limit of $1000.00.
- Existing META position value $18844.98 exceeds the configured per-position limit of $1000.00.
- Existing MSFT position value $16112.96 exceeds the configured per-position limit of $1000.00.
- Existing NVDA position value $41454.61 exceeds the configured per-position limit of $1000.00.
- Existing SOL/USD position value $1682.88 exceeds the configured per-position limit of $1000.00.
- Existing SPY position value $4630.26 exceeds the configured per-position limit of $1000.00.
- Existing TSLA position value $8502.00 exceeds the configured per-position limit of $1000.00.
- Existing VTI position value $10665.48 exceeds the configured per-position limit of $1000.00.

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$23,526.71` (+235.27%)
- **Yesterday-to-today P&L:** `+$2,675.37`
- **Executed today:** No buy/sell orders were approved in this run.

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $315.22 | $22,065.40 | 🟢 +$535.79 | +2.49% |
| **AMZN** | STOCK | 60.00 | $249.93 | $255.79 | $15,347.40 | 🟢 +$351.50 | +2.34% |
| **AVGO** | STOCK | 23.00 | $379.55 | $368.78 | $8,481.94 | 🔴 $-247.61 | -2.84% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $80,762.26 | $18,542.61 | 🟢 +$16,294.46 | +724.80% |
| **ETH/USD** | CRYPTO | 0.6272 | $0.00 | $2,528.53 | $1,586.00 | 🟢 +$1,586.00 | 0.00% |
| **GOOGL** | STOCK | 34.00 | $350.77 | $341.14 | $11,598.76 | 🔴 $-327.56 | -2.75% |
| **LLY** | STOCK | 46.00 | $1,179.52 | $1,187.33 | $54,617.18 | 🟢 +$359.40 | +0.66% |
| **META** | STOCK | 33.00 | $591.43 | $571.06 | $18,844.98 | 🔴 $-672.21 | -3.44% |
| **MSFT** | STOCK | 32.00 | $416.49 | $503.53 | $16,112.96 | 🟢 +$2,785.33 | +20.90% |
| **NVDA** | STOCK | 181.00 | $214.73 | $229.03 | $41,454.61 | 🟢 +$2,588.42 | +6.66% |
| **SOL/USD** | CRYPTO | 15.42 | $0.00 | $109.14 | $1,682.88 | 🟢 +$1,682.88 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $771.71 | $4,630.26 | 🟢 +$157.60 | +3.52% |
| **TSLA** | STOCK | 24.00 | $432.23 | $354.25 | $8,502.00 | 🔴 $-1,871.57 | -18.04% |
| **VTI** | ETF | 28.00 | $370.04 | $380.91 | $10,665.48 | 🟢 +$304.28 | +2.94% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $229.06 | 🟢 +9.20% | **SELL** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $315.28 | 🟢 +0.58% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $341.15 | 🔴 -0.27% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $503.75 | 🟢 +1.49% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $255.90 | 🔴 -1.67% | **BUY** | 96% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $381.01 | 🟢 +0.73% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $368.78 | 🟢 +3.72% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $80,762.26 | 🟢 +2.20% | HOLD | — |
| 9 | **META** | Meta Platforms Inc. | STOCK | $571.06 | 🔴 -0.90% | **BUY** | 83% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,187.33 | 🔴 -0.17% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 78% | Extreme gain today (+9.20%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.58%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.27%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.49%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-1.67%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.73%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 74% | Extreme gain today (+3.72%) — mean reversion pullback likely |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+2.20%) — continuation expected |
| 9 | **META** | Meta Platforms Inc. | **SELL** | 73% | Moderate negative momentum (-0.90%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.17%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
