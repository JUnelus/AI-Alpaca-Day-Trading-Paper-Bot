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

> 🕐 **Last updated:** 2026-06-02 22:07 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,278.52` |
| 💸 Cash Available    | `$34,896.33` |
| 🧾 Buying Power      | `$127,127.45` |
| 🔴 Total P&L | `$-811.51` &nbsp; `(-8.12%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-811.51` (-8.12%)
- **Yesterday-to-today P&L:** `$-161.05`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 100% | Positive momentum detected |
| **NVDA** | SELL | 74% | Negative momentum detected |
| **TSLA** | BUY | 98% | Positive momentum detected |
| **MSFT** | SELL | 100% | Negative momentum detected |
| **BTC/USD** | SELL | 100% | Negative momentum detected |
| **ETH/USD** | SELL | 100% | Negative momentum detected |
| **SOL/USD** | SELL | 100% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $309.67 | $314.99 | $15,119.52 | 🟢 +$255.22 | +1.72% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $67,327.60 | $1,175.66 | 🔴 $-177.73 | -13.13% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $1,894.10 | $1,188.06 | 🔴 $-143.14 | -10.75% |
| **META** | STOCK | 2.0000 | $608.05 | $601.13 | $1,202.26 | 🔴 $-13.84 | -1.14% |
| **MSFT** | STOCK | 15.00 | $446.68 | $440.61 | $6,609.15 | 🔴 $-90.98 | -1.36% |
| **NVDA** | STOCK | 108.00 | $225.77 | $222.35 | $24,013.84 | 🔴 $-368.86 | -1.51% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $75.07 | $1,157.43 | 🔴 $-170.95 | -12.87% |
| **SPY** | ETF | 7.0000 | $744.36 | $759.73 | $5,318.11 | 🟢 +$107.61 | +2.07% |
| **TSLA** | STOCK | 18.00 | $433.72 | $422.12 | $7,598.16 | 🔴 $-208.84 | -2.68% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $315.20 | 🟢 +2.90% | **BUY** | 100% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $222.82 | 🔴 -0.69% | **SELL** | 74% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $423.74 | 🟢 +1.89% | **BUY** | 98% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $441.31 | 🔴 -4.17% | **SELL** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $256.52 | 🔴 -1.81% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $597.63 | 🔴 -0.47% | **SELL** | 69% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $759.57 | 🟢 +0.14% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $67,316.41 | 🔴 -5.60% | **SELL** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $1,894.23 | 🔴 -5.47% | **SELL** | 100% |
| 10 | **SOL/USD** | Solana | CRYPTO | $75.31 | 🔴 -7.20% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 70% | Extreme gain today (+2.90%) — mean reversion pullback likely |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 65% | Moderate negative momentum (-0.69%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 85% | Moderate positive momentum (+1.89%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 76% | Extreme loss today (-4.17%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-1.81%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 61% | Moderate negative momentum (-0.47%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (+0.14%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 78% | Extreme loss today (-5.60%) — mean reversion pullback likely |
| 9 | **ETH/USD** | Ethereum | **BUY** | 78% | Extreme loss today (-5.47%) — mean reversion pullback likely |
| 10 | **SOL/USD** | Solana | **BUY** | 78% | Extreme loss today (-7.20%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
