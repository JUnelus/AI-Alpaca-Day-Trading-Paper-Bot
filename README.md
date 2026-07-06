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

> 🕐 **Last updated:** 2026-07-06 14:45 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$96,075.22` |
| 💸 Cash Available    | `$-31,777.04` |
| 🧾 Buying Power      | `$179,665.56` |
| 🔴 Total P&L | `$-2,653.02` &nbsp; `(-26.53%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-2,653.02` (-26.53%)
- **Yesterday-to-today P&L:** `+$486.77`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **MSFT** | BUY | 97% | DCA buy: quality asset on a deep pullback |
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $305.99 | $311.56 | $14,954.88 | 🟢 +$267.32 | +1.82% |
| **AMZN** | STOCK | 28.00 | $237.74 | $242.83 | $6,799.29 | 🟢 +$142.65 | +2.14% |
| **AVGO** | STOCK | 14.00 | $377.43 | $378.03 | $5,292.42 | 🟢 +$8.38 | +0.16% |
| **BTC/USD** | CRYPTO | 0.2032 | $63,872.65 | $62,020.29 | $12,600.27 | 🔴 $-376.33 | -2.90% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,751.00 | $1,098.30 | 🔴 $-232.89 | -17.50% |
| **GOOGL** | STOCK | 16.00 | $352.54 | $361.24 | $5,779.76 | 🟢 +$139.16 | +2.47% |
| **LLY** | STOCK | 14.00 | $1,143.08 | $1,200.26 | $16,803.68 | 🟢 +$800.58 | +5.00% |
| **META** | STOCK | 18.00 | $572.09 | $587.50 | $10,575.09 | 🟢 +$277.50 | +2.69% |
| **MSFT** | STOCK | 22.00 | $393.63 | $384.40 | $8,456.80 | 🔴 $-203.11 | -2.35% |
| **NVDA** | STOCK | 132.00 | $217.83 | $196.62 | $25,953.18 | 🔴 $-2,800.92 | -9.74% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $80.48 | $1,240.89 | 🔴 $-87.49 | -6.59% |
| **SPY** | STOCK | 6.0000 | $745.44 | $749.71 | $4,498.26 | 🟢 +$25.60 | +0.57% |
| **TSLA** | STOCK | 24.00 | $432.23 | $404.42 | $9,706.08 | 🔴 $-667.49 | -6.43% |
| **VTI** | ETF | 11.00 | $366.18 | $371.09 | $4,081.99 | 🟢 +$54.03 | +1.34% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $196.55 | 🟢 +0.88% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $311.40 | 🟢 +0.90% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $361.29 | 🟢 +0.38% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $384.13 | 🔴 -1.63% | **BUY** | 97% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $242.74 | 🟢 +0.03% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $371.10 | 🟢 +0.63% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $377.88 | 🟢 +4.84% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $587.12 | 🟢 +0.72% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,976.92 | 🔴 -2.54% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,200.22 | 🔴 -1.13% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+0.88%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.90%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.38%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.63%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.03%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.63%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 78% | Extreme gain today (+4.84%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.72%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 68% | Extreme loss today (-2.54%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 75% | Moderate negative momentum (-1.13%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
