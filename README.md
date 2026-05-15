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

> 🕐 **Last updated:** 2026-05-15 14:34 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$100,514.00` |
| 💸 Cash Available    | `$45,209.31` |
| 🧾 Buying Power      | `$138,660.23` |
| 🔴 Total P&L | `$-32.33` &nbsp; `(-0.32%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-32.33` (-0.32%)
- **Yesterday-to-today P&L:** `$-1,719.68`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 70% | Positive momentum detected |
| **NVDA** | SELL | 100% | Negative momentum detected |
| **MSFT** | BUY | 100% | Positive momentum detected |
| **META** | SELL | 78% | Negative momentum detected |
| **SPY** | SELL | 78% | Negative momentum detected |
| **BTC/USD** | SELL | 100% | Negative momentum detected |
| **ETH/USD** | SELL | 100% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **BTC/USD** | CRYPTO | 0.0180 | $80,844.19 | $79,065.10 | $1,423.75 | 🔴 $-32.04 | -2.20% |
| **ETH/USD** | CRYPTO | 0.6510 | $2,299.70 | $2,210.62 | $1,439.05 | 🔴 $-57.99 | -3.87% |
| **META** | STOCK | 2.0000 | $620.18 | $612.86 | $1,225.72 | 🔴 $-14.64 | -1.18% |
| **MSFT** | STOCK | 6.0000 | $409.19 | $420.10 | $2,520.57 | 🟢 +$65.40 | +2.66% |
| **NVDA** | STOCK | 182.00 | $226.59 | $227.05 | $41,323.10 | 🟢 +$83.86 | +0.20% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $89.34 | $1,440.75 | 🔴 $-57.83 | -3.86% |
| **SPY** | ETF | 8.0000 | $743.86 | $741.47 | $5,931.76 | 🔴 $-19.10 | -0.32% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $299.75 | 🟢 +0.52% | **BUY** | 70% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $227.09 | 🔴 -3.67% | **SELL** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $427.26 | 🔴 -3.62% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $420.18 | 🟢 +2.63% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $263.08 | 🔴 -1.55% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $612.86 | 🔴 -0.90% | **SELL** | 78% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $741.47 | 🔴 -0.90% | **SELL** | 78% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $79,028.87 | 🔴 -2.53% | **SELL** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,210.64 | 🔴 -3.15% | **SELL** | 100% |
| 10 | **SOL/USD** | Solana | CRYPTO | $89.00 | 🔴 -3.42% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 62% | Moderate positive momentum (+0.52%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 73% | Extreme loss today (-3.67%) — mean reversion pullback likely |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 73% | Extreme loss today (-3.62%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 68% | Extreme gain today (+2.63%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 80% | Moderate negative momentum (-1.55%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 69% | Moderate negative momentum (-0.90%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | **SELL** | 69% | Moderate negative momentum (-0.90%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 68% | Extreme loss today (-2.53%) — mean reversion pullback likely |
| 9 | **ETH/USD** | Ethereum | **BUY** | 71% | Extreme loss today (-3.15%) — mean reversion pullback likely |
| 10 | **SOL/USD** | Solana | **BUY** | 72% | Extreme loss today (-3.42%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
