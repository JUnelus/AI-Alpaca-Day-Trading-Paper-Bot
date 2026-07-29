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

> 🕐 **Last updated:** 2026-07-29 14:31 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,178.50` |
| 💸 Cash Available    | `$-81,405.61` |
| 🧾 Buying Power      | `$101,618.34` |
| 🟢 Total P&L | `+$10,038.17` &nbsp; `(+100.38%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$10,038.17` (+100.38%)
- **Yesterday-to-today P&L:** `$-1,239.33`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 80% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 78% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $341.14 | $18,080.16 | 🟢 +$1,806.29 | +11.10% |
| **AMZN** | STOCK | 58.00 | $239.64 | $227.54 | $13,197.61 | 🔴 $-701.59 | -5.05% |
| **AVGO** | STOCK | 18.00 | $379.35 | $376.02 | $6,768.36 | 🔴 $-59.88 | -0.88% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $64,168.50 | $17,824.51 | 🟢 +$12,578.75 | +239.79% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,892.61 | $1,187.12 | 🟢 +$1,187.12 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $332.62 | $9,313.36 | 🔴 $-570.61 | -5.77% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,224.02 | $33,048.40 | 🟢 +$1,676.38 | +5.34% |
| **META** | STOCK | 24.00 | $601.30 | $589.41 | $14,145.84 | 🔴 $-285.28 | -1.98% |
| **MSFT** | STOCK | 33.00 | $391.33 | $393.02 | $12,969.50 | 🟢 +$55.53 | +0.43% |
| **NVDA** | STOCK | 153.00 | $214.88 | $191.68 | $29,326.52 | 🔴 $-3,550.87 | -10.80% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.30 | $1,130.24 | 🟢 +$1,130.24 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $735.07 | $4,410.42 | 🔴 $-62.24 | -1.39% |
| **TSLA** | STOCK | 24.00 | $432.23 | $303.65 | $7,287.60 | 🔴 $-3,085.97 | -29.75% |
| **VTI** | ETF | 19.00 | $367.28 | $363.09 | $6,898.71 | 🔴 $-79.68 | -1.14% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $341.29 | 🟢 +0.36% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $191.83 | 🔴 -2.63% | **BUY** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $332.94 | 🔴 -0.23% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $392.63 | 🔴 -0.18% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $227.80 | 🔴 -1.33% | **BUY** | 85% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $363.17 | 🔴 -0.77% | **BUY** | 80% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $376.10 | 🔴 -1.26% | **BUY** | 85% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $589.76 | 🔴 -0.62% | **BUY** | 78% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,171.82 | 🟢 +0.51% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,223.40 | 🟢 +0.22% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.36%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 68% | Extreme loss today (-2.63%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.23%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.18%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Moderate negative momentum (-1.33%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 70% | Moderate negative momentum (-0.77%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 75% | Moderate negative momentum (-1.26%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 68% | Moderate negative momentum (-0.62%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.51%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.22%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
