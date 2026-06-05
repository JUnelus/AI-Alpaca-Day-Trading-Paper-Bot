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

> 🕐 **Last updated:** 2026-06-05 21:44 UTC &nbsp;|&nbsp; **Trades today:** 9 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,402.59` |
| 💸 Cash Available    | `$31,899.69` |
| 🧾 Buying Power      | `$277,188.00` |
| 🔴 Total P&L | `$-4,542.28` &nbsp; `(-45.42%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-4,542.28` (-45.42%)
- **Yesterday-to-today P&L:** `$-2,668.73`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AAPL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **VTI** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 44.00 | $311.29 | $307.87 | $13,546.28 | 🔴 $-150.61 | -1.10% |
| **AMZN** | STOCK | 4.0000 | $252.71 | $246.30 | $985.20 | 🔴 $-25.63 | -2.54% |
| **AVGO** | STOCK | 4.0000 | $407.01 | $387.00 | $1,548.00 | 🔴 $-80.06 | -4.92% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,959.02 | $61,781.73 | $1,578.50 | 🔴 $-311.12 | -16.46% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,611.02 | $1,010.49 | 🔴 $-320.70 | -24.09% |
| **GOOGL** | STOCK | 2.0000 | $366.23 | $366.30 | $732.60 | 🟢 +$0.15 | +0.02% |
| **META** | STOCK | 7.0000 | $618.04 | $591.49 | $4,140.43 | 🔴 $-185.87 | -4.30% |
| **MSFT** | STOCK | 7.0000 | $451.41 | $415.10 | $2,905.70 | 🔴 $-254.19 | -8.04% |
| **NVDA** | STOCK | 92.00 | $225.53 | $205.40 | $18,896.80 | 🔴 $-1,851.56 | -8.92% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $65.03 | $1,002.68 | 🔴 $-325.70 | -24.52% |
| **SPY** | STOCK | 6.0000 | $745.44 | $735.35 | $4,412.10 | 🔴 $-60.56 | -1.35% |
| **TSLA** | STOCK | 24.00 | $432.23 | $392.15 | $9,411.59 | 🔴 $-961.98 | -9.27% |
| **VTI** | ETF | 2.0000 | $370.14 | $362.92 | $725.84 | 🔴 $-14.44 | -1.95% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $205.10 | 🔴 -6.20% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $307.34 | 🔴 -1.25% | **BUY** | 85% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $368.53 | 🔴 -0.98% | **BUY** | 84% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $416.67 | 🔴 -2.66% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $246.03 | 🔴 -3.06% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $363.38 | 🔴 -2.68% | **BUY** | 100% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $385.73 | 🔴 -7.92% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $593.00 | 🔴 -5.51% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,866.31 | 🔴 -3.04% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,131.42 | 🟢 +0.55% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 78% | Extreme loss today (-6.20%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.25%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 74% | Moderate negative momentum (-0.98%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 68% | Extreme loss today (-2.66%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 70% | Extreme loss today (-3.06%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 68% | Extreme loss today (-2.68%) — mean reversion pullback likely |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 78% | Extreme loss today (-7.92%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 78% | Extreme loss today (-5.51%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 70% | Extreme loss today (-3.04%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.55%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
