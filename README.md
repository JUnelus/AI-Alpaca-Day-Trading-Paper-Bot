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

> 🕐 **Last updated:** 2026-06-15 15:41 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,772.73` |
| 💸 Cash Available    | `$4,968.31` |
| 🧾 Buying Power      | `$246,031.52` |
| 🔴 Total P&L | `$-3,171.69` &nbsp; `(-31.72%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-3,171.69` (-31.72%)
- **Yesterday-to-today P&L:** `+$2,309.51`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **META** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $308.82 | $296.87 | $15,437.24 | 🔴 $-621.17 | -3.87% |
| **AMZN** | STOCK | 20.00 | $243.99 | $245.95 | $4,918.97 | 🟢 +$39.10 | +0.80% |
| **AVGO** | STOCK | 11.00 | $393.05 | $393.54 | $4,328.89 | 🟢 +$5.36 | +0.12% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $66,816.50 | $1,707.13 | 🔴 $-182.35 | -9.65% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,822.50 | $1,143.14 | 🔴 $-188.05 | -14.13% |
| **GOOGL** | STOCK | 7.0000 | $361.34 | $371.60 | $2,601.16 | 🟢 +$71.82 | +2.84% |
| **LLY** | STOCK | 4.0000 | $1,148.32 | $1,130.99 | $4,523.96 | 🔴 $-69.31 | -1.51% |
| **META** | STOCK | 14.00 | $596.84 | $597.73 | $8,368.15 | 🟢 +$12.38 | +0.15% |
| **MSFT** | STOCK | 16.00 | $422.42 | $398.32 | $6,373.12 | 🔴 $-385.54 | -5.70% |
| **NVDA** | STOCK | 100.00 | $223.97 | $211.61 | $21,161.00 | 🔴 $-1,236.39 | -5.52% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $74.65 | $1,151.01 | 🔴 $-177.37 | -13.35% |
| **SPY** | STOCK | 6.0000 | $745.44 | $755.32 | $4,531.92 | 🟢 +$59.26 | +1.32% |
| **TSLA** | STOCK | 24.00 | $432.23 | $410.36 | $9,848.64 | 🔴 $-524.93 | -5.06% |
| **VTI** | ETF | 4.0000 | $366.61 | $372.98 | $1,491.92 | 🟢 +$25.49 | +1.74% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $211.56 | 🟢 +3.10% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $371.84 | 🟢 +3.38% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $296.85 | 🟢 +1.96% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $398.32 | 🟢 +1.94% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $245.95 | 🟢 +3.10% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $373.02 | 🟢 +1.82% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $393.50 | 🟢 +2.99% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $597.74 | 🟢 +5.42% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $66,806.84 | 🟢 +1.68% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,131.19 | 🔴 -0.16% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 71% | Extreme gain today (+3.10%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 72% | Extreme gain today (+3.38%) — mean reversion pullback likely |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.96%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.94%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 71% | Extreme gain today (+3.10%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.82%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 70% | Extreme gain today (+2.99%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 78% | Extreme gain today (+5.42%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.68%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.16%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
