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

> 🕐 **Last updated:** 2026-07-01 14:39 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,945.27` |
| 💸 Cash Available    | `$-27,731.64` |
| 🧾 Buying Power      | `$183,847.78` |
| 🔴 Total P&L | `$-3,772.24` &nbsp; `(-37.72%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-3,772.24` (-37.72%)
- **Yesterday-to-today P&L:** `+$1,492.80`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 97% | DCA buy: quality asset on a deep pullback |
| **META** | SELL | 100% | Take-profit trim after overextended rally |
| **LLY** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $305.99 | $293.44 | $17,606.10 | 🔴 $-753.36 | -4.10% |
| **AMZN** | STOCK | 28.00 | $237.74 | $241.53 | $6,762.84 | 🟢 +$106.20 | +1.60% |
| **AVGO** | STOCK | 9.0000 | $380.51 | $370.79 | $3,337.11 | 🔴 $-87.48 | -2.55% |
| **BTC/USD** | CRYPTO | 0.1947 | $63,955.48 | $59,577.16 | $11,598.78 | 🔴 $-852.39 | -6.85% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,598.00 | $1,002.33 | 🔴 $-328.86 | -24.70% |
| **GOOGL** | STOCK | 13.00 | $350.09 | $361.24 | $4,696.06 | 🟢 +$144.94 | +3.18% |
| **LLY** | STOCK | 12.00 | $1,135.36 | $1,183.78 | $14,205.36 | 🟢 +$581.04 | +4.26% |
| **META** | STOCK | 18.00 | $577.11 | $620.45 | $11,168.10 | 🟢 +$780.12 | +7.51% |
| **MSFT** | STOCK | 22.00 | $393.63 | $383.63 | $8,439.97 | 🔴 $-219.94 | -2.54% |
| **NVDA** | STOCK | 122.00 | $219.68 | $195.80 | $23,887.55 | 🔴 $-2,913.56 | -10.87% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $76.35 | $1,177.22 | 🔴 $-151.16 | -11.38% |
| **SPY** | STOCK | 6.0000 | $745.44 | $746.87 | $4,481.22 | 🟢 +$8.56 | +0.19% |
| **TSLA** | STOCK | 24.00 | $432.23 | $426.82 | $10,243.68 | 🔴 $-129.89 | -1.25% |
| **VTI** | ETF | 11.00 | $366.18 | $370.13 | $4,071.49 | 🟢 +$43.52 | +1.08% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $195.68 | 🔴 -2.21% | **BUY** | 100% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $361.09 | 🟢 +1.04% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $293.31 | 🟢 +1.37% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $383.71 | 🟢 +2.87% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $241.78 | 🟢 +1.44% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $370.11 | 🟢 +0.02% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $371.01 | 🔴 -1.78% | **BUY** | 97% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $619.53 | 🟢 +9.98% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $59,588.21 | 🟢 +1.81% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,181.56 | 🔴 -1.49% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-2.21%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.04%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.37%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 69% | Extreme gain today (+2.87%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.44%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.02%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 85% | Moderate negative momentum (-1.78%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 78% | Extreme gain today (+9.98%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.81%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 75% | Moderate negative momentum (-1.49%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
