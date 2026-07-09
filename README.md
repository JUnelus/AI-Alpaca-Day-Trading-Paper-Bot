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

> 🕐 **Last updated:** 2026-07-09 14:40 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$96,647.91` |
| 💸 Cash Available    | `$-41,231.39` |
| 🧾 Buying Power      | `$164,499.72` |
| 🟢 Total P&L | `+$13,005.19` &nbsp; `(+130.05%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$13,005.19` (+130.05%)
- **Yesterday-to-today P&L:** `$-596.59`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **AAPL** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 82% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 50.00 | $305.42 | $312.23 | $15,611.50 | 🟢 +$340.59 | +2.23% |
| **AMZN** | STOCK | 32.00 | $238.10 | $241.16 | $7,717.12 | 🟢 +$97.82 | +1.28% |
| **AVGO** | STOCK | 6.0000 | $372.25 | $394.00 | $2,363.97 | 🟢 +$130.48 | +5.84% |
| **BTC/USD** | CRYPTO | 0.2284 | $9,202.82 | $62,749.64 | $14,332.05 | 🟢 +$12,230.12 | +581.85% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,738.28 | $1,090.32 | 🟢 +$1,090.32 | 0.00% |
| **GOOGL** | STOCK | 18.00 | $353.31 | $353.70 | $6,366.60 | 🟢 +$7.09 | +0.11% |
| **LLY** | STOCK | 18.00 | $1,160.16 | $1,215.20 | $21,873.60 | 🟢 +$990.75 | +4.74% |
| **META** | STOCK | 20.00 | $574.01 | $594.86 | $11,897.20 | 🟢 +$416.92 | +3.63% |
| **MSFT** | STOCK | 26.00 | $392.07 | $377.28 | $9,809.28 | 🔴 $-384.62 | -3.77% |
| **NVDA** | STOCK | 132.00 | $217.83 | $200.54 | $26,471.28 | 🔴 $-2,282.82 | -7.94% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $77.62 | $1,196.81 | 🟢 +$1,196.81 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $748.42 | $4,490.52 | 🟢 +$17.86 | +0.40% |
| **TSLA** | STOCK | 24.00 | $432.23 | $394.86 | $9,476.64 | 🔴 $-896.93 | -8.65% |
| **VTI** | ETF | 14.00 | $366.54 | $370.17 | $5,182.42 | 🟢 +$50.81 | +0.99% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $200.37 | 🔴 -1.84% | **BUY** | 99% |
| 2 | **AAPL** | Apple Inc. | STOCK | $312.35 | 🔴 -0.33% | **BUY** | 74% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $354.15 | 🔴 -2.15% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $377.50 | 🔴 -1.52% | **BUY** | 96% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $241.49 | 🔴 -0.87% | **BUY** | 82% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $370.24 | 🟢 +0.54% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $394.00 | 🟢 +1.36% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $595.49 | 🔴 -1.27% | **BUY** | 85% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,874.18 | 🟢 +1.01% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,216.28 | 🟢 +0.04% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-1.84%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.33%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 85% | Moderate negative momentum (-2.15%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.52%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 72% | Moderate negative momentum (-0.87%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.54%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.36%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 75% | Moderate negative momentum (-1.27%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.01%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.04%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
