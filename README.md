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

> 🕐 **Last updated:** 2026-06-22 15:32 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,109.77` |
| 💸 Cash Available    | `$-7,321.12` |
| 🧾 Buying Power      | `$215,746.44` |
| 🔴 Total P&L | `$-4,913.52` &nbsp; `(-49.14%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-4,913.52` (-49.14%)
- **Yesterday-to-today P&L:** `$-534.66`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $308.65 | $299.86 | $15,892.58 | 🔴 $-465.96 | -2.85% |
| **AMZN** | STOCK | 24.00 | $243.35 | $233.35 | $5,600.40 | 🔴 $-240.12 | -4.11% |
| **AVGO** | STOCK | 1.0000 | $381.66 | $395.62 | $395.62 | 🟢 +$13.96 | +3.66% |
| **BTC/USD** | CRYPTO | 0.1168 | $66,185.45 | $64,997.80 | $7,589.90 | 🔴 $-138.68 | -1.79% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,750.75 | $1,098.14 | 🔴 $-233.05 | -17.51% |
| **GOOGL** | STOCK | 9.0000 | $362.27 | $344.88 | $3,103.92 | 🔴 $-156.52 | -4.80% |
| **LLY** | STOCK | 12.00 | $1,126.41 | $1,096.24 | $13,154.94 | 🔴 $-361.98 | -2.68% |
| **META** | STOCK | 12.00 | $588.59 | $560.76 | $6,729.12 | 🔴 $-333.94 | -4.73% |
| **MSFT** | STOCK | 20.00 | $415.30 | $371.17 | $7,423.40 | 🔴 $-882.65 | -10.63% |
| **NVDA** | STOCK | 106.00 | $223.07 | $210.16 | $22,276.96 | 🔴 $-1,368.84 | -5.79% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $73.02 | $1,125.86 | 🔴 $-202.52 | -15.25% |
| **SPY** | STOCK | 6.0000 | $745.44 | $744.45 | $4,466.70 | 🔴 $-5.96 | -0.13% |
| **TSLA** | STOCK | 24.00 | $432.23 | $409.59 | $9,830.16 | 🔴 $-543.41 | -5.24% |
| **VTI** | ETF | 6.0000 | $367.86 | $368.88 | $2,213.28 | 🟢 +$6.15 | +0.28% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $210.14 | 🔴 -0.26% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $299.87 | 🟢 +0.62% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $345.13 | 🔴 -6.22% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $371.10 | 🔴 -2.19% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $233.27 | 🔴 -4.55% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.96 | 🔴 -0.28% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $395.67 | 🔴 -3.81% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $560.81 | 🔴 -2.84% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,956.81 | 🟢 +2.70% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,096.60 | 🔴 -0.18% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.26%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.62%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 78% | Extreme loss today (-6.22%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-2.19%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 78% | Extreme loss today (-4.55%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.28%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 74% | Extreme loss today (-3.81%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 69% | Extreme loss today (-2.84%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 69% | Extreme gain today (+2.70%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.18%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
