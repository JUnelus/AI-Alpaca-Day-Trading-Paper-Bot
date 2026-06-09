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

> 🕐 **Last updated:** 2026-06-09 14:40 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,392.02` |
| 💸 Cash Available    | `$24,470.64` |
| 🧾 Buying Power      | `$268,251.00` |
| 🔴 Total P&L | `$-4,552.16` &nbsp; `(-45.52%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-4,552.16` (-45.52%)
- **Yesterday-to-today P&L:** `$-409.28`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 80% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 78% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 46.00 | $311.11 | $293.60 | $13,505.60 | 🔴 $-805.47 | -5.63% |
| **AMZN** | STOCK | 8.0000 | $250.24 | $246.78 | $1,974.24 | 🔴 $-27.70 | -1.38% |
| **AVGO** | STOCK | 5.0000 | $405.01 | $393.29 | $1,966.42 | 🔴 $-58.62 | -2.89% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $61,397.30 | $1,568.68 | 🔴 $-320.81 | -16.98% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,635.47 | $1,025.83 | 🔴 $-305.36 | -22.94% |
| **GOOGL** | STOCK | 5.0000 | $365.74 | $367.16 | $1,835.80 | 🟢 +$7.09 | +0.39% |
| **META** | STOCK | 10.00 | $609.51 | $596.00 | $5,959.95 | 🔴 $-135.16 | -2.22% |
| **MSFT** | STOCK | 10.00 | $439.77 | $409.40 | $4,093.99 | 🔴 $-303.75 | -6.91% |
| **NVDA** | STOCK | 94.00 | $225.17 | $207.51 | $19,505.94 | 🔴 $-1,660.36 | -7.84% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $64.55 | $995.30 | 🔴 $-333.08 | -25.07% |
| **SPY** | STOCK | 6.0000 | $745.44 | $741.14 | $4,446.87 | 🔴 $-25.79 | -0.58% |
| **TSLA** | STOCK | 24.00 | $432.23 | $408.35 | $9,800.40 | 🔴 $-573.17 | -5.53% |
| **VTI** | ETF | 3.0000 | $369.03 | $365.71 | $1,097.13 | 🔴 $-9.96 | -0.90% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $207.12 | 🔴 -0.73% | **BUY** | 80% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $367.39 | 🟢 +1.12% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $293.36 | 🔴 -2.71% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $409.37 | 🔴 -0.58% | **BUY** | 78% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $246.92 | 🟢 +0.69% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.64 | 🟢 +0.32% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $392.60 | 🔴 -1.01% | **BUY** | 84% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $596.02 | 🟢 +1.82% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,381.82 | 🔴 -2.66% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,157.00 | 🟢 +0.68% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 70% | Moderate negative momentum (-0.73%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.12%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 69% | Extreme loss today (-2.71%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 69% | Moderate negative momentum (-0.58%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.69%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.32%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 74% | Moderate negative momentum (-1.01%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.82%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 68% | Extreme loss today (-2.66%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.68%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
