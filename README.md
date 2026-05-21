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

> 🕐 **Last updated:** 2026-05-21 21:47 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,053.91` |
| 💸 Cash Available    | `$51,594.92` |
| 🧾 Buying Power      | `$139,365.40` |
| 🔴 Total P&L | `$-1,146.12` &nbsp; `(-11.46%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,146.12` (-11.46%)
- **Yesterday-to-today P&L:** `$-218.74`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 78% | Positive momentum detected |
| **NVDA** | SELL | 95% | Negative momentum detected |
| **AMZN** | BUY | 86% | Positive momentum detected |
| **SOL/USD** | BUY | 89% | Positive momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 8.0000 | $299.74 | $304.55 | $2,436.40 | 🟢 +$38.46 | +1.60% |
| **AMZN** | STOCK | 5.0000 | $262.76 | $268.55 | $1,342.75 | 🟢 +$28.93 | +2.20% |
| **BTC/USD** | CRYPTO | 0.0372 | $78,714.67 | $77,671.60 | $2,890.18 | 🔴 $-38.81 | -1.33% |
| **ETH/USD** | CRYPTO | 1.3536 | $2,211.56 | $2,136.61 | $2,892.12 | 🔴 $-101.46 | -3.39% |
| **NVDA** | STOCK | 140.00 | $226.71 | $219.52 | $30,732.80 | 🔴 $-1,006.37 | -3.17% |
| **SOL/USD** | CRYPTO | 33.26 | $90.07 | $87.28 | $2,903.10 | 🔴 $-92.96 | -3.10% |
| **SPY** | ETF | 4.0000 | $737.94 | $743.07 | $2,972.28 | 🟢 +$20.51 | +0.69% |
| **TSLA** | STOCK | 3.0000 | $415.47 | $417.33 | $1,251.99 | 🟢 +$5.59 | +0.45% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $304.99 | 🟢 +0.91% | **BUY** | 78% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $219.51 | 🔴 -1.77% | **SELL** | 95% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $417.85 | 🟢 +0.14% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $419.09 | 🔴 -0.47% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $268.46 | 🟢 +1.30% | **BUY** | 86% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $607.38 | 🟢 +0.38% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $742.72 | 🟢 +0.20% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $77,621.48 | 🟢 +0.20% | HOLD | — |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,134.20 | 🟢 +0.31% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $87.32 | 🟢 +1.45% | **BUY** | 89% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 69% | Moderate positive momentum (+0.91%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 84% | Moderate negative momentum (-1.77%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | HOLD | 50% | Flat session today (+0.14%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 61% | Moderate negative momentum (-0.47%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 76% | Moderate positive momentum (+1.30%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.38%) — no trend to carry forward |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (+0.20%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.20%) — no trend to carry forward |
| 9 | **ETH/USD** | Ethereum | HOLD | 50% | Flat session today (+0.31%) — no trend to carry forward |
| 10 | **SOL/USD** | Solana | **BUY** | 78% | Moderate positive momentum (+1.45%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
