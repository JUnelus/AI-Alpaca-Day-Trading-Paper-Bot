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

> 🕐 **Last updated:** 2026-06-11 21:54 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,670.79` |
| 💸 Cash Available    | `$11,494.05` |
| 🧾 Buying Power      | `$248,055.83` |
| 🔴 Total P&L | `$-5,273.91` &nbsp; `(-52.74%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,273.91` (-52.74%)
- **Yesterday-to-today P&L:** `+$1,647.36`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **MSFT** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 75% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 50.00 | $309.48 | $295.89 | $14,794.50 | 🔴 $-679.55 | -4.39% |
| **AMZN** | STOCK | 16.00 | $244.72 | $241.45 | $3,863.20 | 🔴 $-52.24 | -1.33% |
| **AVGO** | STOCK | 9.0000 | $394.67 | $384.21 | $3,457.91 | 🔴 $-94.08 | -2.65% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $63,500.60 | $1,622.41 | 🔴 $-267.07 | -14.13% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,678.24 | $1,052.66 | 🔴 $-278.53 | -20.92% |
| **GOOGL** | STOCK | 7.0000 | $361.34 | $358.58 | $2,510.06 | 🔴 $-19.29 | -0.76% |
| **LLY** | STOCK | 2.0000 | $1,150.72 | $1,159.00 | $2,318.00 | 🟢 +$16.55 | +0.72% |
| **META** | STOCK | 12.00 | $601.28 | $571.74 | $6,860.88 | 🔴 $-354.43 | -4.91% |
| **MSFT** | STOCK | 14.00 | $427.54 | $391.32 | $5,478.48 | 🔴 $-507.05 | -8.47% |
| **NVDA** | STOCK | 100.00 | $223.97 | $205.16 | $20,515.86 | 🔴 $-1,881.53 | -8.40% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $67.16 | $1,035.58 | 🔴 $-292.80 | -22.04% |
| **SPY** | STOCK | 6.0000 | $745.44 | $737.88 | $4,427.28 | 🔴 $-45.38 | -1.01% |
| **TSLA** | STOCK | 24.00 | $432.23 | $398.48 | $9,563.49 | 🔴 $-810.08 | -7.81% |
| **VTI** | ETF | 4.0000 | $366.61 | $364.50 | $1,458.00 | 🔴 $-8.43 | -0.57% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $204.87 | 🟢 +2.22% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $357.77 | 🟢 +0.39% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $295.63 | 🟢 +1.39% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $390.34 | 🔴 -1.77% | **BUY** | 99% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $241.51 | 🟢 +1.47% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $364.30 | 🟢 +1.75% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $385.57 | 🟢 +3.62% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $568.43 | 🔴 -0.45% | **BUY** | 75% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,489.94 | 🟢 +3.32% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,160.95 | 🟢 +2.16% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+2.22%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.39%) — no trend to carry forward |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.39%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.77%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.47%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.75%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 73% | Extreme gain today (+3.62%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 66% | Moderate negative momentum (-0.45%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 72% | Extreme gain today (+3.32%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+2.16%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
