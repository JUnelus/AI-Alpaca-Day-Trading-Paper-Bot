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

> 🕐 **Last updated:** 2026-07-02 21:40 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,184.28` |
| 💸 Cash Available    | `$-29,774.79` |
| 🧾 Buying Power      | `$181,580.41` |
| 🔴 Total P&L | `$-3,583.72` &nbsp; `(-35.84%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-3,583.72` (-35.84%)
- **Yesterday-to-today P&L:** `$-111.66`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AAPL** | SELL | 100% | Take-profit trim after overextended rally |
| **GOOGL** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $305.99 | $308.07 | $18,484.20 | 🟢 +$124.74 | +0.68% |
| **AMZN** | STOCK | 28.00 | $237.74 | $242.75 | $6,797.00 | 🟢 +$140.36 | +2.11% |
| **AVGO** | STOCK | 11.00 | $378.26 | $360.30 | $3,963.30 | 🔴 $-197.55 | -4.75% |
| **BTC/USD** | CRYPTO | 0.1947 | $63,955.48 | $61,415.57 | $11,956.69 | 🔴 $-494.48 | -3.97% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,699.40 | $1,065.93 | 🔴 $-265.26 | -19.93% |
| **GOOGL** | STOCK | 13.00 | $350.09 | $358.91 | $4,665.83 | 🟢 +$114.72 | +2.52% |
| **LLY** | STOCK | 14.00 | $1,143.08 | $1,212.70 | $16,977.80 | 🟢 +$974.70 | +6.09% |
| **META** | STOCK | 15.00 | $571.93 | $583.00 | $8,745.00 | 🟢 +$166.12 | +1.94% |
| **MSFT** | STOCK | 22.00 | $393.63 | $390.28 | $8,586.16 | 🔴 $-73.75 | -0.85% |
| **NVDA** | STOCK | 126.00 | $218.95 | $194.47 | $24,503.22 | 🔴 $-3,084.70 | -11.18% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $81.01 | $1,249.09 | 🔴 $-79.29 | -5.97% |
| **SPY** | STOCK | 6.0000 | $745.44 | $744.42 | $4,466.52 | 🔴 $-6.14 | -0.14% |
| **TSLA** | STOCK | 24.00 | $432.23 | $393.42 | $9,442.08 | 🔴 $-931.49 | -8.98% |
| **VTI** | ETF | 11.00 | $366.18 | $368.75 | $4,056.25 | 🟢 +$28.29 | +0.70% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $194.83 | 🔴 -1.39% | **BUY** | 85% |
| 2 | **AAPL** | Apple Inc. | STOCK | $308.63 | 🟢 +4.84% | **SELL** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $359.91 | 🔴 -0.36% | **BUY** | 74% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $390.49 | 🟢 +1.62% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $242.67 | 🟢 +0.40% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.76 | 🔴 -0.14% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $360.45 | 🔴 -2.41% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $582.90 | 🔴 -4.90% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,466.90 | 🟢 +2.50% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,213.91 | 🟢 +1.86% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Moderate negative momentum (-1.39%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 78% | Extreme gain today (+4.84%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.36%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.62%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.40%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.14%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 85% | Moderate negative momentum (-2.41%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 78% | Extreme loss today (-4.90%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 68% | Extreme gain today (+2.50%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.86%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
