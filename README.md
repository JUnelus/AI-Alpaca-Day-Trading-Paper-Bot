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

> 🕐 **Last updated:** 2026-06-01 22:16 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,435.83` |
| 💸 Cash Available    | `$38,892.41` |
| 🧾 Buying Power      | `$130,892.45` |
| 🔴 Total P&L | `$-650.46` &nbsp; `(-6.50%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-650.46` (-6.50%)
- **Yesterday-to-today P&L:** `+$495.68`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | SELL | 97% | Negative momentum detected |
| **NVDA** | BUY | 100% | Positive momentum detected |
| **TSLA** | SELL | 100% | Negative momentum detected |
| **MSFT** | BUY | 100% | Positive momentum detected |
| **BTC/USD** | SELL | 100% | Negative momentum detected |
| **ETH/USD** | SELL | 77% | Negative momentum detected |
| **SOL/USD** | SELL | 100% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $308.65 | $305.65 | $14,671.20 | 🔴 $-143.93 | -0.97% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $70,904.70 | $1,238.12 | 🔴 $-115.27 | -8.52% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $1,988.85 | $1,247.49 | 🔴 $-83.71 | -6.29% |
| **MSFT** | STOCK | 15.00 | $445.62 | $453.70 | $6,805.50 | 🟢 +$121.25 | +1.81% |
| **NVDA** | STOCK | 96.00 | $225.63 | $224.69 | $21,570.24 | 🔴 $-89.91 | -0.42% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $80.50 | $1,241.25 | 🔴 $-87.13 | -6.56% |
| **SPY** | ETF | 7.0000 | $744.36 | $756.96 | $5,298.72 | 🟢 +$88.22 | +1.69% |
| **TSLA** | STOCK | 18.00 | $433.94 | $415.05 | $7,470.90 | 🔴 $-339.99 | -4.35% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $306.31 | 🔴 -1.84% | **SELL** | 97% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $224.36 | 🟢 +6.26% | **BUY** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $415.88 | 🔴 -4.57% | **SELL** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $460.52 | 🟢 +2.28% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $261.26 | 🔴 -3.47% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $600.47 | 🔴 -5.07% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $758.54 | 🟢 +0.27% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $70,885.56 | 🔴 -3.68% | **SELL** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $1,987.29 | 🔴 -0.84% | **SELL** | 77% |
| 10 | **SOL/USD** | Solana | CRYPTO | $80.35 | 🔴 -2.38% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 85% | Moderate negative momentum (-1.84%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 78% | Extreme gain today (+6.26%) — mean reversion pullback likely |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 78% | Extreme loss today (-4.57%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 85% | Moderate positive momentum (+2.28%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 72% | Extreme loss today (-3.47%) — mean reversion pullback likely |
| 6 | **META** | Meta Platforms Inc. | **BUY** | 78% | Extreme loss today (-5.07%) — mean reversion pullback likely |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (+0.27%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 73% | Extreme loss today (-3.68%) — mean reversion pullback likely |
| 9 | **ETH/USD** | Ethereum | **SELL** | 68% | Moderate negative momentum (-0.84%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 85% | Moderate negative momentum (-2.38%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
