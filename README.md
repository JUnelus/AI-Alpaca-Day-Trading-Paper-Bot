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

> 🕐 **Last updated:** 2026-07-23 21:36 UTC &nbsp;|&nbsp; **Trades today:** 0 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,599.04` |
| 💸 Cash Available    | `$-75,035.14` |
| 🧾 Buying Power      | `$0.00` |
| 🟢 Total P&L | `+$11,454.43` &nbsp; `(+114.54%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$11,454.43` (+114.54%)
- **Yesterday-to-today P&L:** `$-2,521.48`
- **Executed today:** No buy/sell orders were approved in this run.

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $320.73 | $16,998.67 | 🟢 +$724.79 | +4.45% |
| **AMZN** | STOCK | 50.00 | $240.90 | $234.53 | $11,726.40 | 🔴 $-318.43 | -2.64% |
| **AVGO** | STOCK | 13.00 | $379.10 | $392.48 | $5,102.24 | 🟢 +$173.89 | +3.53% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $65,007.14 | $18,057.47 | 🟢 +$12,811.70 | +244.23% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,880.11 | $1,179.28 | 🟢 +$1,179.28 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $318.70 | $8,923.60 | 🔴 $-960.37 | -9.72% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,184.79 | $31,989.33 | 🟢 +$617.30 | +1.97% |
| **META** | STOCK | 23.00 | $600.93 | $605.71 | $13,931.33 | 🟢 +$109.93 | +0.80% |
| **MSFT** | STOCK | 33.00 | $391.33 | $383.11 | $12,642.63 | 🔴 $-271.34 | -2.10% |
| **NVDA** | STOCK | 143.00 | $215.88 | $208.36 | $29,795.37 | 🔴 $-1,075.58 | -3.48% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.93 | $1,170.76 | 🟢 +$1,170.76 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $738.72 | $4,432.33 | 🔴 $-40.33 | -0.90% |
| **TSLA** | STOCK | 24.00 | $432.23 | $322.77 | $7,746.48 | 🔴 $-2,627.09 | -25.32% |
| **VTI** | ETF | 19.00 | $367.28 | $365.17 | $6,938.31 | 🔴 $-40.08 | -0.57% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.76 | 🔴 -1.56% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $321.66 | 🔴 -1.30% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $317.69 | 🔴 -7.13% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $381.58 | 🔴 -2.24% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $233.66 | 🔴 -4.57% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $364.69 | 🔴 -1.13% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $392.47 | 🔴 -1.09% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $606.10 | 🔴 -3.36% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $65,062.10 | 🔴 -1.54% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,185.87 | 🟢 +1.97% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 84% | Moderate negative momentum (-1.56%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.30%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 78% | Extreme loss today (-7.13%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-2.24%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 78% | Extreme loss today (-4.57%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 75% | Moderate negative momentum (-1.13%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 75% | Moderate negative momentum (-1.09%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 72% | Extreme loss today (-3.36%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 81% | Moderate negative momentum (-1.54%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.97%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
