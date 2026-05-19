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

> 🕐 **Last updated:** 2026-05-19 21:45 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,293.08` |
| 💸 Cash Available    | `$53,798.93` |
| 🧾 Buying Power      | `$148,969.64` |
| 🔴 Total P&L | `$-1,080.66` &nbsp; `(-10.81%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,080.66` (-10.81%)
- **Yesterday-to-today P&L:** `$-216.84`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | SELL | 75% | Negative momentum detected |
| **MSFT** | SELL | 89% | Negative momentum detected |
| **SPY** | SELL | 73% | Negative momentum detected |
| **ETH/USD** | SELL | 71% | Negative momentum detected |
| **SOL/USD** | SELL | 77% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 4.0000 | $298.13 | $298.50 | $1,194.00 | 🟢 +$1.46 | +0.12% |
| **BTC/USD** | CRYPTO | 0.0180 | $81,502.71 | $76,894.68 | $1,384.66 | 🔴 $-82.98 | -5.65% |
| **ETH/USD** | CRYPTO | 0.6510 | $2,299.70 | $2,116.63 | $1,377.86 | 🔴 $-119.17 | -7.96% |
| **MSFT** | STOCK | 12.00 | $414.36 | $416.76 | $5,001.12 | 🟢 +$28.77 | +0.58% |
| **NVDA** | STOCK | 152.00 | $226.72 | $221.77 | $33,709.65 | 🔴 $-751.53 | -2.18% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $84.32 | $1,359.85 | 🔴 $-138.72 | -9.26% |
| **SPY** | ETF | 2.0000 | $742.75 | $733.50 | $1,467.01 | 🔴 $-18.49 | -1.24% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $298.97 | 🟢 +0.38% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $220.61 | 🔴 -0.77% | **SELL** | 75% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $404.11 | 🔴 -1.43% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $417.42 | 🔴 -1.44% | **SELL** | 89% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $259.34 | 🔴 -2.08% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $602.61 | 🔴 -1.41% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $733.73 | 🔴 -0.67% | **SELL** | 73% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $76,941.45 | 🔴 -0.01% | HOLD | — |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,116.97 | 🔴 -0.57% | **SELL** | 71% |
| 10 | **SOL/USD** | Solana | CRYPTO | $84.53 | 🔴 -0.87% | **SELL** | 77% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.38%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 66% | Moderate negative momentum (-0.77%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **SELL** | 78% | Moderate negative momentum (-1.43%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 78% | Moderate negative momentum (-1.44%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.08%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 78% | Moderate negative momentum (-1.41%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | **SELL** | 65% | Moderate negative momentum (-0.67%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.01%) — no trend to carry forward |
| 9 | **ETH/USD** | Ethereum | **SELL** | 63% | Moderate negative momentum (-0.57%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 68% | Moderate negative momentum (-0.87%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
