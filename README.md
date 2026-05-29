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

> 🕐 **Last updated:** 2026-05-29 14:42 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,140.87` |
| 💸 Cash Available    | `$33,788.40` |
| 🧾 Buying Power      | `$126,842.33` |
| 🔴 Total P&L | `$-1,102.56` &nbsp; `(-11.03%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,102.56` (-11.03%)
- **Yesterday-to-today P&L:** `$-318.76`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **TSLA** | SELL | 100% | Negative momentum detected |
| **MSFT** | BUY | 100% | Positive momentum detected |
| **AMZN** | SELL | 79% | Negative momentum detected |
| **META** | SELL | 93% | Negative momentum detected |
| **BTC/USD** | SELL | 85% | Negative momentum detected |
| **ETH/USD** | SELL | 81% | Negative momentum detected |
| **SOL/USD** | SELL | 92% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $308.65 | $313.29 | $16,290.82 | 🟢 +$241.10 | +1.50% |
| **AMZN** | STOCK | 10.00 | $271.92 | $271.11 | $2,711.10 | 🔴 $-8.11 | -0.30% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $72,658.83 | $1,268.75 | 🔴 $-84.64 | -6.25% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $1,987.68 | $1,246.75 | 🔴 $-84.44 | -6.34% |
| **META** | STOCK | 2.0000 | $634.20 | $624.10 | $1,248.20 | 🔴 $-20.20 | -1.59% |
| **MSFT** | STOCK | 6.0000 | $432.00 | $442.63 | $2,655.81 | 🟢 +$63.84 | +2.46% |
| **NVDA** | STOCK | 97.00 | $225.99 | $214.68 | $20,823.98 | 🔴 $-1,097.45 | -5.01% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $80.64 | $1,243.37 | 🔴 $-85.01 | -6.40% |
| **SPY** | ETF | 7.0000 | $744.36 | $755.31 | $5,287.17 | 🟢 +$76.67 | +1.47% |
| **TSLA** | STOCK | 27.00 | $432.60 | $428.74 | $11,575.98 | 🔴 $-104.32 | -0.89% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $313.57 | 🟢 +0.34% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $215.00 | 🟢 +0.35% | HOLD | — |
| 3 | **TSLA** | Tesla Inc. | STOCK | $429.14 | 🔴 -2.93% | **SELL** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $443.19 | 🟢 +3.79% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $271.33 | 🔴 -0.97% | **SELL** | 79% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $624.96 | 🔴 -1.63% | **SELL** | 93% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $755.75 | 🟢 +0.15% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $72,604.45 | 🔴 -1.23% | **SELL** | 85% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $1,986.37 | 🔴 -1.03% | **SELL** | 81% |
| 10 | **SOL/USD** | Solana | CRYPTO | $80.71 | 🔴 -1.60% | **SELL** | 92% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.34%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.35%) — no trend to carry forward |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 70% | Extreme loss today (-2.93%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 74% | Extreme gain today (+3.79%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 70% | Moderate negative momentum (-0.97%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 81% | Moderate negative momentum (-1.63%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (+0.15%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 74% | Moderate negative momentum (-1.23%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 71% | Moderate negative momentum (-1.03%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 81% | Moderate negative momentum (-1.60%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
