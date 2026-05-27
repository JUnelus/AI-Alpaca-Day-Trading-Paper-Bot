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

> 🕐 **Last updated:** 2026-05-27 14:45 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,031.22` |
| 💸 Cash Available    | `$46,054.53` |
| 🧾 Buying Power      | `$136,269.25` |
| 🔴 Total P&L | `$-1,411.42` &nbsp; `(-14.11%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,411.42` (-14.11%)
- **Yesterday-to-today P&L:** `$-292.03`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 89% | Positive momentum detected |
| **NVDA** | SELL | 100% | Negative momentum detected |
| **TSLA** | BUY | 100% | Positive momentum detected |
| **AMZN** | BUY | 99% | Positive momentum detected |
| **BTC/USD** | SELL | 83% | Negative momentum detected |
| **ETH/USD** | SELL | 74% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 40.00 | $307.56 | $312.69 | $12,507.40 | 🟢 +$205.16 | +1.67% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $75,000.50 | $1,309.64 | 🔴 $-43.75 | -3.23% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $2,057.06 | $1,290.27 | 🔴 $-40.92 | -3.07% |
| **NVDA** | STOCK | 104.00 | $226.75 | $209.40 | $21,777.60 | 🔴 $-1,804.73 | -7.65% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $83.25 | $1,283.54 | 🔴 $-44.84 | -3.38% |
| **SPY** | ETF | 6.0000 | $742.43 | $750.28 | $4,501.68 | 🟢 +$47.07 | +1.06% |
| **TSLA** | STOCK | 21.00 | $430.28 | $443.17 | $9,306.57 | 🟢 +$270.60 | +2.99% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $312.74 | 🟢 +1.43% | **BUY** | 89% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $209.44 | 🔴 -2.52% | **SELL** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $443.79 | 🟢 +2.35% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $415.06 | 🔴 -0.23% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $270.43 | 🟢 +1.94% | **BUY** | 99% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $613.23 | 🟢 +0.14% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $750.42 | 🔴 -0.02% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $74,946.12 | 🔴 -1.15% | **SELL** | 83% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,056.18 | 🔴 -0.69% | **SELL** | 74% |
| 10 | **SOL/USD** | Solana | CRYPTO | $83.41 | 🔴 -0.19% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 78% | Moderate positive momentum (+1.43%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 68% | Extreme loss today (-2.52%) — mean reversion pullback likely |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 85% | Moderate positive momentum (+2.35%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.23%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 85% | Moderate positive momentum (+1.94%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.14%) — no trend to carry forward |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (-0.02%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 73% | Moderate negative momentum (-1.15%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 65% | Moderate negative momentum (-0.69%) — continuation expected |
| 10 | **SOL/USD** | Solana | HOLD | 50% | Flat session today (-0.19%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
