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

> 🕐 **Last updated:** 2026-06-17 21:54 UTC &nbsp;|&nbsp; **Trades today:** 10 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,696.94` |
| 💸 Cash Available    | `$-1,528.62` |
| 🧾 Buying Power      | `$223,324.34` |
| 🔴 Total P&L | `$-5,189.74` &nbsp; `(-51.90%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,189.74` (-51.90%)
- **Yesterday-to-today P&L:** `$-1,200.16`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AAPL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **VTI** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 82% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $308.82 | $297.35 | $15,462.20 | 🔴 $-596.21 | -3.71% |
| **AMZN** | STOCK | 22.00 | $243.75 | $238.50 | $5,247.00 | 🔴 $-115.43 | -2.15% |
| **AVGO** | STOCK | 10.00 | $391.54 | $395.50 | $3,954.99 | 🟢 +$39.56 | +1.01% |
| **BTC/USD** | CRYPTO | 0.0661 | $68,661.89 | $64,215.68 | $4,242.37 | 🔴 $-293.74 | -6.48% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,738.96 | $1,090.74 | 🔴 $-240.45 | -18.06% |
| **GOOGL** | STOCK | 8.0000 | $361.73 | $364.30 | $2,914.40 | 🟢 +$20.59 | +0.71% |
| **LLY** | STOCK | 7.0000 | $1,137.97 | $1,112.26 | $7,785.82 | 🔴 $-179.95 | -2.26% |
| **META** | STOCK | 11.00 | $589.78 | $573.50 | $6,308.50 | 🔴 $-179.06 | -2.76% |
| **MSFT** | STOCK | 19.00 | $417.25 | $380.94 | $7,237.86 | 🔴 $-689.89 | -8.70% |
| **NVDA** | STOCK | 104.00 | $223.38 | $205.35 | $21,356.40 | 🔴 $-1,874.66 | -8.07% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $72.03 | $1,110.63 | 🔴 $-217.75 | -16.39% |
| **SPY** | STOCK | 6.0000 | $745.44 | $742.75 | $4,456.50 | 🔴 $-16.16 | -0.36% |
| **TSLA** | STOCK | 24.00 | $432.23 | $397.05 | $9,529.20 | 🔴 $-844.37 | -8.14% |
| **VTI** | ETF | 5.0000 | $367.42 | $366.97 | $1,834.85 | 🔴 $-2.23 | -0.12% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $204.65 | 🔴 -1.33% | **BUY** | 85% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $363.79 | 🔴 -2.53% | **BUY** | 100% |
| 3 | **AAPL** | Apple Inc. | STOCK | $295.95 | 🔴 -1.10% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $378.91 | 🔴 -3.79% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $237.50 | 🔴 -3.46% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.76 | 🔴 -1.24% | **BUY** | 85% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $392.90 | 🟢 +4.30% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $567.58 | 🔴 -5.44% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,220.52 | 🔴 -2.11% | **BUY** | 99% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,112.00 | 🔴 -0.94% | **BUY** | 82% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Moderate negative momentum (-1.33%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 68% | Extreme loss today (-2.53%) — mean reversion pullback likely |
| 3 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.10%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 74% | Extreme loss today (-3.79%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 72% | Extreme loss today (-3.46%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 75% | Moderate negative momentum (-1.24%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 76% | Extreme gain today (+4.30%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 78% | Extreme loss today (-5.44%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.11%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 73% | Moderate negative momentum (-0.94%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
