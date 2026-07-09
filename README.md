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

> 🕐 **Last updated:** 2026-07-09 21:44 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,764.58` |
| 💸 Cash Available    | `$-43,752.96` |
| 🧾 Buying Power      | `$168,659.04` |
| 🟢 Total P&L | `+$15,121.86` &nbsp; `(+151.22%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$15,121.86` (+151.22%)
- **Yesterday-to-today P&L:** `+$1,520.08`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 82% | DCA buy: quality asset on a mild dip |
| **META** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 51.00 | $305.55 | $315.74 | $16,102.74 | 🟢 +$519.63 | +3.33% |
| **AMZN** | STOCK | 34.00 | $238.28 | $246.32 | $8,374.88 | 🟢 +$273.26 | +3.37% |
| **AVGO** | STOCK | 6.0000 | $372.25 | $402.46 | $2,414.76 | 🟢 +$181.27 | +8.12% |
| **BTC/USD** | CRYPTO | 0.2284 | $9,202.82 | $63,164.64 | $14,426.83 | 🟢 +$12,324.90 | +586.36% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,744.55 | $1,094.25 | 🟢 +$1,094.25 | 0.00% |
| **GOOGL** | STOCK | 19.00 | $353.33 | $358.09 | $6,803.72 | 🟢 +$90.50 | +1.35% |
| **LLY** | STOCK | 18.00 | $1,160.16 | $1,219.56 | $21,952.04 | 🟢 +$1,069.19 | +5.12% |
| **META** | STOCK | 21.00 | $575.01 | $627.46 | $13,176.66 | 🟢 +$1,101.47 | +9.12% |
| **MSFT** | STOCK | 27.00 | $391.53 | $383.80 | $10,362.60 | 🔴 $-208.62 | -1.97% |
| **NVDA** | STOCK | 134.00 | $217.58 | $202.78 | $27,172.52 | 🔴 $-1,982.70 | -6.80% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $78.18 | $1,205.44 | 🟢 +$1,205.44 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $751.20 | $4,507.20 | 🟢 +$34.54 | +0.77% |
| **TSLA** | STOCK | 24.00 | $432.23 | $405.22 | $9,725.28 | 🔴 $-648.29 | -6.25% |
| **VTI** | ETF | 14.00 | $366.54 | $371.33 | $5,198.62 | 🟢 +$67.01 | +1.31% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $202.78 | 🔴 -0.66% | **BUY** | 79% |
| 2 | **AAPL** | Apple Inc. | STOCK | $316.22 | 🟢 +0.90% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $358.89 | 🔴 -0.84% | **BUY** | 82% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $384.36 | 🟢 +0.27% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $247.04 | 🟢 +1.40% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $371.45 | 🟢 +0.87% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $401.11 | 🟢 +3.20% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $631.48 | 🟢 +4.70% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,185.35 | 🟢 +1.51% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,216.95 | 🟢 +0.09% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 69% | Moderate negative momentum (-0.66%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.90%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 72% | Moderate negative momentum (-0.84%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.27%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.40%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.87%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 71% | Extreme gain today (+3.20%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 78% | Extreme gain today (+4.70%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.51%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.09%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
