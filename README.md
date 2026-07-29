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

> 🕐 **Last updated:** 2026-07-29 21:32 UTC &nbsp;|&nbsp; **Trades today:** 8 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$91,253.25` |
| 💸 Cash Available    | `$-83,572.99` |
| 🧾 Buying Power      | `$89,806.06` |
| 🟢 Total P&L | `+$7,114.30` &nbsp; `(+71.14%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$7,114.30` (+71.14%)
- **Yesterday-to-today P&L:** `$-4,163.20`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 78% | DCA buy: quality asset on a mild dip |
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 98% | DCA buy: quality asset on a deep pullback |
| **VTI** | BUY | 94% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 81% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $339.30 | $17,982.90 | 🟢 +$1,709.03 | +10.50% |
| **AMZN** | STOCK | 60.00 | $239.24 | $225.30 | $13,518.00 | 🔴 $-836.38 | -5.83% |
| **AVGO** | STOCK | 19.00 | $379.17 | $366.85 | $6,970.15 | 🔴 $-234.17 | -3.25% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $63,364.40 | $17,601.15 | 🟢 +$12,355.39 | +235.53% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,884.99 | $1,182.34 | 🟢 +$1,182.34 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $331.51 | $9,282.28 | 🔴 $-601.69 | -6.09% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,210.11 | $32,672.97 | 🟢 +$1,300.94 | +4.15% |
| **META** | STOCK | 25.00 | $600.83 | $527.95 | $13,198.75 | 🔴 $-1,822.09 | -12.13% |
| **MSFT** | STOCK | 33.00 | $391.33 | $401.17 | $13,238.63 | 🟢 +$324.66 | +2.51% |
| **NVDA** | STOCK | 155.00 | $214.59 | $189.84 | $29,425.23 | 🔴 $-3,835.48 | -11.53% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $72.41 | $1,116.53 | 🟢 +$1,116.53 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $728.10 | $4,368.60 | 🔴 $-104.06 | -2.33% |
| **TSLA** | STOCK | 24.00 | $432.23 | $294.70 | $7,072.80 | 🔴 $-3,300.77 | -31.82% |
| **VTI** | ETF | 20.00 | $367.07 | $360.08 | $7,201.53 | 🔴 $-139.94 | -1.91% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $338.19 | 🔴 -0.56% | **BUY** | 78% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $190.01 | 🔴 -3.55% | **BUY** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $336.71 | 🟢 +0.90% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $390.54 | 🔴 -0.71% | **BUY** | 81% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $226.65 | 🔴 -1.82% | **BUY** | 98% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $360.42 | 🔴 -1.52% | **BUY** | 94% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $370.32 | 🔴 -2.78% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $585.61 | 🔴 -1.31% | **BUY** | 85% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,481.58 | 🔴 -0.57% | **BUY** | 75% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,210.02 | 🔴 -0.87% | **BUY** | 81% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 68% | Moderate negative momentum (-0.56%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 73% | Extreme loss today (-3.55%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.90%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 71% | Moderate negative momentum (-0.71%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-1.82%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 83% | Moderate negative momentum (-1.52%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 69% | Extreme loss today (-2.78%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 75% | Moderate negative momentum (-1.31%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 66% | Moderate negative momentum (-0.57%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 72% | Moderate negative momentum (-0.87%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
