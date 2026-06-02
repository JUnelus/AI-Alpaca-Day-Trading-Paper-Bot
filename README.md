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

> 🕐 **Last updated:** 2026-06-02 15:06 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,693.91` |
| 💸 Cash Available    | `$37,523.15` |
| 🧾 Buying Power      | `$128,678.61` |
| 🔴 Total P&L | `$-405.68` &nbsp; `(-4.06%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-405.68` (-4.06%)
- **Yesterday-to-today P&L:** `+$244.78`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 92% | Positive momentum detected |
| **NVDA** | BUY | 80% | Positive momentum detected |
| **TSLA** | BUY | 93% | Positive momentum detected |
| **MSFT** | SELL | 100% | Negative momentum detected |
| **META** | BUY | 82% | Positive momentum detected |
| **BTC/USD** | SELL | 100% | Negative momentum detected |
| **ETH/USD** | SELL | 100% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 44.00 | $309.52 | $311.29 | $13,696.76 | 🟢 +$77.68 | +0.57% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $67,876.70 | $1,185.25 | 🔴 $-168.14 | -12.42% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $1,932.60 | $1,212.20 | 🔴 $-118.99 | -8.94% |
| **MSFT** | STOCK | 18.00 | $446.68 | $443.49 | $7,982.87 | 🔴 $-57.29 | -0.71% |
| **NVDA** | STOCK | 107.00 | $225.76 | $226.62 | $24,248.88 | 🟢 +$92.82 | +0.38% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $76.83 | $1,184.62 | 🔴 $-143.76 | -10.82% |
| **SPY** | ETF | 7.0000 | $744.36 | $759.70 | $5,317.90 | 🟢 +$107.40 | +2.06% |
| **TSLA** | STOCK | 15.00 | $435.87 | $422.84 | $6,342.60 | 🔴 $-195.40 | -2.99% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $311.14 | 🟢 +1.58% | **BUY** | 92% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $226.56 | 🟢 +0.98% | **BUY** | 80% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $422.79 | 🟢 +1.66% | **BUY** | 93% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $443.64 | 🔴 -3.67% | **SELL** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $260.31 | 🔴 -0.36% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $607.16 | 🟢 +1.11% | **BUY** | 82% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $759.61 | 🟢 +0.14% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $67,845.55 | 🔴 -4.86% | **SELL** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $1,931.89 | 🔴 -3.59% | **SELL** | 100% |
| 10 | **SOL/USD** | Solana | CRYPTO | $77.00 | 🔴 -5.12% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 81% | Moderate positive momentum (+1.58%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 70% | Moderate positive momentum (+0.98%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 82% | Moderate positive momentum (+1.66%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 73% | Extreme loss today (-3.67%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.36%) — no trend to carry forward |
| 6 | **META** | Meta Platforms Inc. | **BUY** | 72% | Moderate positive momentum (+1.11%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (+0.14%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 78% | Extreme loss today (-4.86%) — mean reversion pullback likely |
| 9 | **ETH/USD** | Ethereum | **BUY** | 73% | Extreme loss today (-3.59%) — mean reversion pullback likely |
| 10 | **SOL/USD** | Solana | **BUY** | 78% | Extreme loss today (-5.12%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
