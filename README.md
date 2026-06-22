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

> 🕐 **Last updated:** 2026-06-22 21:54 UTC &nbsp;|&nbsp; **Trades today:** 8 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,601.56` |
| 💸 Cash Available    | `$-9,460.50` |
| 🧾 Buying Power      | `$211,084.72` |
| 🔴 Total P&L | `$-5,425.80` &nbsp; `(-54.26%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,425.80` (-54.26%)
- **Yesterday-to-today P&L:** `$-1,046.95`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **VTI** | BUY | 72% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $308.65 | $296.30 | $15,703.90 | 🔴 $-654.64 | -4.00% |
| **AMZN** | STOCK | 26.00 | $242.59 | $233.75 | $6,077.47 | 🔴 $-229.79 | -3.64% |
| **AVGO** | STOCK | 2.0000 | $388.64 | $393.28 | $786.56 | 🟢 +$9.27 | +1.19% |
| **BTC/USD** | CRYPTO | 0.1168 | $66,185.45 | $64,200.00 | $7,496.74 | 🔴 $-231.84 | -3.00% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,729.30 | $1,084.69 | 🔴 $-246.51 | -18.52% |
| **GOOGL** | STOCK | 10.00 | $360.54 | $348.70 | $3,487.00 | 🔴 $-118.37 | -3.28% |
| **LLY** | STOCK | 12.00 | $1,126.41 | $1,105.98 | $13,271.76 | 🔴 $-245.16 | -1.81% |
| **META** | STOCK | 13.00 | $586.46 | $563.46 | $7,324.99 | 🔴 $-298.94 | -3.92% |
| **MSFT** | STOCK | 21.00 | $413.20 | $368.45 | $7,737.45 | 🔴 $-939.81 | -10.83% |
| **NVDA** | STOCK | 106.00 | $223.07 | $208.00 | $22,048.00 | 🔴 $-1,597.80 | -6.76% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $72.63 | $1,119.87 | 🔴 $-208.51 | -15.70% |
| **SPY** | STOCK | 6.0000 | $745.44 | $744.53 | $4,467.18 | 🔴 $-5.48 | -0.12% |
| **TSLA** | STOCK | 24.00 | $432.23 | $404.46 | $9,707.04 | 🔴 $-666.53 | -6.43% |
| **VTI** | ETF | 6.0000 | $367.86 | $369.24 | $2,215.44 | 🟢 +$8.31 | +0.38% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.65 | 🔴 -0.97% | **BUY** | 84% |
| 2 | **AAPL** | Apple Inc. | STOCK | $297.01 | 🔴 -0.34% | **BUY** | 74% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $349.68 | 🔴 -4.99% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $367.34 | 🔴 -3.18% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $232.79 | 🔴 -4.75% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.81 | 🔴 -0.32% | **BUY** | 72% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $392.13 | 🔴 -4.67% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $563.85 | 🔴 -2.32% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,179.97 | 🟢 +1.47% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,102.08 | 🟢 +0.32% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 74% | Moderate negative momentum (-0.97%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.34%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 78% | Extreme loss today (-4.99%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 71% | Extreme loss today (-3.18%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 78% | Extreme loss today (-4.75%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.32%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 78% | Extreme loss today (-4.67%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-2.32%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.47%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.32%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
