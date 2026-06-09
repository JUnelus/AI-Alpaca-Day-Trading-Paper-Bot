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

> 🕐 **Last updated:** 2026-06-09 21:51 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,623.77` |
| 💸 Cash Available    | `$22,423.67` |
| 🧾 Buying Power      | `$261,112.45` |
| 🔴 Total P&L | `$-5,320.95` &nbsp; `(-53.21%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,320.95` (-53.21%)
- **Yesterday-to-today P&L:** `$-1,178.07`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 98% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 73% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 47.00 | $310.74 | $290.36 | $13,646.92 | 🔴 $-957.77 | -6.56% |
| **AMZN** | STOCK | 8.0000 | $250.24 | $243.34 | $1,946.72 | 🔴 $-55.22 | -2.76% |
| **AVGO** | STOCK | 6.0000 | $403.07 | $388.90 | $2,333.40 | 🔴 $-85.05 | -3.52% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $61,747.49 | $1,577.62 | 🔴 $-311.86 | -16.51% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,648.75 | $1,034.16 | 🔴 $-297.03 | -22.31% |
| **GOOGL** | STOCK | 5.0000 | $365.74 | $363.63 | $1,818.15 | 🔴 $-10.56 | -0.58% |
| **META** | STOCK | 10.00 | $609.51 | $586.00 | $5,860.00 | 🔴 $-235.11 | -3.86% |
| **MSFT** | STOCK | 11.00 | $437.01 | $402.95 | $4,432.40 | 🔴 $-374.75 | -7.80% |
| **NVDA** | STOCK | 96.00 | $224.81 | $206.90 | $19,862.40 | 🔴 $-1,718.92 | -7.96% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $65.08 | $1,003.38 | 🔴 $-325.00 | -24.47% |
| **SPY** | STOCK | 6.0000 | $745.44 | $735.50 | $4,413.00 | 🔴 $-59.66 | -1.33% |
| **TSLA** | STOCK | 24.00 | $432.23 | $395.90 | $9,501.62 | 🔴 $-871.95 | -8.41% |
| **VTI** | ETF | 3.0000 | $369.03 | $363.01 | $1,089.03 | 🔴 $-18.06 | -1.63% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.19 | 🔴 -0.22% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $364.26 | 🟢 +0.26% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $290.55 | 🔴 -3.64% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $403.41 | 🔴 -2.02% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $244.19 | 🔴 -0.42% | **BUY** | 75% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $363.67 | 🔴 -0.22% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $392.16 | 🔴 -1.12% | **BUY** | 85% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $584.59 | 🔴 -0.14% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,759.45 | 🔴 -2.06% | **BUY** | 98% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,144.68 | 🔴 -0.39% | **BUY** | 73% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.22%) — no trend to carry forward |
| 2 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.26%) — no trend to carry forward |
| 3 | **AAPL** | Apple Inc. | **BUY** | 73% | Extreme loss today (-3.64%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-2.02%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 66% | Moderate negative momentum (-0.42%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.22%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 75% | Moderate negative momentum (-1.12%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.14%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.06%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
