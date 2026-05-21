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

> 🕐 **Last updated:** 2026-05-21 14:42 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,868.90` |
| 💸 Cash Available    | `$49,098.75` |
| 🧾 Buying Power      | `$140,834.60` |
| 🔴 Total P&L | `$-1,352.79` &nbsp; `(-13.53%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,352.79` (-13.53%)
- **Yesterday-to-today P&L:** `$-425.41`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | SELL | 96% | Negative momentum detected |
| **TSLA** | SELL | 75% | Negative momentum detected |
| **MSFT** | SELL | 81% | Negative momentum detected |
| **AMZN** | SELL | 70% | Negative momentum detected |
| **BTC/USD** | SELL | 74% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 8.0000 | $299.74 | $302.01 | $2,416.08 | 🟢 +$18.14 | +0.76% |
| **AMZN** | STOCK | 10.00 | $262.76 | $263.68 | $2,636.80 | 🟢 +$9.15 | +0.35% |
| **BTC/USD** | CRYPTO | 0.0372 | $78,714.67 | $77,066.60 | $2,867.67 | 🔴 $-61.33 | -2.09% |
| **ETH/USD** | CRYPTO | 1.3536 | $2,211.56 | $2,123.44 | $2,874.31 | 🔴 $-119.28 | -3.98% |
| **MSFT** | STOCK | 3.0000 | $423.70 | $416.77 | $1,250.30 | 🔴 $-20.81 | -1.64% |
| **NVDA** | STOCK | 141.00 | $226.71 | $219.14 | $30,898.73 | 🔴 $-1,067.15 | -3.34% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $86.26 | $1,391.08 | 🔴 $-107.49 | -7.17% |
| **SPY** | ETF | 4.0000 | $737.94 | $738.18 | $2,952.72 | 🟢 +$0.95 | +0.03% |
| **TSLA** | STOCK | 3.0000 | $415.47 | $413.81 | $1,241.43 | 🔴 $-4.97 | -0.40% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $302.00 | 🔴 -0.08% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $219.44 | 🔴 -1.80% | **SELL** | 96% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $414.07 | 🔴 -0.76% | **SELL** | 75% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $416.70 | 🔴 -1.04% | **SELL** | 81% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $263.63 | 🔴 -0.52% | **SELL** | 70% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $597.13 | 🔴 -1.31% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $738.34 | 🔴 -0.39% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $76,911.89 | 🔴 -0.71% | **SELL** | 74% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,117.53 | 🔴 -0.47% | **SELL** | 69% |
| 10 | **SOL/USD** | Solana | CRYPTO | $86.09 | 🟢 +0.02% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.08%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-1.80%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **SELL** | 66% | Moderate negative momentum (-0.76%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 71% | Moderate negative momentum (-1.04%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 62% | Moderate negative momentum (-0.52%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 76% | Moderate negative momentum (-1.31%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 65% | Moderate negative momentum (-0.71%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 61% | Moderate negative momentum (-0.47%) — continuation expected |
| 10 | **SOL/USD** | Solana | HOLD | 50% | Flat session today (+0.02%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
