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

> 🕐 **Last updated:** 2026-07-27 21:38 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,649.09` |
| 💸 Cash Available    | `$-78,953.13` |
| 🧾 Buying Power      | `$106,416.22` |
| 🟢 Total P&L | `+$10,504.49` &nbsp; `(+105.04%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$10,504.49` (+105.04%)
- **Yesterday-to-today P&L:** `$-715.15`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 79% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $336.52 | $17,835.56 | 🟢 +$1,561.69 | +9.60% |
| **AMZN** | STOCK | 54.00 | $240.34 | $231.64 | $12,508.56 | 🔴 $-470.03 | -3.62% |
| **AVGO** | STOCK | 16.00 | $379.76 | $383.42 | $6,134.76 | 🟢 +$58.61 | +0.96% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $64,773.60 | $17,992.60 | 🟢 +$12,746.83 | +242.99% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,944.50 | $1,219.67 | 🟢 +$1,219.67 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $327.55 | $9,171.40 | 🔴 $-712.57 | -7.21% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,195.81 | $32,286.87 | 🟢 +$914.84 | +2.92% |
| **META** | STOCK | 24.00 | $601.30 | $595.60 | $14,294.40 | 🔴 $-136.72 | -0.95% |
| **MSFT** | STOCK | 33.00 | $391.33 | $389.14 | $12,841.65 | 🔴 $-72.32 | -0.56% |
| **NVDA** | STOCK | 149.00 | $215.42 | $197.04 | $29,358.96 | 🔴 $-2,738.67 | -8.53% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.98 | $1,171.46 | 🟢 +$1,171.46 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $739.50 | $4,437.00 | 🔴 $-35.66 | -0.80% |
| **TSLA** | STOCK | 24.00 | $432.23 | $308.63 | $7,407.12 | 🔴 $-2,966.45 | -28.60% |
| **VTI** | ETF | 19.00 | $367.28 | $365.38 | $6,942.22 | 🔴 $-36.17 | -0.52% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $336.91 | 🟢 +1.17% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $196.51 | 🔴 -4.99% | **BUY** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $326.56 | 🟢 +2.13% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $389.10 | 🟢 +1.94% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $231.39 | 🔴 -0.31% | **BUY** | 73% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.18 | 🟢 +0.10% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $383.22 | 🟢 +0.34% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $593.87 | 🔴 -0.22% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,787.82 | 🔴 -0.84% | **BUY** | 79% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,197.53 | 🟢 +0.13% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.17%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 78% | Extreme loss today (-4.99%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+2.13%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.94%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.31%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.10%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (+0.34%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.22%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 70% | Moderate negative momentum (-0.84%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.13%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
