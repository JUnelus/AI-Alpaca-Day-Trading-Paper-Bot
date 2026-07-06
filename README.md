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

> 🕐 **Last updated:** 2026-07-06 21:46 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$97,288.05` |
| 💸 Cash Available    | `$-32,218.32` |
| 🧾 Buying Power      | `$180,891.34` |
| 🔴 Total P&L | `$-1,440.63` &nbsp; `(-14.41%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,440.63` (-14.41%)
- **Yesterday-to-today P&L:** `+$1,699.16`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $305.99 | $312.69 | $15,009.36 | 🟢 +$321.79 | +2.19% |
| **AMZN** | STOCK | 28.00 | $237.74 | $244.60 | $6,848.80 | 🟢 +$192.16 | +2.89% |
| **AVGO** | STOCK | 11.00 | $377.43 | $374.27 | $4,117.00 | 🔴 $-34.75 | -0.84% |
| **BTC/USD** | CRYPTO | 0.2032 | $63,872.65 | $64,116.39 | $13,026.12 | 🟢 +$49.52 | +0.38% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,810.93 | $1,135.89 | 🔴 $-195.30 | -14.67% |
| **GOOGL** | STOCK | 16.00 | $352.54 | $366.02 | $5,856.30 | 🟢 +$215.70 | +3.82% |
| **LLY** | STOCK | 15.00 | $1,146.94 | $1,204.00 | $18,060.00 | 🟢 +$855.90 | +4.97% |
| **META** | STOCK | 18.00 | $572.09 | $599.74 | $10,795.32 | 🟢 +$497.73 | +4.83% |
| **MSFT** | STOCK | 23.00 | $393.23 | $387.23 | $8,906.29 | 🔴 $-138.02 | -1.53% |
| **NVDA** | STOCK | 132.00 | $217.83 | $195.55 | $25,812.60 | 🔴 $-2,941.50 | -10.23% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $82.36 | $1,269.89 | 🔴 $-58.49 | -4.40% |
| **SPY** | STOCK | 6.0000 | $745.44 | $751.84 | $4,511.06 | 🟢 +$38.40 | +0.86% |
| **TSLA** | STOCK | 24.00 | $432.23 | $419.47 | $10,067.28 | 🔴 $-306.29 | -2.95% |
| **VTI** | ETF | 11.00 | $366.18 | $371.86 | $4,090.47 | 🟢 +$62.51 | +1.55% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $195.55 | 🟢 +0.37% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $312.66 | 🟢 +1.31% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $366.46 | 🟢 +1.82% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $386.74 | 🔴 -0.96% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $244.16 | 🟢 +0.61% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $371.67 | 🟢 +0.79% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $373.90 | 🟢 +3.73% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $600.29 | 🟢 +2.98% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,152.20 | 🟢 +0.88% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,200.06 | 🔴 -1.14% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.37%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.31%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.82%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-0.96%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.61%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.79%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 74% | Extreme gain today (+3.73%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 70% | Extreme gain today (+2.98%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.88%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 75% | Moderate negative momentum (-1.14%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
