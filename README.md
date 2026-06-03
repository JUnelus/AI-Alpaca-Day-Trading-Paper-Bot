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

> 🕐 **Last updated:** 2026-06-03 15:20 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$97,430.93` |
| 💸 Cash Available    | `$35,003.01` |
| 🧾 Buying Power      | `$126,456.18` |
| 🔴 Total P&L | `$-1,696.89` &nbsp; `(-16.97%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,696.89` (-16.97%)
- **Yesterday-to-today P&L:** `$-885.38`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | SELL | 85% | Negative momentum detected |
| **NVDA** | SELL | 100% | Negative momentum detected |
| **TSLA** | BUY | 92% | Positive momentum detected |
| **MSFT** | SELL | 100% | Negative momentum detected |
| **META** | BUY | 100% | Positive momentum detected |
| **BTC/USD** | SELL | 72% | Negative momentum detected |
| **ETH/USD** | SELL | 74% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $310.82 | $311.34 | $16,189.68 | 🟢 +$27.10 | +0.17% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $66,257.98 | $1,156.98 | 🔴 $-196.41 | -14.51% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $1,844.86 | $1,157.17 | 🔴 $-174.02 | -13.07% |
| **META** | STOCK | 2.0000 | $608.05 | $617.29 | $1,234.59 | 🟢 +$18.49 | +1.52% |
| **MSFT** | STOCK | 12.00 | $450.97 | $427.26 | $5,127.18 | 🔴 $-284.50 | -5.26% |
| **NVDA** | STOCK | 102.00 | $225.77 | $216.64 | $22,097.08 | 🔴 $-931.03 | -4.04% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $73.81 | $1,138.06 | 🔴 $-190.32 | -14.33% |
| **SPY** | ETF | 7.0000 | $744.36 | $756.17 | $5,293.19 | 🟢 +$82.69 | +1.59% |
| **TSLA** | STOCK | 21.00 | $432.52 | $430.19 | $9,033.99 | 🔴 $-48.89 | -0.54% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $311.23 | 🔴 -1.26% | **SELL** | 85% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $216.53 | 🔴 -2.82% | **SELL** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $430.49 | 🟢 +1.59% | **BUY** | 92% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $427.30 | 🔴 -3.18% | **SELL** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $250.72 | 🔴 -2.26% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $617.15 | 🟢 +3.27% | **BUY** | 100% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $756.09 | 🔴 -0.46% | **SELL** | 69% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $66,242.35 | 🔴 -0.61% | **SELL** | 72% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $1,843.98 | 🔴 -0.70% | **SELL** | 74% |
| 10 | **SOL/USD** | Solana | CRYPTO | $73.71 | 🔴 -0.54% | **SELL** | 71% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.26%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 69% | Extreme loss today (-2.82%) — mean reversion pullback likely |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 81% | Moderate positive momentum (+1.59%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 71% | Extreme loss today (-3.18%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.26%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 71% | Extreme gain today (+3.27%) — mean reversion pullback likely |
| 7 | **SPY** | SPDR S&P 500 ETF | **SELL** | 61% | Moderate negative momentum (-0.46%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 63% | Moderate negative momentum (-0.61%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 65% | Moderate negative momentum (-0.70%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 62% | Moderate negative momentum (-0.54%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
