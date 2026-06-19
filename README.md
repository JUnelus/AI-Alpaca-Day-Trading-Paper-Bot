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

> 🕐 **Last updated:** 2026-06-19 14:41 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,512.69` |
| 💸 Cash Available    | `$-6,448.00` |
| 🧾 Buying Power      | `$218,831.84` |
| 🔴 Total P&L | `$-4,347.77` &nbsp; `(-43.48%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-4,347.77` (-43.48%)
- **Yesterday-to-today P&L:** `+$56.74`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **LLY** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $308.65 | $298.01 | $15,794.53 | 🔴 $-564.01 | -3.45% |
| **AMZN** | STOCK | 24.00 | $243.35 | $244.39 | $5,865.36 | 🟢 +$24.84 | +0.43% |
| **AVGO** | STOCK | 7.0000 | $381.66 | $411.35 | $2,879.45 | 🟢 +$207.85 | +7.78% |
| **BTC/USD** | CRYPTO | 0.1168 | $66,185.45 | $63,262.95 | $7,387.32 | 🔴 $-341.26 | -4.42% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,704.97 | $1,069.43 | 🔴 $-261.76 | -19.66% |
| **GOOGL** | STOCK | 9.0000 | $362.27 | $368.03 | $3,312.27 | 🟢 +$51.83 | +1.59% |
| **LLY** | STOCK | 9.0000 | $1,131.88 | $1,098.57 | $9,887.13 | 🔴 $-299.82 | -2.94% |
| **META** | STOCK | 12.00 | $588.59 | $577.22 | $6,926.64 | 🔴 $-136.42 | -1.93% |
| **MSFT** | STOCK | 20.00 | $415.30 | $379.40 | $7,588.00 | 🔴 $-718.05 | -8.64% |
| **NVDA** | STOCK | 106.00 | $223.07 | $210.69 | $22,333.14 | 🔴 $-1,312.66 | -5.55% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $69.48 | $1,071.30 | 🔴 $-257.08 | -19.35% |
| **SPY** | STOCK | 6.0000 | $745.44 | $746.74 | $4,480.44 | 🟢 +$7.78 | +0.17% |
| **TSLA** | STOCK | 24.00 | $432.23 | $400.49 | $9,611.76 | 🔴 $-761.81 | -7.34% |
| **VTI** | ETF | 6.0000 | $367.86 | $369.99 | $2,219.94 | 🟢 +$12.81 | +0.58% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $210.69 | 🟢 +2.95% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $368.03 | 🟢 +1.17% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $298.01 | 🟢 +0.70% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $379.40 | 🟢 +0.13% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $244.39 | 🟢 +2.90% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $369.99 | 🟢 +1.16% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $411.35 | 🟢 +4.70% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $577.22 | 🟢 +1.70% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,307.61 | 🟢 +0.68% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,098.57 | 🔴 -1.21% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 70% | Extreme gain today (+2.95%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.17%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.70%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.13%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 70% | Extreme gain today (+2.90%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.16%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 78% | Extreme gain today (+4.70%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.70%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.68%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 75% | Moderate negative momentum (-1.21%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
