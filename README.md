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

> 🕐 **Last updated:** 2026-05-22 14:39 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,708.91` |
| 💸 Cash Available    | `$50,840.36` |
| 🧾 Buying Power      | `$141,430.62` |
| 🔴 Total P&L | `$-1,184.91` &nbsp; `(-11.85%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,184.91` (-11.85%)
- **Yesterday-to-today P&L:** `$-38.79`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 88% | Positive momentum detected |
| **NVDA** | SELL | 85% | Negative momentum detected |
| **TSLA** | BUY | 100% | Positive momentum detected |
| **BTC/USD** | SELL | 82% | Negative momentum detected |
| **ETH/USD** | SELL | 74% | Negative momentum detected |
| **SOL/USD** | SELL | 73% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 20.00 | $304.60 | $309.31 | $6,186.10 | 🟢 +$94.15 | +1.55% |
| **AMZN** | STOCK | 20.00 | $267.55 | $268.49 | $5,369.80 | 🟢 +$18.85 | +0.35% |
| **BTC/USD** | CRYPTO | 0.0176 | $77,432.95 | $76,726.90 | $1,351.18 | 🔴 $-12.43 | -0.91% |
| **ETH/USD** | CRYPTO | 0.6450 | $2,211.56 | $2,119.09 | $1,366.83 | 🔴 $-59.64 | -4.18% |
| **NVDA** | STOCK | 122.00 | $226.76 | $216.78 | $26,447.16 | 🔴 $-1,218.03 | -4.40% |
| **SOL/USD** | CRYPTO | 15.95 | $90.07 | $86.71 | $1,383.10 | 🔴 $-53.52 | -3.73% |
| **SPY** | ETF | 4.0000 | $737.94 | $746.07 | $2,984.28 | 🟢 +$32.51 | +1.10% |
| **TSLA** | STOCK | 3.0000 | $421.93 | $426.33 | $1,278.99 | 🟢 +$13.21 | +1.04% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $309.19 | 🟢 +1.38% | **BUY** | 88% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $216.72 | 🔴 -1.27% | **SELL** | 85% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $426.77 | 🟢 +2.13% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $417.80 | 🔴 -0.31% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $268.57 | 🟢 +0.04% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $609.40 | 🟢 +0.33% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $746.24 | 🟢 +0.47% | **BUY** | 69% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $76,701.56 | 🔴 -1.10% | **SELL** | 82% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,116.76 | 🔴 -0.68% | **SELL** | 74% |
| 10 | **SOL/USD** | Solana | CRYPTO | $86.65 | 🔴 -0.67% | **SELL** | 73% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 77% | Moderate positive momentum (+1.38%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Moderate negative momentum (-1.27%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 85% | Moderate positive momentum (+2.13%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.31%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.04%) — no trend to carry forward |
| 6 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.33%) — no trend to carry forward |
| 7 | **SPY** | SPDR S&P 500 ETF | **BUY** | 61% | Moderate positive momentum (+0.47%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 72% | Moderate negative momentum (-1.10%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 65% | Moderate negative momentum (-0.68%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 65% | Moderate negative momentum (-0.67%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
