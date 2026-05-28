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

> 🕐 **Last updated:** 2026-05-28 21:53 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,449.11` |
| 💸 Cash Available    | `$39,977.47` |
| 🧾 Buying Power      | `$128,442.65` |
| 🔴 Total P&L | `$-783.80` &nbsp; `(-7.84%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-783.80` (-7.84%)
- **Yesterday-to-today P&L:** `+$459.64`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 71% | Positive momentum detected |
| **NVDA** | BUY | 76% | Positive momentum detected |
| **MSFT** | BUY | 100% | Positive momentum detected |
| **AMZN** | BUY | 76% | Positive momentum detected |
| **SPY** | BUY | 71% | Positive momentum detected |
| **BTC/USD** | SELL | 75% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $308.21 | $312.35 | $14,992.80 | 🟢 +$198.52 | +1.34% |
| **AMZN** | STOCK | 5.0000 | $270.57 | $273.52 | $1,367.60 | 🟢 +$14.76 | +1.09% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $73,832.60 | $1,289.25 | 🔴 $-64.14 | -4.74% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $2,019.19 | $1,266.52 | 🔴 $-64.67 | -4.86% |
| **META** | STOCK | 2.0000 | $634.20 | $633.90 | $1,267.80 | 🔴 $-0.60 | -0.05% |
| **MSFT** | STOCK | 3.0000 | $425.19 | $427.60 | $1,282.80 | 🟢 +$7.24 | +0.57% |
| **NVDA** | STOCK | 90.00 | $226.85 | $214.18 | $19,276.20 | 🔴 $-1,140.29 | -5.59% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $82.61 | $1,273.70 | 🔴 $-54.68 | -4.12% |
| **SPY** | ETF | 6.0000 | $742.43 | $755.24 | $4,531.44 | 🟢 +$76.83 | +1.72% |
| **TSLA** | STOCK | 27.00 | $432.60 | $441.61 | $11,923.54 | 🟢 +$243.24 | +2.08% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $312.51 | 🟢 +0.53% | **BUY** | 71% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $214.25 | 🟢 +0.78% | **BUY** | 76% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $442.10 | 🟢 +0.40% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $426.99 | 🟢 +3.47% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $274.00 | 🟢 +0.79% | **BUY** | 76% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $635.29 | 🟢 +0.01% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $754.60 | 🟢 +0.55% | **BUY** | 71% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $73,782.60 | 🔴 -0.73% | **SELL** | 75% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,019.51 | 🔴 -0.10% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $82.40 | 🟢 +0.12% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 62% | Moderate positive momentum (+0.53%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 66% | Moderate positive momentum (+0.78%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | HOLD | 50% | Flat session today (+0.40%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 72% | Extreme gain today (+3.47%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 67% | Moderate positive momentum (+0.79%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.01%) — no trend to carry forward |
| 7 | **SPY** | SPDR S&P 500 ETF | **BUY** | 63% | Moderate positive momentum (+0.55%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 66% | Moderate negative momentum (-0.73%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | HOLD | 50% | Flat session today (-0.10%) — no trend to carry forward |
| 10 | **SOL/USD** | Solana | HOLD | 50% | Flat session today (+0.12%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
