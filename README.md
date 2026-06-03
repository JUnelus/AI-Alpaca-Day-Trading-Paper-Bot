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

> 🕐 **Last updated:** 2026-06-03 22:44 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$96,960.50` |
| 💸 Cash Available    | `$35,767.00` |
| 🧾 Buying Power      | `$125,907.24` |
| 🔴 Total P&L | `$-2,043.11` &nbsp; `(-20.43%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-2,043.11` (-20.43%)
- **Yesterday-to-today P&L:** `$-1,231.60`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AAPL** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **META** | SELL | 100% | Take-profit trim after overextended rally |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $310.82 | $313.53 | $15,049.67 | 🟢 +$130.36 | +0.87% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $64,947.60 | $1,134.10 | 🔴 $-219.29 | -16.20% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,829.00 | $1,147.22 | 🔴 $-183.97 | -13.82% |
| **META** | STOCK | 4.0000 | $612.74 | $619.41 | $2,477.64 | 🟢 +$26.68 | +1.09% |
| **MSFT** | STOCK | 9.0000 | $450.97 | $428.24 | $3,854.15 | 🔴 $-204.61 | -5.04% |
| **NVDA** | STOCK | 96.00 | $225.77 | $213.66 | $20,511.36 | 🔴 $-1,162.15 | -5.36% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $72.38 | $1,116.01 | 🔴 $-212.37 | -15.99% |
| **SPY** | STOCK | 7.0000 | $744.36 | $750.73 | $5,255.11 | 🟢 +$44.61 | +0.86% |
| **TSLA** | STOCK | 24.00 | $432.23 | $421.30 | $10,111.20 | 🔴 $-262.37 | -2.53% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $214.75 | 🔴 -3.62% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $310.26 | 🔴 -1.57% | **BUY** | 96% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $358.99 | 🔴 -0.79% | **BUY** | 81% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $427.34 | 🔴 -3.17% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $250.02 | 🔴 -2.53% | **BUY** | 100% |
| 6 | **AVGO** | Broadcom Inc. | STOCK | $479.23 | 🔴 -0.49% | **BUY** | 75% |
| 7 | **VTI** | Vanguard Total Stock Market ETF | ETF | $371.65 | 🔴 -0.72% | **BUY** | 79% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $622.98 | 🟢 +4.24% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,947.91 | 🔴 -2.55% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,078.78 | 🟢 +1.37% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 73% | Extreme loss today (-3.62%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **SELL** | 85% | Moderate negative momentum (-1.57%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 71% | Moderate negative momentum (-0.79%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 71% | Extreme loss today (-3.17%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 68% | Extreme loss today (-2.53%) — mean reversion pullback likely |
| 6 | **AVGO** | Broadcom Inc. | **SELL** | 66% | Moderate negative momentum (-0.49%) — continuation expected |
| 7 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 70% | Moderate negative momentum (-0.72%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 76% | Extreme gain today (+4.24%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 68% | Extreme loss today (-2.55%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.37%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
