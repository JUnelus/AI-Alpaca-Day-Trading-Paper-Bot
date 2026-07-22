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

> 🕐 **Last updated:** 2026-07-22 21:38 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,120.45` |
| 💸 Cash Available    | `$-75,035.14` |
| 🧾 Buying Power      | `$116,512.22` |
| 🟢 Total P&L | `+$13,975.91` &nbsp; `(+139.76%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$13,975.91` (+139.76%)
- **Yesterday-to-today P&L:** `$-1,752.09`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 78% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 78% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 84% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $326.00 | $17,278.00 | 🟢 +$1,004.13 | +6.17% |
| **AMZN** | STOCK | 50.00 | $240.90 | $240.77 | $12,038.53 | 🔴 $-6.29 | -0.05% |
| **AVGO** | STOCK | 13.00 | $379.10 | $398.93 | $5,186.10 | 🟢 +$257.75 | +5.23% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.58 | $65,901.20 | $18,305.82 | 🟢 +$13,060.12 | +248.97% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,929.30 | $1,210.13 | 🟢 +$1,210.13 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $326.02 | $9,128.62 | 🔴 $-755.35 | -7.64% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,164.26 | $31,435.02 | 🟢 +$62.99 | +0.20% |
| **META** | STOCK | 23.00 | $600.93 | $618.12 | $14,216.76 | 🟢 +$395.36 | +2.86% |
| **MSFT** | STOCK | 33.00 | $391.33 | $386.99 | $12,770.67 | 🔴 $-143.30 | -1.11% |
| **NVDA** | STOCK | 143.00 | $215.88 | $211.86 | $30,296.54 | 🔴 $-574.41 | -1.86% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $77.64 | $1,197.11 | 🟢 +$1,197.11 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $746.80 | $4,480.80 | 🟢 +$8.14 | +0.18% |
| **TSLA** | STOCK | 24.00 | $432.23 | $358.50 | $8,604.00 | 🔴 $-1,769.57 | -17.06% |
| **VTI** | ETF | 19.00 | $367.28 | $368.81 | $7,007.48 | 🟢 +$29.09 | +0.42% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $212.06 | 🟢 +2.30% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $325.89 | 🔴 -0.56% | **BUY** | 78% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $342.09 | 🔴 -1.46% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $390.34 | 🔴 -1.86% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $244.85 | 🔴 -1.09% | **BUY** | 85% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.87 | 🔴 -0.16% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $396.81 | 🟢 +2.67% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $627.17 | 🔴 -2.58% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $66,014.30 | 🔴 -0.77% | **BUY** | 78% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,163.01 | 🔴 -1.05% | **BUY** | 84% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+2.30%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 69% | Moderate negative momentum (-0.56%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.46%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.86%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Moderate negative momentum (-1.09%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.16%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 68% | Extreme gain today (+2.67%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 68% | Extreme loss today (-2.58%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 69% | Moderate negative momentum (-0.77%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 74% | Moderate negative momentum (-1.05%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
