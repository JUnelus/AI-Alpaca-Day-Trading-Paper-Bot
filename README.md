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

> 🕐 **Last updated:** 2026-06-12 14:41 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,100.29` |
| 💸 Cash Available    | `$10,531.79` |
| 🧾 Buying Power      | `$243,060.53` |
| 🔴 Total P&L | `$-5,844.48` &nbsp; `(-58.44%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,844.48` (-58.44%)
- **Yesterday-to-today P&L:** `$-570.58`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 94% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 79% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 50.00 | $309.48 | $291.44 | $14,572.00 | 🔴 $-902.05 | -5.83% |
| **AMZN** | STOCK | 17.00 | $244.19 | $235.78 | $4,008.26 | 🔴 $-143.05 | -3.45% |
| **AVGO** | STOCK | 9.0000 | $394.67 | $378.96 | $3,410.64 | 🔴 $-141.35 | -3.98% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $63,680.20 | $1,627.00 | 🔴 $-262.48 | -13.89% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,670.01 | $1,047.49 | 🔴 $-283.70 | -21.31% |
| **GOOGL** | STOCK | 7.0000 | $361.34 | $361.55 | $2,530.85 | 🟢 +$1.50 | +0.06% |
| **LLY** | STOCK | 2.0000 | $1,150.72 | $1,152.74 | $2,305.48 | 🟢 +$4.03 | +0.18% |
| **META** | STOCK | 13.00 | $599.22 | $565.70 | $7,354.03 | 🔴 $-435.86 | -5.60% |
| **MSFT** | STOCK | 15.00 | $424.88 | $385.33 | $5,779.95 | 🔴 $-593.24 | -9.31% |
| **NVDA** | STOCK | 100.00 | $223.97 | $205.05 | $20,505.00 | 🔴 $-1,892.39 | -8.45% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $67.29 | $1,037.53 | 🔴 $-290.85 | -21.90% |
| **SPY** | STOCK | 6.0000 | $745.44 | $739.58 | $4,437.48 | 🔴 $-35.18 | -0.79% |
| **TSLA** | STOCK | 24.00 | $432.23 | $396.17 | $9,507.96 | 🔴 $-865.61 | -8.34% |
| **VTI** | ETF | 4.0000 | $366.61 | $365.55 | $1,462.18 | 🔴 $-4.25 | -0.29% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $205.35 | 🟢 +0.23% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $362.20 | 🟢 +1.24% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $291.59 | 🔴 -1.37% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $385.83 | 🔴 -1.16% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $235.99 | 🔴 -2.29% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.84 | 🟢 +0.42% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $379.61 | 🔴 -1.55% | **BUY** | 94% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $565.94 | 🔴 -0.44% | **BUY** | 75% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,606.36 | 🟢 +0.07% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,152.74 | 🔴 -0.71% | **BUY** | 79% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.23%) — no trend to carry forward |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.24%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.37%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.16%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.29%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.42%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 83% | Moderate negative momentum (-1.55%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 66% | Moderate negative momentum (-0.44%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.07%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 69% | Moderate negative momentum (-0.71%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
