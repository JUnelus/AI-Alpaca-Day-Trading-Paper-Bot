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

> 🕐 **Last updated:** 2026-07-03 21:38 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,564.45` |
| 💸 Cash Available    | `$-29,774.81` |
| 🧾 Buying Power      | `$178,508.15` |
| 🔴 Total P&L | `$-3,139.79` &nbsp; `(-31.40%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-3,139.79` (-31.40%)
- **Yesterday-to-today P&L:** `+$443.93`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AAPL** | SELL | 100% | Take-profit trim after overextended rally |
| **GOOGL** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $305.99 | $308.63 | $18,517.80 | 🟢 +$158.34 | +0.86% |
| **AMZN** | STOCK | 28.00 | $237.74 | $242.67 | $6,794.76 | 🟢 +$138.12 | +2.07% |
| **AVGO** | STOCK | 11.00 | $378.26 | $360.45 | $3,964.95 | 🔴 $-195.90 | -4.71% |
| **BTC/USD** | CRYPTO | 0.1947 | $63,955.48 | $62,471.48 | $12,162.26 | 🔴 $-288.91 | -2.32% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,761.72 | $1,105.02 | 🔴 $-226.17 | -16.99% |
| **GOOGL** | STOCK | 13.00 | $350.09 | $359.91 | $4,678.83 | 🟢 +$127.72 | +2.81% |
| **LLY** | STOCK | 14.00 | $1,143.08 | $1,213.91 | $16,994.74 | 🟢 +$991.64 | +6.20% |
| **META** | STOCK | 15.00 | $567.68 | $582.90 | $8,743.50 | 🟢 +$228.36 | +2.68% |
| **MSFT** | STOCK | 22.00 | $393.63 | $390.49 | $8,590.78 | 🔴 $-69.13 | -0.80% |
| **NVDA** | STOCK | 126.00 | $218.95 | $194.83 | $24,548.58 | 🔴 $-3,039.34 | -11.02% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $82.38 | $1,270.20 | 🔴 $-58.18 | -4.38% |
| **SPY** | STOCK | 6.0000 | $745.44 | $744.78 | $4,468.68 | 🔴 $-3.98 | -0.09% |
| **TSLA** | STOCK | 24.00 | $432.23 | $393.45 | $9,442.80 | 🔴 $-930.77 | -8.97% |
| **VTI** | ETF | 11.00 | $366.18 | $368.76 | $4,056.36 | 🟢 +$28.40 | +0.71% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $194.83 | 🔴 -1.39% | **BUY** | 85% |
| 2 | **AAPL** | Apple Inc. | STOCK | $308.63 | 🟢 +4.84% | **SELL** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $359.91 | 🔴 -0.36% | **BUY** | 74% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $390.49 | 🟢 +1.62% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $242.67 | 🟢 +0.40% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.76 | 🔴 -0.14% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $360.45 | 🔴 -2.41% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $582.90 | 🔴 -4.90% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,525.65 | 🟢 +1.68% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,213.91 | 🟢 +1.86% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Moderate negative momentum (-1.39%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 78% | Extreme gain today (+4.84%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.36%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.62%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.40%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.14%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 85% | Moderate negative momentum (-2.41%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 78% | Extreme loss today (-4.90%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.68%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.86%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
