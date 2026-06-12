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

> 🕐 **Last updated:** 2026-06-12 21:52 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,463.49` |
| 💸 Cash Available    | `$7,285.01` |
| 🧾 Buying Power      | `$241,016.65` |
| 🔴 Total P&L | `$-5,481.19` &nbsp; `(-54.81%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,481.19` (-54.81%)
- **Yesterday-to-today P&L:** `$-207.28`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 82% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 51.00 | $309.13 | $291.17 | $14,849.67 | 🔴 $-915.86 | -5.81% |
| **AMZN** | STOCK | 18.00 | $243.73 | $238.58 | $4,294.47 | 🔴 $-92.73 | -2.11% |
| **AVGO** | STOCK | 10.00 | $393.10 | $381.80 | $3,818.00 | 🔴 $-112.95 | -2.87% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $63,389.49 | $1,619.58 | 🔴 $-269.91 | -14.28% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,663.04 | $1,043.13 | 🔴 $-288.07 | -21.64% |
| **GOOGL** | STOCK | 7.0000 | $361.34 | $360.15 | $2,521.05 | 🔴 $-8.30 | -0.33% |
| **LLY** | STOCK | 3.0000 | $1,151.56 | $1,134.80 | $3,404.40 | 🔴 $-50.29 | -1.46% |
| **META** | STOCK | 14.00 | $596.84 | $567.44 | $7,944.09 | 🔴 $-411.68 | -4.93% |
| **MSFT** | STOCK | 16.00 | $422.42 | $390.42 | $6,246.72 | 🔴 $-511.94 | -7.57% |
| **NVDA** | STOCK | 100.00 | $223.97 | $205.31 | $20,531.13 | 🔴 $-1,866.26 | -8.33% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $66.74 | $1,029.05 | 🔴 $-299.33 | -22.53% |
| **SPY** | STOCK | 6.0000 | $745.44 | $742.20 | $4,453.20 | 🔴 $-19.46 | -0.44% |
| **TSLA** | STOCK | 24.00 | $432.23 | $405.74 | $9,737.76 | 🔴 $-635.81 | -6.13% |
| **VTI** | ETF | 4.0000 | $366.61 | $366.96 | $1,467.82 | 🟢 +$1.39 | +0.09% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $205.19 | 🟢 +0.16% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $359.68 | 🟢 +0.53% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $291.13 | 🔴 -1.52% | **BUY** | 96% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $390.74 | 🟢 +0.10% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $238.55 | 🔴 -1.23% | **BUY** | 85% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $366.36 | 🟢 +0.57% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $382.07 | 🔴 -0.91% | **BUY** | 82% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $566.98 | 🔴 -0.26% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,410.59 | 🔴 -0.24% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,133.00 | 🔴 -2.41% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.16%) — no trend to carry forward |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.53%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **SELL** | 84% | Moderate negative momentum (-1.52%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.10%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Moderate negative momentum (-1.23%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.57%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 72% | Moderate negative momentum (-0.91%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.26%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.24%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.41%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
