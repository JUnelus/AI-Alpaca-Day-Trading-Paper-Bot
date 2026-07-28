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

> 🕐 **Last updated:** 2026-07-28 14:33 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,348.56` |
| 💸 Cash Available    | `$-79,806.35` |
| 🧾 Buying Power      | `$105,865.80` |
| 🟢 Total P&L | `+$10,203.98` &nbsp; `(+102.04%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$10,203.98` (+102.04%)
- **Yesterday-to-today P&L:** `$-300.51`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 81% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $338.56 | $17,943.68 | 🟢 +$1,669.81 | +10.26% |
| **AMZN** | STOCK | 56.00 | $240.02 | $229.07 | $12,827.92 | 🔴 $-613.14 | -4.56% |
| **AVGO** | STOCK | 16.00 | $379.76 | $374.87 | $5,997.92 | 🔴 $-78.23 | -1.29% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $63,094.70 | $17,526.24 | 🟢 +$12,280.47 | +234.10% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,876.37 | $1,176.93 | 🟢 +$1,176.93 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $327.91 | $9,181.48 | 🔴 $-702.49 | -7.11% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,226.82 | $33,124.14 | 🟢 +$1,752.11 | +5.58% |
| **META** | STOCK | 24.00 | $601.30 | $593.07 | $14,233.56 | 🔴 $-197.56 | -1.37% |
| **MSFT** | STOCK | 33.00 | $391.33 | $395.16 | $13,040.28 | 🟢 +$126.31 | +0.98% |
| **NVDA** | STOCK | 151.00 | $215.15 | $194.56 | $29,379.31 | 🔴 $-3,109.06 | -9.57% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $72.88 | $1,123.79 | 🟢 +$1,123.79 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $737.48 | $4,424.88 | 🔴 $-47.78 | -1.07% |
| **TSLA** | STOCK | 24.00 | $432.23 | $302.33 | $7,255.92 | 🔴 $-3,117.65 | -30.05% |
| **VTI** | ETF | 19.00 | $367.28 | $364.15 | $6,918.85 | 🔴 $-59.54 | -0.85% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $338.48 | 🟢 +0.47% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $194.47 | 🔴 -1.04% | **BUY** | 85% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $327.89 | 🟢 +0.41% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $395.19 | 🟢 +1.57% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $228.85 | 🔴 -1.10% | **BUY** | 85% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $364.22 | 🔴 -0.26% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $375.51 | 🔴 -2.01% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $593.57 | 🔴 -0.05% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,104.89 | 🔴 -0.94% | **BUY** | 81% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,226.65 | 🟢 +2.43% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.47%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Moderate negative momentum (-1.04%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.41%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.57%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Moderate negative momentum (-1.10%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.26%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 85% | Moderate negative momentum (-2.01%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.05%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 71% | Moderate negative momentum (-0.94%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+2.43%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
