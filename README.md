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

> 🕐 **Last updated:** 2026-05-26 21:51 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,305.83` |
| 💸 Cash Available    | `$48,137.22` |
| 🧾 Buying Power      | `$140,462.24` |
| 🔴 Total P&L | `$-1,119.38` &nbsp; `(-11.19%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,119.38` (-11.19%)
- **Yesterday-to-today P&L:** `+$228.24`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **TSLA** | BUY | 96% | Positive momentum detected |
| **SPY** | BUY | 73% | Positive momentum detected |
| **BTC/USD** | SELL | 96% | Negative momentum detected |
| **ETH/USD** | SELL | 96% | Negative momentum detected |
| **SOL/USD** | SELL | 90% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 40.00 | $307.56 | $308.41 | $12,336.40 | 🟢 +$34.16 | +0.28% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,527.19 | $75,862.79 | $1,324.70 | 🔴 $-29.06 | -2.15% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,126.13 | $2,076.58 | $1,302.51 | 🔴 $-31.08 | -2.33% |
| **NVDA** | STOCK | 104.00 | $226.47 | $214.45 | $22,302.81 | 🔴 $-1,250.18 | -5.31% |
| **SOL/USD** | CRYPTO | 15.42 | $86.75 | $83.91 | $1,293.79 | 🔴 $-43.73 | -3.27% |
| **SPY** | ETF | 5.0000 | $740.76 | $750.10 | $3,750.50 | 🟢 +$46.72 | +1.26% |
| **TSLA** | STOCK | 18.00 | $428.01 | $436.55 | $7,857.90 | 🟢 +$153.79 | +2.00% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $308.33 | 🔴 -0.16% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $214.86 | 🔴 -0.22% | HOLD | — |
| 3 | **TSLA** | Tesla Inc. | STOCK | $433.59 | 🟢 +1.78% | **BUY** | 96% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $416.03 | 🔴 -0.61% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $265.29 | 🔴 -0.39% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $612.34 | 🟢 +0.34% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $750.59 | 🟢 +0.66% | **BUY** | 73% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $75,877.58 | 🔴 -1.78% | **SELL** | 96% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,074.68 | 🔴 -1.78% | **SELL** | 96% |
| 10 | **SOL/USD** | Solana | CRYPTO | $83.74 | 🔴 -1.50% | **SELL** | 90% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.16%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.22%) — no trend to carry forward |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 84% | Moderate positive momentum (+1.78%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 63% | Moderate negative momentum (-0.61%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |
| 6 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.34%) — no trend to carry forward |
| 7 | **SPY** | SPDR S&P 500 ETF | **BUY** | 64% | Moderate positive momentum (+0.66%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 84% | Moderate negative momentum (-1.78%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 84% | Moderate negative momentum (-1.78%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 79% | Moderate negative momentum (-1.50%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
