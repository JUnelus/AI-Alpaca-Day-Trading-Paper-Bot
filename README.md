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

> 🕐 **Last updated:** 2026-05-19 14:41 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,054.13` |
| 💸 Cash Available    | `$49,728.65` |
| 🧾 Buying Power      | `$144,680.30` |
| 🔴 Total P&L | `$-1,433.98` &nbsp; `(-14.34%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,433.98` (-14.34%)
- **Yesterday-to-today P&L:** `$-570.16`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | SELL | 82% | Negative momentum detected |
| **AMZN** | SELL | 100% | Negative momentum detected |
| **SPY** | SELL | 75% | Negative momentum detected |
| **BTC/USD** | SELL | 74% | Negative momentum detected |
| **ETH/USD** | SELL | 81% | Negative momentum detected |
| **SOL/USD** | SELL | 84% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 4.0000 | $298.13 | $296.94 | $1,187.76 | 🔴 $-4.78 | -0.40% |
| **AMZN** | STOCK | 5.0000 | $267.77 | $257.26 | $1,286.33 | 🔴 $-52.52 | -3.92% |
| **BTC/USD** | CRYPTO | 0.0180 | $81,502.71 | $76,404.70 | $1,375.84 | 🔴 $-91.80 | -6.26% |
| **ETH/USD** | CRYPTO | 0.6510 | $2,299.70 | $2,105.40 | $1,370.55 | 🔴 $-126.48 | -8.45% |
| **MSFT** | STOCK | 12.00 | $414.36 | $424.35 | $5,092.20 | 🟢 +$119.85 | +2.41% |
| **NVDA** | STOCK | 158.00 | $226.72 | $219.78 | $34,725.24 | 🔴 $-1,096.25 | -3.06% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $84.09 | $1,356.09 | 🔴 $-142.48 | -9.51% |
| **SPY** | ETF | 4.0000 | $742.75 | $732.87 | $2,931.48 | 🔴 $-39.51 | -1.33% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $296.81 | 🔴 -0.34% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $219.91 | 🔴 -1.08% | **SELL** | 82% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $397.06 | 🔴 -3.15% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $424.61 | 🟢 +0.25% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $257.36 | 🔴 -2.83% | **SELL** | 100% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $607.64 | 🔴 -0.58% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $733.15 | 🔴 -0.74% | **SELL** | 75% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $76,414.65 | 🔴 -0.69% | **SELL** | 74% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,107.23 | 🔴 -1.03% | **SELL** | 81% |
| 10 | **SOL/USD** | Solana | CRYPTO | $84.27 | 🔴 -1.18% | **SELL** | 84% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.34%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 72% | Moderate negative momentum (-1.08%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 71% | Extreme loss today (-3.15%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.25%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 69% | Extreme loss today (-2.83%) — mean reversion pullback likely |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 63% | Moderate negative momentum (-0.58%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | **SELL** | 66% | Moderate negative momentum (-0.74%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 65% | Moderate negative momentum (-0.69%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 71% | Moderate negative momentum (-1.03%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 74% | Moderate negative momentum (-1.18%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
