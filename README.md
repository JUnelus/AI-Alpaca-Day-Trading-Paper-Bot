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

> 🕐 **Last updated:** 2026-07-02 14:30 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$96,230.71` |
| 💸 Cash Available    | `$-29,183.13` |
| 🧾 Buying Power      | `$186,014.19` |
| 🔴 Total P&L | `$-2,542.01` &nbsp; `(-25.42%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-2,542.01` (-25.42%)
- **Yesterday-to-today P&L:** `+$930.06`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $305.99 | $305.25 | $18,315.00 | 🔴 $-44.46 | -0.24% |
| **AMZN** | STOCK | 28.00 | $237.74 | $244.13 | $6,835.64 | 🟢 +$179.00 | +2.69% |
| **AVGO** | STOCK | 11.00 | $378.26 | $369.87 | $4,068.51 | 🔴 $-92.34 | -2.22% |
| **BTC/USD** | CRYPTO | 0.1947 | $63,955.48 | $61,685.80 | $12,009.30 | 🔴 $-441.87 | -3.55% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,698.74 | $1,065.52 | 🔴 $-265.67 | -19.96% |
| **GOOGL** | STOCK | 13.00 | $350.09 | $362.18 | $4,708.34 | 🟢 +$157.23 | +3.45% |
| **LLY** | STOCK | 14.00 | $1,143.08 | $1,223.55 | $17,129.70 | 🟢 +$1,126.60 | +7.04% |
| **META** | STOCK | 14.00 | $570.52 | $591.34 | $8,278.76 | 🟢 +$291.54 | +3.65% |
| **MSFT** | STOCK | 22.00 | $393.63 | $389.26 | $8,563.83 | 🔴 $-96.08 | -1.11% |
| **NVDA** | STOCK | 126.00 | $218.95 | $198.17 | $24,969.42 | 🔴 $-2,618.50 | -9.49% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $80.43 | $1,240.13 | 🔴 $-88.25 | -6.64% |
| **SPY** | STOCK | 6.0000 | $745.44 | $748.54 | $4,491.24 | 🟢 +$18.58 | +0.42% |
| **TSLA** | STOCK | 24.00 | $432.23 | $402.36 | $9,656.64 | 🔴 $-716.93 | -6.91% |
| **VTI** | ETF | 11.00 | $366.18 | $370.64 | $4,077.09 | 🟢 +$49.13 | +1.22% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $197.85 | 🟢 +0.14% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $305.05 | 🟢 +3.62% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $362.07 | 🟢 +0.24% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $388.65 | 🟢 +1.14% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $244.13 | 🟢 +1.01% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $370.31 | 🟢 +0.28% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $369.17 | 🔴 -0.05% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $590.92 | 🔴 -3.59% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,612.46 | 🟢 +2.75% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,223.55 | 🟢 +2.67% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.14%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **SELL** | 73% | Extreme gain today (+3.62%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.24%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.14%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.01%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.28%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (-0.05%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 73% | Extreme loss today (-3.59%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 69% | Extreme gain today (+2.75%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 68% | Extreme gain today (+2.67%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
