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

> 🕐 **Last updated:** 2026-05-14 14:36 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$102,001.17` |
| 💸 Cash Available    | `$57,643.60` |
| 🧾 Buying Power      | `$152,752.04` |
| 🟢 Total P&L | `+$1,391.22` &nbsp; `(+13.91%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$1,391.22` (+13.91%)
- **Yesterday-to-today P&L:** `+$858.84`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | Positive momentum detected |
| **MSFT** | BUY | 70% | Positive momentum detected |
| **META** | BUY | 71% | Positive momentum detected |
| **SPY** | BUY | 70% | Positive momentum detected |
| **BTC/USD** | BUY | 81% | Positive momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **NVDA** | STOCK | 170.00 | $226.23 | $234.37 | $39,842.87 | 🟢 +$1,384.11 | +3.60% |
| **SPY** | ETF | 4.0000 | $744.36 | $746.14 | $2,984.56 | 🟢 +$7.11 | +0.24% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $297.90 | 🔴 -0.32% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $234.16 | 🟢 +3.69% | **BUY** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $443.40 | 🔴 -0.42% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $407.28 | 🟢 +0.51% | **BUY** | 70% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $267.38 | 🔴 -1.02% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $620.12 | 🟢 +0.57% | **BUY** | 71% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $746.04 | 🟢 +0.50% | **BUY** | 70% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $80,114.76 | 🟢 +1.04% | **BUY** | 81% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,265.16 | 🟢 +0.33% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $91.31 | 🟢 +0.22% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.32%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 73% | Extreme gain today (+3.69%) — mean reversion pullback likely |
| 3 | **TSLA** | Tesla Inc. | **SELL** | 60% | Moderate negative momentum (-0.42%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 62% | Moderate positive momentum (+0.51%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 71% | Moderate negative momentum (-1.02%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **BUY** | 63% | Moderate positive momentum (+0.57%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | **BUY** | 62% | Moderate positive momentum (+0.50%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 71% | Moderate positive momentum (+1.04%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | HOLD | 50% | Flat session today (+0.33%) — no trend to carry forward |
| 10 | **SOL/USD** | Solana | HOLD | 50% | Flat session today (+0.22%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
