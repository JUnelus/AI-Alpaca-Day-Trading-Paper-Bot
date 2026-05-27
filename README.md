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

> 🕐 **Last updated:** 2026-05-27 21:53 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,077.72` |
| 💸 Cash Available    | `$43,587.16` |
| 🧾 Buying Power      | `$132,642.21` |
| 🔴 Total P&L | `$-1,243.44` &nbsp; `(-12.43%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,243.44` (-12.43%)
- **Yesterday-to-today P&L:** `$-124.06`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 76% | Positive momentum detected |
| **NVDA** | SELL | 81% | Negative momentum detected |
| **TSLA** | BUY | 91% | Positive momentum detected |
| **AMZN** | BUY | 100% | Positive momentum detected |
| **META** | BUY | 100% | Positive momentum detected |
| **BTC/USD** | SELL | 100% | Negative momentum detected |
| **ETH/USD** | SELL | 100% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 44.00 | $308.02 | $310.60 | $13,666.40 | 🟢 +$113.40 | +0.84% |
| **AMZN** | STOCK | 5.0000 | $270.58 | $272.71 | $1,363.55 | 🟢 +$10.64 | +0.79% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $74,331.20 | $1,297.95 | 🔴 $-55.44 | -4.10% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $2,016.80 | $1,265.02 | 🔴 $-66.17 | -4.97% |
| **NVDA** | STOCK | 97.00 | $226.75 | $212.16 | $20,579.52 | 🔴 $-1,415.54 | -6.44% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $82.18 | $1,267.06 | 🔴 $-61.32 | -4.62% |
| **SPY** | ETF | 6.0000 | $742.43 | $751.47 | $4,508.82 | 🟢 +$54.21 | +1.22% |
| **TSLA** | STOCK | 24.00 | $431.89 | $439.26 | $10,542.24 | 🟢 +$176.77 | +1.71% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $310.85 | 🟢 +0.82% | **BUY** | 76% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $212.60 | 🔴 -1.05% | **SELL** | 81% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $440.36 | 🟢 +1.56% | **BUY** | 91% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $412.67 | 🔴 -0.81% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $271.85 | 🟢 +2.47% | **BUY** | 100% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $635.25 | 🟢 +3.74% | **BUY** | 100% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $750.46 | 🔴 -0.02% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $74,301.95 | 🔴 -2.00% | **SELL** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,020.30 | 🔴 -2.42% | **SELL** | 100% |
| 10 | **SOL/USD** | Solana | CRYPTO | $82.10 | 🔴 -1.75% | **SELL** | 95% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 67% | Moderate positive momentum (+0.82%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 71% | Moderate negative momentum (-1.05%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 80% | Moderate positive momentum (+1.56%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 67% | Moderate negative momentum (-0.81%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 85% | Moderate positive momentum (+2.47%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 74% | Extreme gain today (+3.74%) — mean reversion pullback likely |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (-0.02%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.00%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 85% | Moderate negative momentum (-2.42%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 84% | Moderate negative momentum (-1.75%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
