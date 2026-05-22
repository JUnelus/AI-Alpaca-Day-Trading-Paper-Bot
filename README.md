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

> 🕐 **Last updated:** 2026-05-22 21:40 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,363.68` |
| 💸 Cash Available    | `$51,120.62` |
| 🧾 Buying Power      | `$142,939.30` |
| 🔴 Total P&L | `$-1,465.17` &nbsp; `(-14.65%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,465.17` (-14.65%)
- **Yesterday-to-today P&L:** `$-319.06`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 85% | Positive momentum detected |
| **NVDA** | SELL | 98% | Negative momentum detected |
| **TSLA** | BUY | 99% | Positive momentum detected |
| **AMZN** | SELL | 76% | Negative momentum detected |
| **BTC/USD** | SELL | 100% | Negative momentum detected |
| **ETH/USD** | SELL | 100% | Negative momentum detected |
| **SOL/USD** | SELL | 100% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 24.00 | $305.39 | $308.68 | $7,408.32 | 🟢 +$79.01 | +1.08% |
| **AMZN** | STOCK | 20.00 | $267.55 | $266.56 | $5,331.20 | 🔴 $-19.75 | -0.37% |
| **BTC/USD** | CRYPTO | 0.0176 | $77,432.95 | $76,006.17 | $1,338.49 | 🔴 $-25.13 | -1.84% |
| **ETH/USD** | CRYPTO | 0.6450 | $2,211.56 | $2,073.57 | $1,337.47 | 🔴 $-89.00 | -6.24% |
| **NVDA** | STOCK | 116.00 | $226.76 | $214.99 | $24,938.84 | 🔴 $-1,365.76 | -5.19% |
| **SOL/USD** | CRYPTO | 15.95 | $90.07 | $85.21 | $1,359.11 | 🔴 $-77.51 | -5.40% |
| **SPY** | ETF | 4.0000 | $737.94 | $744.83 | $2,979.33 | 🟢 +$27.56 | +0.93% |
| **TSLA** | STOCK | 6.0000 | $424.15 | $425.05 | $2,550.30 | 🟢 +$5.41 | +0.21% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $308.82 | 🟢 +1.26% | **BUY** | 85% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $215.33 | 🔴 -1.90% | **SELL** | 98% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $426.01 | 🟢 +1.95% | **BUY** | 99% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $418.57 | 🔴 -0.12% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $266.32 | 🔴 -0.80% | **SELL** | 76% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $610.26 | 🟢 +0.47% | **BUY** | 69% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $745.64 | 🟢 +0.39% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $75,936.30 | 🔴 -2.09% | **SELL** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,074.71 | 🔴 -2.65% | **SELL** | 100% |
| 10 | **SOL/USD** | Solana | CRYPTO | $85.07 | 🔴 -2.48% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 75% | Moderate positive momentum (+1.26%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-1.90%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 85% | Moderate positive momentum (+1.95%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.12%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 67% | Moderate negative momentum (-0.80%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **BUY** | 61% | Moderate positive momentum (+0.47%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (+0.39%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.09%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **BUY** | 68% | Extreme loss today (-2.65%) — mean reversion pullback likely |
| 10 | **SOL/USD** | Solana | **SELL** | 85% | Moderate negative momentum (-2.48%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
