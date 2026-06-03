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

> 🕐 **Last updated:** 2026-06-03 22:09 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$97,055.65` |
| 💸 Cash Available    | `$36,304.04` |
| 🧾 Buying Power      | `$128,696.94` |
| 🔴 Total P&L | `$-1,947.95` &nbsp; `(-19.48%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,947.95` (-19.48%)
- **Yesterday-to-today P&L:** `$-1,136.44`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | SELL | 91% | Negative momentum detected |
| **NVDA** | SELL | 100% | Negative momentum detected |
| **MSFT** | SELL | 100% | Negative momentum detected |
| **META** | BUY | 100% | Positive momentum detected |
| **SPY** | SELL | 74% | Negative momentum detected |
| **BTC/USD** | SELL | 96% | Negative momentum detected |
| **ETH/USD** | SELL | 75% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $310.82 | $313.00 | $15,024.00 | 🟢 +$104.70 | +0.70% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $65,469.37 | $1,143.21 | 🔴 $-210.18 | -15.53% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $1,843.89 | $1,156.56 | 🔴 $-174.63 | -13.12% |
| **META** | STOCK | 4.0000 | $612.74 | $620.05 | $2,480.20 | 🟢 +$29.24 | +1.19% |
| **MSFT** | STOCK | 9.0000 | $450.97 | $428.38 | $3,855.42 | 🔴 $-203.34 | -5.01% |
| **NVDA** | STOCK | 96.00 | $225.77 | $214.28 | $20,571.22 | 🔴 $-1,102.29 | -5.09% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $72.80 | $1,122.48 | 🔴 $-205.90 | -15.50% |
| **SPY** | ETF | 7.0000 | $744.36 | $751.32 | $5,259.24 | 🟢 +$48.74 | +0.94% |
| **TSLA** | STOCK | 24.00 | $432.23 | $422.47 | $10,139.28 | 🔴 $-234.29 | -2.26% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $310.26 | 🔴 -1.57% | **SELL** | 91% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $214.75 | 🔴 -3.62% | **SELL** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $423.70 | 🔴 -0.01% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $427.34 | 🔴 -3.17% | **SELL** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $250.02 | 🔴 -2.53% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $622.98 | 🟢 +4.24% | **BUY** | 100% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $754.24 | 🔴 -0.70% | **SELL** | 74% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $65,435.11 | 🔴 -1.82% | **SELL** | 96% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $1,843.25 | 🔴 -0.74% | **SELL** | 75% |
| 10 | **SOL/USD** | Solana | CRYPTO | $72.68 | 🔴 -1.93% | **SELL** | 99% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 80% | Moderate negative momentum (-1.57%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 73% | Extreme loss today (-3.62%) — mean reversion pullback likely |
| 3 | **TSLA** | Tesla Inc. | HOLD | 50% | Flat session today (-0.01%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 71% | Extreme loss today (-3.17%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 68% | Extreme loss today (-2.53%) — mean reversion pullback likely |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 76% | Extreme gain today (+4.24%) — mean reversion pullback likely |
| 7 | **SPY** | SPDR S&P 500 ETF | **SELL** | 65% | Moderate negative momentum (-0.70%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-1.82%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 66% | Moderate negative momentum (-0.74%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 85% | Moderate negative momentum (-1.93%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
