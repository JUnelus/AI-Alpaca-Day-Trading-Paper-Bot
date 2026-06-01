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

> 🕐 **Last updated:** 2026-06-01 15:44 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,294.69` |
| 💸 Cash Available    | `$39,101.29` |
| 🧾 Buying Power      | `$130,975.79` |
| 🔴 Total P&L | `$-832.10` &nbsp; `(-8.32%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-832.10` (-8.32%)
- **Yesterday-to-today P&L:** `+$314.05`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | SELL | 93% | Negative momentum detected |
| **NVDA** | BUY | 100% | Positive momentum detected |
| **TSLA** | SELL | 100% | Negative momentum detected |
| **MSFT** | BUY | 100% | Positive momentum detected |
| **BTC/USD** | SELL | 100% | Negative momentum detected |
| **ETH/USD** | SELL | 93% | Negative momentum detected |
| **SOL/USD** | SELL | 100% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $308.65 | $306.87 | $15,956.98 | 🔴 $-92.74 | -0.58% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $71,205.00 | $1,243.36 | 🔴 $-110.02 | -8.13% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $1,972.70 | $1,237.36 | 🔴 $-93.84 | -7.05% |
| **MSFT** | STOCK | 12.00 | $441.72 | $461.17 | $5,533.98 | 🟢 +$233.39 | +4.40% |
| **NVDA** | STOCK | 90.00 | $225.99 | $220.10 | $19,809.45 | 🔴 $-530.02 | -2.61% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $80.10 | $1,235.06 | 🔴 $-93.32 | -7.02% |
| **SPY** | ETF | 7.0000 | $744.36 | $757.25 | $5,300.75 | 🟢 +$90.25 | +1.73% |
| **TSLA** | STOCK | 21.00 | $433.94 | $422.71 | $8,876.91 | 🔴 $-235.79 | -2.59% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $306.93 | 🔴 -1.64% | **SELL** | 93% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $220.02 | 🟢 +4.21% | **BUY** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $423.12 | 🔴 -2.91% | **SELL** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $461.49 | 🟢 +2.50% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $264.27 | 🔴 -2.35% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $613.79 | 🔴 -2.96% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $757.25 | 🟢 +0.10% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $71,156.78 | 🔴 -3.31% | **SELL** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $1,971.37 | 🔴 -1.63% | **SELL** | 93% |
| 10 | **SOL/USD** | Solana | CRYPTO | $79.78 | 🔴 -3.07% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 82% | Moderate negative momentum (-1.64%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 76% | Extreme gain today (+4.21%) — mean reversion pullback likely |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 70% | Extreme loss today (-2.91%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 85% | Moderate positive momentum (+2.50%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.35%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **BUY** | 70% | Extreme loss today (-2.96%) — mean reversion pullback likely |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (+0.10%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 72% | Extreme loss today (-3.31%) — mean reversion pullback likely |
| 9 | **ETH/USD** | Ethereum | **SELL** | 82% | Moderate negative momentum (-1.63%) — continuation expected |
| 10 | **SOL/USD** | Solana | **BUY** | 70% | Extreme loss today (-3.07%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
