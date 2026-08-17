# AI-Alpaca-Day-Trading-Paper-Bot

AI-powered day trading paper bot using Alpaca API, Python, risk management, and automated trade analytics.

**$10,000 paper portfolio · 10 symbols (stocks + crypto) · fully automated · GitHub Actions daily schedule**

---

## 🏗️ Architecture

```
Market Data → Strategy Rules → AI Agent Decision → Risk Manager → Alpaca Paper Trade → Trade Log / Dashboard
```

The AI agent returns **structured decisions only** — it never places orders directly.

## 📁 Project Structure

```text
ai-alpaca-day-trading-paper-bot/
├── .github/workflows/daily_trade.yml   ← GitHub Actions (9:45 AM & 4:15 PM ET)
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

## 🛡️ Risk Rules

| Rule                       | Policy                                     |
|:---------------------------|:-------------------------------------------|
| Trading mode               | Paper only                                 |
| Max symbols                | 10                                         |
| Watchlist refresh          | Weekly top-10 by market value             |
| Entry style                | DCA on dips for quality assets            |
| Max trades per symbol/day  | 1                                          |
| Max account risk per trade | 1 %                                        |
| Min AI confidence          | 70 %                                       |
| Margin                     | ❌ Not permitted                            |
| Stop loss                  | Required on every trade                    |
| Logging                    | Every decision (approved **and** rejected) |

## ⚙️ GitHub Actions Setup

1. Go to **Settings → Secrets and variables → Actions** in your repo.
2. Add two repository secrets:
   - `ALPACA_API_KEY`
   - `ALPACA_SECRET_KEY`
3. The workflow at `.github/workflows/daily_trade.yml` runs automatically:
   - **9:45 AM ET** Mon–Fri — place day orders
   - **4:15 PM ET** Mon–Fri — update portfolio and dashboard

## 🚀 Local Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env          # then fill in your keys
python -m pytest -q                  # run tests
python -m src.main                   # run one full cycle
```

---

<!-- PORTFOLIO_DASHBOARD_START -->

## 📊 Live Portfolio Dashboard

> 🕐 **Last updated:** 2026-08-17 21:22 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$103,357.42` |
| 💸 Cash Available    | `$-102,577.02` |
| 🧾 Buying Power      | `$94,917.05` |
| 🟢 Total P&L | `+$17,153.20` &nbsp; `(+171.53%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$17,153.20` (+171.53%)
- **Yesterday-to-today P&L:** `$-780.10`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $305.22 | $20,449.74 | 🔴 $-149.59 | -0.73% |
| **AMZN** | STOCK | 45.00 | $246.48 | $261.32 | $11,759.40 | 🟢 +$667.88 | +6.02% |
| **AVGO** | STOCK | 14.00 | $389.31 | $392.47 | $5,494.55 | 🟢 +$44.27 | +0.81% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $64,354.84 | $19,975.42 | 🟢 +$12,631.55 | +172.00% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,907.67 | $1,196.57 | 🟢 +$1,196.57 | 0.00% |
| **GOOGL** | STOCK | 26.00 | $353.36 | $343.65 | $8,934.90 | 🔴 $-252.44 | -2.75% |
| **LLY** | STOCK | 41.00 | $1,168.10 | $1,183.50 | $48,523.50 | 🟢 +$631.32 | +1.32% |
| **META** | STOCK | 30.00 | $595.67 | $569.02 | $17,070.55 | 🔴 $-799.50 | -4.47% |
| **MSFT** | STOCK | 29.00 | $409.80 | $480.39 | $13,931.31 | 🟢 +$2,047.01 | +17.22% |
| **NVDA** | STOCK | 161.00 | $214.48 | $224.97 | $36,220.12 | 🟢 +$1,688.78 | +4.89% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.04 | $1,172.49 | 🟢 +$1,172.49 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $772.67 | $4,636.02 | 🟢 +$163.36 | +3.65% |
| **TSLA** | STOCK | 24.00 | $432.23 | $340.03 | $8,160.80 | 🔴 $-2,212.77 | -21.33% |
| **VTI** | ETF | 22.00 | $367.49 | $382.23 | $8,409.06 | 🟢 +$324.27 | +4.01% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $225.01 | 🔴 -0.07% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $305.59 | 🔴 -0.11% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $344.00 | 🔴 -0.55% | **BUY** | 77% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $480.35 | 🔴 -3.04% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $261.31 | 🔴 -0.51% | **BUY** | 76% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $382.13 | 🔴 -0.45% | **BUY** | 75% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $392.43 | 🔴 -0.14% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $568.97 | 🔴 -3.54% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,327.42 | 🟢 +2.35% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,183.16 | 🟢 +0.25% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.07%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.11%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 68% | Moderate negative momentum (-0.55%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 70% | Extreme loss today (-3.04%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 67% | Moderate negative momentum (-0.51%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 66% | Moderate negative momentum (-0.45%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (-0.14%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 73% | Extreme loss today (-3.54%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+2.35%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.25%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
