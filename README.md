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

> 🕐 **Last updated:** 2026-05-28 14:53 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,118.57` |
| 💸 Cash Available    | `$39,900.90` |
| 🧾 Buying Power      | `$132,983.99` |
| 🔴 Total P&L | `$-1,115.06` &nbsp; `(-11.15%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,115.06` (-11.15%)
- **Yesterday-to-today P&L:** `+$128.39`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **MSFT** | BUY | 100% | Positive momentum detected |
| **AMZN** | SELL | 71% | Negative momentum detected |
| **BTC/USD** | SELL | 100% | Negative momentum detected |
| **ETH/USD** | SELL | 94% | Negative momentum detected |
| **SOL/USD** | SELL | 95% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $308.21 | $311.44 | $14,949.10 | 🟢 +$154.82 | +1.05% |
| **AMZN** | STOCK | 10.00 | $270.57 | $270.43 | $2,704.30 | 🔴 $-1.39 | -0.05% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $72,774.91 | $1,270.78 | 🔴 $-82.61 | -6.10% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $1,982.79 | $1,243.69 | 🔴 $-87.51 | -6.57% |
| **META** | STOCK | 2.0000 | $634.20 | $635.81 | $1,271.62 | 🟢 +$3.22 | +0.25% |
| **NVDA** | STOCK | 90.00 | $226.85 | $212.14 | $19,092.76 | 🔴 $-1,323.73 | -6.48% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $80.77 | $1,245.37 | 🔴 $-83.02 | -6.25% |
| **SPY** | ETF | 6.0000 | $742.43 | $752.77 | $4,516.60 | 🟢 +$61.99 | +1.39% |
| **TSLA** | STOCK | 27.00 | $432.60 | $441.61 | $11,923.47 | 🟢 +$243.17 | +2.08% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $311.30 | 🟢 +0.14% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $212.06 | 🔴 -0.25% | HOLD | — |
| 3 | **TSLA** | Tesla Inc. | STOCK | $441.81 | 🟢 +0.33% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $424.95 | 🟢 +2.98% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $270.37 | 🔴 -0.55% | **SELL** | 71% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $635.82 | 🟢 +0.09% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $752.68 | 🟢 +0.30% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $72,808.11 | 🔴 -2.04% | **SELL** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $1,986.81 | 🔴 -1.72% | **SELL** | 94% |
| 10 | **SOL/USD** | Solana | CRYPTO | $80.86 | 🔴 -1.75% | **SELL** | 95% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.14%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.25%) — no trend to carry forward |
| 3 | **TSLA** | Tesla Inc. | HOLD | 50% | Flat session today (+0.33%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 70% | Extreme gain today (+2.98%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 62% | Moderate negative momentum (-0.55%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.09%) — no trend to carry forward |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (+0.30%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.04%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 83% | Moderate negative momentum (-1.72%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 84% | Moderate negative momentum (-1.75%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
