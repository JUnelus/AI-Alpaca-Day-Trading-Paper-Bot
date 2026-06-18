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

> 🕐 **Last updated:** 2026-06-18 21:55 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,491.24` |
| 💸 Cash Available    | `$-6,447.98` |
| 🧾 Buying Power      | `$220,008.86` |
| 🔴 Total P&L | `$-4,404.51` &nbsp; `(-44.05%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-4,404.51` (-44.05%)
- **Yesterday-to-today P&L:** `+$785.23`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $308.65 | $298.12 | $15,800.36 | 🔴 $-558.18 | -3.41% |
| **AMZN** | STOCK | 24.00 | $243.35 | $243.76 | $5,850.24 | 🟢 +$9.72 | +0.17% |
| **AVGO** | STOCK | 7.0000 | $386.50 | $412.52 | $2,887.64 | 🟢 +$182.12 | +6.73% |
| **BTC/USD** | CRYPTO | 0.1168 | $66,196.92 | $62,897.40 | $7,344.63 | 🔴 $-385.29 | -4.98% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,706.21 | $1,070.21 | 🔴 $-260.99 | -19.61% |
| **GOOGL** | STOCK | 9.0000 | $362.27 | $367.50 | $3,307.50 | 🟢 +$47.06 | +1.44% |
| **LLY** | STOCK | 9.0000 | $1,131.88 | $1,099.89 | $9,899.01 | 🔴 $-287.94 | -2.83% |
| **META** | STOCK | 12.00 | $588.59 | $577.68 | $6,932.16 | 🔴 $-130.90 | -1.85% |
| **MSFT** | STOCK | 20.00 | $415.30 | $379.80 | $7,596.00 | 🔴 $-710.05 | -8.55% |
| **NVDA** | STOCK | 106.00 | $223.07 | $210.80 | $22,345.08 | 🔴 $-1,300.72 | -5.50% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $69.50 | $1,071.60 | 🔴 $-256.78 | -19.33% |
| **SPY** | STOCK | 6.0000 | $745.44 | $747.97 | $4,487.82 | 🟢 +$15.16 | +0.34% |
| **TSLA** | STOCK | 24.00 | $432.23 | $399.59 | $9,590.16 | 🔴 $-783.41 | -7.55% |
| **VTI** | ETF | 6.0000 | $367.86 | $370.47 | $2,222.82 | 🟢 +$15.69 | +0.71% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $210.69 | 🟢 +2.95% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $368.03 | 🟢 +1.17% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $298.01 | 🟢 +0.70% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $379.40 | 🟢 +0.13% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $244.39 | 🟢 +2.90% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $369.99 | 🟢 +1.16% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $411.35 | 🟢 +4.70% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $577.22 | 🟢 +1.70% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,837.21 | 🔴 -2.49% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,098.57 | 🔴 -1.21% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 70% | Extreme gain today (+2.95%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.17%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.70%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.13%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 70% | Extreme gain today (+2.90%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.16%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 78% | Extreme gain today (+4.70%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.70%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.49%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 75% | Moderate negative momentum (-1.21%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
