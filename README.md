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

> 🕐 **Last updated:** 2026-08-18 13:59 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$102,670.23` |
| 💸 Cash Available    | `$-104,856.45` |
| 🧾 Buying Power      | `$90,140.27` |
| 🟢 Total P&L | `+$16,465.91` &nbsp; `(+164.66%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$16,465.91` (+164.66%)
- **Yesterday-to-today P&L:** `$-687.30`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 74% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $307.06 | $20,572.69 | 🔴 $-26.65 | -0.13% |
| **AMZN** | STOCK | 47.00 | $247.07 | $258.01 | $12,126.36 | 🟢 +$514.22 | +4.43% |
| **AVGO** | STOCK | 14.00 | $389.31 | $379.42 | $5,311.88 | 🔴 $-138.40 | -2.54% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $64,190.30 | $19,924.34 | 🟢 +$12,580.48 | +171.31% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,895.58 | $1,188.98 | 🟢 +$1,188.98 | 0.00% |
| **GOOGL** | STOCK | 27.00 | $352.92 | $341.99 | $9,233.73 | 🔴 $-295.03 | -3.10% |
| **LLY** | STOCK | 41.00 | $1,168.10 | $1,211.91 | $49,688.31 | 🟢 +$1,796.13 | +3.75% |
| **META** | STOCK | 31.00 | $594.44 | $547.80 | $16,981.96 | 🔴 $-1,445.60 | -7.84% |
| **MSFT** | STOCK | 30.00 | $412.13 | $479.64 | $14,389.20 | 🟢 +$2,025.42 | +16.38% |
| **NVDA** | STOCK | 161.00 | $214.48 | $220.19 | $35,450.91 | 🟢 +$919.57 | +2.66% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.82 | $1,169.04 | 🟢 +$1,169.04 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $768.45 | $4,610.70 | 🟢 +$138.04 | +3.09% |
| **TSLA** | STOCK | 24.00 | $432.23 | $339.17 | $8,139.96 | 🔴 $-2,233.61 | -21.53% |
| **VTI** | ETF | 23.00 | $368.05 | $379.94 | $8,738.50 | 🟢 +$273.32 | +3.23% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $220.10 | 🔴 -2.18% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $307.31 | 🟢 +0.56% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $342.09 | 🔴 -0.56% | **BUY** | 77% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $479.58 | 🔴 -0.16% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $257.94 | 🔴 -1.29% | **BUY** | 85% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $380.02 | 🔴 -0.55% | **BUY** | 76% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $379.43 | 🔴 -3.31% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $548.79 | 🔴 -3.55% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,153.13 | 🔴 -0.52% | **BUY** | 74% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,214.87 | 🟢 +2.68% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-2.18%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.56%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 68% | Moderate negative momentum (-0.56%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.16%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Moderate negative momentum (-1.29%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 67% | Moderate negative momentum (-0.55%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 72% | Extreme loss today (-3.31%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 73% | Extreme loss today (-3.55%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 65% | Moderate negative momentum (-0.52%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 68% | Extreme gain today (+2.68%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
