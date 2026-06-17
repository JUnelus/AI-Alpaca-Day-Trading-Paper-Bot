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

> 🕐 **Last updated:** 2026-06-17 14:42 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,476.12` |
| 💸 Cash Available    | `$265.33` |
| 🧾 Buying Power      | `$230,449.25` |
| 🔴 Total P&L | `$-4,402.59` &nbsp; `(-44.03%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-4,402.59` (-44.03%)
- **Yesterday-to-today P&L:** `$-413.01`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 80% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 75% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $308.82 | $299.50 | $15,574.00 | 🔴 $-484.41 | -3.02% |
| **AMZN** | STOCK | 22.00 | $243.75 | $241.23 | $5,307.10 | 🔴 $-55.33 | -1.03% |
| **AVGO** | STOCK | 13.00 | $391.54 | $394.77 | $5,132.01 | 🟢 +$41.96 | +0.82% |
| **BTC/USD** | CRYPTO | 0.0579 | $69,289.20 | $65,031.97 | $3,764.37 | 🔴 $-246.43 | -6.14% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,751.03 | $1,098.32 | 🔴 $-232.88 | -17.49% |
| **GOOGL** | STOCK | 7.0000 | $361.34 | $364.43 | $2,550.97 | 🟢 +$21.63 | +0.85% |
| **LLY** | STOCK | 6.0000 | $1,141.28 | $1,117.62 | $6,705.69 | 🔴 $-142.01 | -2.07% |
| **META** | STOCK | 10.00 | $590.48 | $582.70 | $5,827.00 | 🔴 $-77.81 | -1.32% |
| **MSFT** | STOCK | 18.00 | $418.96 | $386.38 | $6,954.84 | 🔴 $-586.52 | -7.78% |
| **NVDA** | STOCK | 104.00 | $223.38 | $207.13 | $21,541.52 | 🔴 $-1,689.54 | -7.27% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $72.11 | $1,111.80 | 🔴 $-216.58 | -16.30% |
| **SPY** | STOCK | 6.0000 | $745.44 | $750.00 | $4,500.00 | 🟢 +$27.34 | +0.61% |
| **TSLA** | STOCK | 24.00 | $432.23 | $399.86 | $9,596.52 | 🔴 $-777.05 | -7.49% |
| **VTI** | ETF | 5.0000 | $367.42 | $370.42 | $1,852.10 | 🟢 +$15.02 | +0.82% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $206.94 | 🔴 -0.23% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $364.43 | 🔴 -2.36% | **BUY** | 100% |
| 3 | **AAPL** | Apple Inc. | STOCK | $299.11 | 🔴 -0.05% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $386.03 | 🔴 -1.98% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $240.87 | 🔴 -2.09% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $370.33 | 🔴 -0.01% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $394.72 | 🟢 +4.78% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $582.55 | 🔴 -2.94% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $65,010.60 | 🔴 -0.91% | **BUY** | 80% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,116.97 | 🔴 -0.49% | **BUY** | 75% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.23%) — no trend to carry forward |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 85% | Moderate negative momentum (-2.36%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.05%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.98%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.09%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.01%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 78% | Extreme gain today (+4.78%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 70% | Extreme loss today (-2.94%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 71% | Moderate negative momentum (-0.91%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 66% | Moderate negative momentum (-0.49%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
