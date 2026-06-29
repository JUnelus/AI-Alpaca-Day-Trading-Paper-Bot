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

> The active 10 symbols are refreshed automatically once per ISO week from a larger universe,
> ranked by market value (market cap for stocks/crypto, total assets fallback for ETFs).

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
| Watchlist refresh          | Weekly top-10 by market value             |
| Entry style                | DCA on dips for quality assets            |
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

> 🕐 **Last updated:** 2026-06-29 21:44 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$92,819.62` |
| 💸 Cash Available    | `$-23,998.50` |
| 🧾 Buying Power      | `$186,581.18` |
| 🔴 Total P&L | `$-6,253.61` &nbsp; `(-62.54%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-6,253.61` (-62.54%)
- **Yesterday-to-today P&L:** `+$2,349.32`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | SELL | 100% | Take-profit trim after overextended rally |
| **AAPL** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 59.00 | $306.38 | $281.40 | $16,602.60 | 🔴 $-1,474.12 | -8.15% |
| **AMZN** | STOCK | 26.00 | $240.18 | $240.30 | $6,247.80 | 🟢 +$3.06 | +0.05% |
| **AVGO** | STOCK | 9.0000 | $380.51 | $372.25 | $3,350.25 | 🔴 $-74.34 | -2.17% |
| **BTC/USD** | CRYPTO | 0.1768 | $64,498.90 | $60,331.87 | $10,668.47 | 🔴 $-736.86 | -6.46% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,615.10 | $1,013.06 | 🔴 $-318.14 | -23.90% |
| **GOOGL** | STOCK | 17.00 | $353.61 | $352.60 | $5,994.20 | 🔴 $-17.14 | -0.29% |
| **LLY** | STOCK | 10.00 | $1,123.81 | $1,228.74 | $12,287.38 | 🟢 +$1,049.27 | +9.34% |
| **META** | STOCK | 17.00 | $578.39 | $563.02 | $9,571.34 | 🔴 $-261.34 | -2.66% |
| **MSFT** | STOCK | 21.00 | $404.92 | $370.58 | $7,782.11 | 🔴 $-721.26 | -8.48% |
| **NVDA** | STOCK | 122.00 | $219.68 | $194.95 | $23,783.89 | 🔴 $-3,017.22 | -11.26% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $75.54 | $1,164.73 | 🔴 $-163.65 | -12.32% |
| **SPY** | STOCK | 6.0000 | $745.44 | $740.66 | $4,443.96 | 🔴 $-28.70 | -0.64% |
| **TSLA** | STOCK | 24.00 | $432.23 | $411.15 | $9,867.60 | 🔴 $-505.97 | -4.88% |
| **VTI** | ETF | 11.00 | $366.18 | $367.34 | $4,040.74 | 🟢 +$12.78 | +0.32% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $194.97 | 🟢 +1.27% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $353.65 | 🟢 +4.82% | **SELL** | 100% |
| 3 | **AAPL** | Apple Inc. | STOCK | $281.64 | 🔴 -0.75% | **BUY** | 81% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $368.57 | 🔴 -1.18% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $240.14 | 🟢 +3.20% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $367.12 | 🟢 +1.35% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $372.45 | 🟢 +2.04% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $562.33 | 🟢 +2.20% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $60,378.33 | 🟢 +1.52% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,229.93 | 🟢 +1.81% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.27%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 78% | Extreme gain today (+4.82%) — mean reversion pullback likely |
| 3 | **AAPL** | Apple Inc. | **SELL** | 71% | Moderate negative momentum (-0.75%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.18%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 71% | Extreme gain today (+3.20%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.35%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+2.04%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+2.20%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.52%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.81%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
