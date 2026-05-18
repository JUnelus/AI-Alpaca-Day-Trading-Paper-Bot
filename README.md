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

> 🕐 **Last updated:** 2026-05-18 21:41 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,641.78` |
| 💸 Cash Available    | `$48,397.44` |
| 🧾 Buying Power      | `$143,888.00` |
| 🔴 Total P&L | `$-863.82` &nbsp; `(-8.64%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-863.82` (-8.64%)
- **Yesterday-to-today P&L:** `$-456.79`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | SELL | 76% | Negative momentum detected |
| **NVDA** | SELL | 87% | Negative momentum detected |
| **BTC/USD** | SELL | 71% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 4.0000 | $299.04 | $297.40 | $1,189.59 | 🔴 $-6.58 | -0.55% |
| **AMZN** | STOCK | 5.0000 | $267.77 | $264.65 | $1,323.25 | 🔴 $-15.59 | -1.16% |
| **BTC/USD** | CRYPTO | 0.0180 | $81,502.71 | $76,884.50 | $1,384.48 | 🔴 $-83.16 | -5.67% |
| **ETH/USD** | CRYPTO | 0.6510 | $2,299.70 | $2,137.29 | $1,391.31 | 🔴 $-105.72 | -7.06% |
| **MSFT** | STOCK | 12.00 | $414.36 | $423.06 | $5,076.72 | 🟢 +$104.37 | +2.10% |
| **NVDA** | STOCK | 164.00 | $226.63 | $222.90 | $36,555.60 | 🔴 $-611.61 | -1.65% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $85.29 | $1,375.44 | 🔴 $-123.14 | -8.22% |
| **SPY** | ETF | 4.0000 | $743.49 | $737.89 | $2,951.56 | 🔴 $-22.39 | -0.75% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $297.84 | 🔴 -0.80% | **SELL** | 76% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $222.32 | 🔴 -1.33% | **SELL** | 87% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $409.99 | 🔴 -2.90% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $423.54 | 🟢 +0.38% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $264.86 | 🟢 +0.27% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $611.21 | 🔴 -0.49% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $738.65 | 🔴 -0.07% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $76,960.61 | 🔴 -0.57% | **SELL** | 71% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,134.74 | 🟢 +0.20% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $85.37 | 🟢 +0.27% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 67% | Moderate negative momentum (-0.80%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 76% | Moderate negative momentum (-1.33%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 70% | Extreme loss today (-2.90%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.38%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.27%) — no trend to carry forward |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 61% | Moderate negative momentum (-0.49%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (-0.07%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 63% | Moderate negative momentum (-0.57%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | HOLD | 50% | Flat session today (+0.20%) — no trend to carry forward |
| 10 | **SOL/USD** | Solana | HOLD | 50% | Flat session today (+0.27%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
