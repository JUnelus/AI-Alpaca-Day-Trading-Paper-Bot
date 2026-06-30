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

> 🕐 **Last updated:** 2026-06-30 21:46 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,500.02` |
| 💸 Cash Available    | `$-26,043.28` |
| 🧾 Buying Power      | `$183,014.00` |
| 🔴 Total P&L | `$-5,265.04` &nbsp; `(-52.65%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,265.04` (-52.65%)
- **Yesterday-to-today P&L:** `+$988.57`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AMZN** | BUY | 80% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $305.99 | $289.00 | $17,340.00 | 🔴 $-1,019.46 | -5.55% |
| **AMZN** | STOCK | 26.00 | $237.67 | $239.07 | $6,215.82 | 🟢 +$36.52 | +0.59% |
| **AVGO** | STOCK | 9.0000 | $380.51 | $377.13 | $3,394.17 | 🔴 $-30.42 | -0.89% |
| **BTC/USD** | CRYPTO | 0.1947 | $63,959.82 | $58,565.70 | $11,401.86 | 🔴 $-1,050.15 | -8.43% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,568.12 | $983.59 | 🔴 $-347.60 | -26.11% |
| **GOOGL** | STOCK | 13.00 | $353.61 | $356.76 | $4,637.88 | 🟢 +$40.97 | +0.89% |
| **LLY** | STOCK | 11.00 | $1,128.48 | $1,200.35 | $13,203.85 | 🟢 +$790.53 | +6.37% |
| **META** | STOCK | 18.00 | $577.11 | $562.69 | $10,128.42 | 🔴 $-259.56 | -2.50% |
| **MSFT** | STOCK | 22.00 | $393.63 | $374.50 | $8,239.00 | 🔴 $-420.91 | -4.86% |
| **NVDA** | STOCK | 122.00 | $219.68 | $199.24 | $24,307.28 | 🔴 $-2,493.83 | -9.30% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $73.12 | $1,127.44 | 🔴 $-200.94 | -15.13% |
| **SPY** | STOCK | 6.0000 | $745.44 | $745.81 | $4,474.86 | 🟢 +$2.20 | +0.05% |
| **TSLA** | STOCK | 24.00 | $432.23 | $417.63 | $10,023.10 | 🔴 $-350.47 | -3.38% |
| **VTI** | ETF | 11.00 | $366.18 | $369.64 | $4,066.04 | 🟢 +$38.08 | +0.95% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $200.09 | 🟢 +2.63% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $357.37 | 🟢 +1.05% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $289.36 | 🟢 +2.70% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $373.02 | 🟢 +1.21% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $238.34 | 🔴 -0.75% | **BUY** | 80% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $370.04 | 🟢 +0.80% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $377.75 | 🟢 +1.42% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $563.29 | 🟢 +0.12% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $58,498.71 | 🔴 -2.77% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,199.43 | 🔴 -2.48% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 68% | Extreme gain today (+2.63%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.05%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **SELL** | 69% | Extreme gain today (+2.70%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.21%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 71% | Moderate negative momentum (-0.75%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.80%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.42%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.12%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 69% | Extreme loss today (-2.77%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.48%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
