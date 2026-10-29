# AI-Alpaca-Day-Trading-Paper-Bot

AI-powered Alpaca **paper-trading** bot using Python, risk management, structured AI decisions, and automated trade analytics.

**$100 configured paper portfolio (mirrors the live bot's strategy capital) · 10 symbols · fail-closed safety checks · GitHub Actions trade/report schedules**

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
| Portfolio budget | `PORTFOLIO_SIZE=100` — matches the live bot's dynamic strategy capital (50% of its $200 live account) |
| Max position size | `MAX_POSITION_PERCENT=10` (default $10 per symbol) |
| Max total gross exposure | `MAX_TOTAL_EXPOSURE_PERCENT=80` (default $80) |
| Fractional equity sizing | `FRACTIONAL_EQUITY_THRESHOLD=20000`: stock/ETF BUYs may be sized in fractional shares while account equity is below this and Alpaca marks the asset fractionable |
| Fractional DAY-stop cleanup | `FRACTIONAL_EOD_WINDOW_MINUTES=30`: the scheduled `eod` run market-sells every fractional stock/ETF position inside this pre-close window, and new fractional BUYs are refused inside it |
| Daily trade cap | `MAX_DAILY_TRADES=3` across the whole bot |
| Per-symbol trade cap | Max 1 executed trade per symbol per trading day |
| Daily loss circuit breaker | `MAX_DAILY_LOSS_PERCENT=2` blocks new BUYs after the threshold is hit |
| Margin | `ALLOW_MARGIN=false` |
| Shorts | `ALLOW_SHORTS=false` |
| Protective stop policy | New long stock/ETF BUYs must have broker-side stop protection or the entry is rejected: `GTC` for whole-share entries, `DAY` for fractional entries (Alpaca's only option) |
| Crypto BUY safety | Rejected whenever reliable broker-side protective stops cannot be guaranteed |
| Market-data safety | Fallback/demo prices are **never** eligible for paper-order execution |
| Scheduled automation idempotency | Scheduled trade/report runs persist once-per-Eastern-trading-day markers |
| Logging | Every decision is logged, including execution status, protection state, order IDs, and rejection reasons |

### Default Safety Configuration

These values live in `config/watchlist.json` and can be overridden in `.env`:

```dotenv
PORTFOLIO_SIZE=100
MAX_POSITION_PERCENT=10
MAX_DAILY_LOSS_PERCENT=2
MAX_DAILY_TRADES=3
MAX_TOTAL_EXPOSURE_PERCENT=80
ALLOW_MARGIN=false
ALLOW_SHORTS=false
MIN_CONFIDENCE=0.70
MAX_RISK_PERCENT=1
FRACTIONAL_EQUITY_THRESHOLD=20000
FRACTIONAL_EOD_WINDOW_MINUTES=30
```

### Fractional Equity Policy

- New **stock/ETF BUY** sizing may use Alpaca-supported fractional quantities (4 decimal places) only when account equity is below `FRACTIONAL_EQUITY_THRESHOLD` (default `$20,000`) **and** Alpaca reports the asset as fractionable.
- This is what lets a small budget trade at all: with `PORTFOLIO_SIZE=100` the per-symbol cap is `$10`, so a `$347` stock is sized to `0.0288` shares instead of being floored to zero.
- At or above the threshold, new equity BUY quantities are floored to whole shares exactly as before. Crypto precision is unaffected by this policy.
- Existing fractional positions remain eligible for **SELL-to-close** handling regardless of the threshold.
- If the broker asset lookup fails, the asset is treated as **not fractionable** and a fractional BUY is rejected (fail closed).

### Protective Stop Behavior

- For new long whole-share **stock/ETF BUY** orders, the bot submits broker-side protection through Alpaca-supported attached stop logic using **`GTC`** protection so the stop can persist beyond the current session.
- Alpaca only accepts fractional equity orders as simple **`DAY`** market orders, so a fractional BUY is placed as a DAY market entry followed by a standalone **`DAY`** stop sized to the verified fill. The entry is given a bounded fill window, any unfilled remainder is cancelled before the stop is sized, and the stop is confirmed with bounded broker polling. That DAY stop **expires at the close**, so fractional positions are never held overnight: the scheduled end-of-day cleanup below exits them first.
- A fractional BUY is **refused inside the pre-close window** (`FRACTIONAL_EOD_WINDOW_MINUTES`, default 30), when the exchange is closed, or when Alpaca's market clock cannot be read, because no later cleanup run would exist to exit its expiring DAY stop.
- If a fractional request happens to fill to a **whole-share** quantity before its remainder is cancelled, that fill gets a normal **`GTC`** stop instead of a DAY stop, so it never depends on the cleanup. A fractional entry whose cancellation cannot be confirmed is treated as a counted trade that reserves its full cash, exposure and daily-trade slot, because it may still fill.
- Attached OTO protection is only treated as active after bounded polling confirms an actual stop child with a valid child order ID, stop price, side, and quantity.
- If the bot cannot reliably create that protective stop, it **rejects the BUY** instead of placing an unprotected entry.
- If an entry is accepted/executed but protection confirmation fails, the run records a **critical protection failure** and does not treat the trade as safely protected.
- Normal long **SELL-to-close** orders do not create a new entry-style stop.

### End-of-Day Fractional Cleanup (`--mode eod`)

- A fourth scheduled run (`python -m src.main --mode eod --scheduled-run`, 3:40 PM America/New_York, plus a 12:40 PM run that only acts on early-close days) **market-sells every long fractional stock/ETF position** before its DAY protective stop expires at the close. Whole-share positions keep their GTC stops and crypto is untouched.
- The run consults **Alpaca's market clock**, never the runner's wall clock: before the pre-close window it is a no-op (so the 12:40 run skips on a normal day and writes no once-per-day marker); when the session is already closed or the clock is unusable it refuses to sell, records the failure, and fails the job.
- The once-per-day marker is written **only when every fractional position was resolved**, so a failed scheduled cleanup can be re-run (re-run the job or dispatch `eod` manually) while the exchange is still open.
- Candidates are chosen by the broker's own asset class first (crypto is skipped even for unlisted symbols such as `DOGEUSD`), then the watchlist type, then the symbol. A fractional quantity always qualifies; a whole-share holding qualifies when any of its open protective stops is a DAY order (a fractional top-up can turn 0.65 + 0.35 into an integer holding that still carries DAY protection). A holding whose stops cannot be listed is a failure, never a silent exclusion.
- For each position it **cancels and verifies the DAY stop first**, submits a DAY market SELL, gives it a bounded fill window, and if it has not filled, cancels it and confirms a terminal broker state **before** any protection is restored. A SELL whose state stays ambiguous is reported as a critical unprotected position and never has a stop stacked on top of it.
- Every BUY and SELL carries a client order ID. If the submission call raises (for example a response timeout) the bot looks the order up by that ID: an accepted order is recovered and handled normally (a BUY goes on to get its stop, a SELL is reconciled); a confirmed "not found" is a plain error (and restores the original stop for a SELL); an unreliable lookup fails closed, as a counted ambiguous entry for a BUY or with no stop added for a SELL.
- Position discovery is strict: a broker listing error raises instead of reading as "no positions".
- A residual quantity after a partial fill is re-protected with a fresh DAY stop but still reported as a failure, because that stop expires at the close too.
- Exits are written to the trade log, the daily summary (`EOD Cleanup Exits`) and the dashboard; they are safety exits and are not subject to `MAX_DAILY_TRADES`. Any failure is persisted in `portfolio_state.json`, surfaces as a safety warning on the same day's 4:15 PM report, and fails the GitHub Actions job so it is visible. The next day's cleanup sweeps any fractional position that was left behind.

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

- Example: if `PORTFOLIO_SIZE=100` and Alpaca paper equity is `$108,000`, a `1%` max-risk policy still limits allowed trade risk to `$1`.
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
      - scheduled pre-close run: `python -m src.main --mode eod --scheduled-run` (fractional DAY-stop cleanup)
      - scheduled afternoon run: `python -m src.main --mode report --scheduled-run`
     - manual runs require an explicit mode choice and default to `report`
     - every bot run forces `ALPACA_PAPER=true`
      - state-mutating bot runs are serialized with GitHub Actions concurrency (`alpaca-paper-trading-bot`)
      - state commit steps still run after bot-step failures, so email issues cannot prevent execution-state commits
      - native GitHub schedule timezone is `America/New_York`
      - scheduled trade/eod/report runs use persisted once-per-trading-day markers so accidental reruns become no-ops

> The scheduled workflow runs at **10:15 AM America/New_York** for trade mode, **3:40 PM** (and **12:40 PM** for early-close days) for the fractional EOD cleanup, and **4:15 PM America/New_York** for report mode through both EST and EDT using native GitHub timezone scheduling.

## 🚀 Local Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env          # then fill in your keys
python -m pytest -q                  # run tests
python -m src.main --mode report     # safe default: reporting/dashboard only
python -m src.main --mode trade      # paper-trading run with risk checks and broker orders
python -m src.main --mode eod        # pre-close cleanup: sells fractional stock/ETF positions before their DAY stops expire
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

> 🕐 **Last updated:** 2026-10-29 20:23 UTC &nbsp;|&nbsp; **Trades today:** 0 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🧭 Configured Strategy Budget | `$100.00` |
| 🛡️ Strategy Max Gross Exposure | `$80.00` |
| 💵 Alpaca Paper Account Equity | `$199.51` |
| 💸 Broker Cash Available | `$199.51` |
| 🧾 Broker Buying Power | `$199.51` |
| 📦 Actual Broker Gross Exposure | `$0.00` |
| ⚪ Broker Position P&L | `$0.00` &nbsp; `(0.00%)` |
| 📆 Daily P&L (final equity - start of day) | `$0.00` |

### 📝 Daily Trade Summary

- **Broker position P&L:** `$0.00` (0.00%)
- **Daily P&L:** `$0.00`
- **Executed today:** No buy/sell orders were approved in this run.

### 📈 Open Positions

*No open positions.*

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $210.92 | 🔴 -2.05% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $348.98 | 🟢 +1.43% | HOLD | — |
| 3 | **MSFT** | Microsoft Corp. | STOCK | $530.39 | 🔴 -0.35% | HOLD | — |
| 4 | **GOOGL** | Alphabet Inc. | STOCK | $282.53 | 🔴 -13.17% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $230.90 | 🔴 -9.34% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $378.31 | 🔴 -0.23% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $339.51 | 🔴 -3.52% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $80,261.90 | 🔴 -1.22% | HOLD | — |
| 9 | **META** | Meta Platforms Inc. | STOCK | $619.04 | 🟢 +1.05% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,373.46 | 🟢 +6.41% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 48% | Moderate negative momentum (-2.05%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.43%) — continuation expected |
| 3 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.35%) — no trend to carry forward |
| 4 | **GOOGL** | Alphabet Inc. | **BUY** | 78% | Extreme loss today (-13.17%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 78% | Extreme loss today (-9.34%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.23%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 73% | Extreme loss today (-3.52%) — mean reversion pullback likely |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 48% | Moderate negative momentum (-1.22%) — continuation expected |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.05%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 78% | Extreme gain today (+6.41%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
