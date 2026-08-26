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

> 🕐 **Last updated:** 2026-08-26 14:02 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$107,329.76` |
| 💸 Cash Available    | `$-118,555.69` |
| 🧾 Buying Power      | `$90,342.73` |
| 🟢 Total P&L | `+$19,940.56` &nbsp; `(+199.41%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$19,940.56` (+199.41%)
- **Yesterday-to-today P&L:** `$-1,185.75`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $312.06 | $21,844.20 | 🟢 +$314.59 | +1.46% |
| **AMZN** | STOCK | 60.00 | $249.93 | $260.95 | $15,657.00 | 🟢 +$661.10 | +4.41% |
| **AVGO** | STOCK | 21.00 | $381.57 | $354.40 | $7,442.40 | 🔴 $-570.50 | -7.12% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $78,432.60 | $18,007.73 | 🟢 +$15,759.58 | +701.00% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,457.37 | $1,541.36 | 🟢 +$1,541.36 | 0.00% |
| **GOOGL** | STOCK | 33.00 | $351.11 | $343.57 | $11,337.81 | 🔴 $-248.86 | -2.15% |
| **LLY** | STOCK | 44.00 | $1,178.89 | $1,205.60 | $53,046.40 | 🟢 +$1,175.20 | +2.27% |
| **META** | STOCK | 33.00 | $591.43 | $572.47 | $18,891.51 | 🔴 $-625.68 | -3.21% |
| **MSFT** | STOCK | 32.00 | $416.49 | $494.93 | $15,837.76 | 🟢 +$2,510.13 | +18.83% |
| **NVDA** | STOCK | 178.00 | $214.64 | $212.28 | $37,784.95 | 🔴 $-420.91 | -1.10% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $96.42 | $1,486.76 | 🟢 +$1,486.76 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $766.83 | $4,600.98 | 🟢 +$128.32 | +2.87% |
| **TSLA** | STOCK | 24.00 | $432.23 | $348.25 | $8,358.00 | 🔴 $-2,015.57 | -19.43% |
| **VTI** | ETF | 28.00 | $370.04 | $378.79 | $10,606.24 | 🟢 +$245.04 | +2.36% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $212.21 | 🔴 -0.39% | **BUY** | 74% |
| 2 | **AAPL** | Apple Inc. | STOCK | $312.38 | 🟢 +0.80% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $343.12 | 🔴 -1.11% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $495.06 | 🟢 +0.68% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $260.96 | 🔴 -0.04% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $378.74 | 🟢 +0.16% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $354.19 | 🔴 -0.72% | **BUY** | 79% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $78,479.02 | 🔴 -0.07% | HOLD | — |
| 9 | **META** | Meta Platforms Inc. | STOCK | $572.97 | 🟢 +0.51% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,203.82 | 🔴 -2.42% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.80%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.11%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.68%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.04%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.16%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 70% | Moderate negative momentum (-0.72%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.07%) — no trend to carry forward |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.51%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.42%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
