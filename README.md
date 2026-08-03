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

> 🕐 **Last updated:** 2026-08-03 14:39 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,368.14` |
| 💸 Cash Available    | `$-83,537.07` |
| 🧾 Buying Power      | `$114,089.14` |
| 🟢 Total P&L | `+$14,607.19` &nbsp; `(+146.07%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$14,607.19` (+146.07%)
- **Yesterday-to-today P&L:** `+$3,000.55`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | SELL | 100% | Take-profit trim after overextended rally |
| **AMZN** | SELL | 100% | Take-profit trim after overextended rally |
| **AVGO** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **META** | SELL | 100% | Take-profit trim after overextended rally |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 58.00 | $307.78 | $305.50 | $17,718.71 | 🔴 $-132.48 | -0.74% |
| **AMZN** | STOCK | 46.00 | $238.78 | $285.33 | $13,125.41 | 🟢 +$2,141.63 | +19.50% |
| **AVGO** | STOCK | 15.00 | $381.79 | $383.30 | $5,749.50 | 🟢 +$22.71 | +0.40% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $63,664.70 | $17,684.57 | 🟢 +$12,438.80 | +237.12% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,865.01 | $1,169.81 | 🟢 +$1,169.81 | 0.00% |
| **GOOGL** | STOCK | 22.00 | $350.99 | $368.03 | $8,096.66 | 🟢 +$374.98 | +4.86% |
| **LLY** | STOCK | 32.00 | $1,160.99 | $1,120.71 | $35,862.72 | 🔴 $-1,288.92 | -3.47% |
| **META** | STOCK | 28.00 | $594.11 | $585.24 | $16,386.58 | 🔴 $-248.57 | -1.49% |
| **MSFT** | STOCK | 28.00 | $385.20 | $486.15 | $13,612.20 | 🟢 +$2,826.63 | +26.21% |
| **NVDA** | STOCK | 157.00 | $214.30 | $206.15 | $32,365.55 | 🔴 $-1,279.79 | -3.80% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.62 | $1,135.13 | 🟢 +$1,135.13 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $754.92 | $4,529.55 | 🟢 +$56.89 | +1.27% |
| **TSLA** | STOCK | 24.00 | $432.23 | $318.54 | $7,644.96 | 🔴 $-2,728.61 | -26.30% |
| **VTI** | ETF | 21.00 | $366.90 | $372.56 | $7,823.86 | 🟢 +$118.97 | +1.54% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $205.79 | 🟢 +2.51% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $368.05 | 🟢 +3.35% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $305.62 | 🔴 -1.07% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $486.37 | 🟢 +4.66% | **SELL** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $285.71 | 🟢 +5.20% | **SELL** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $372.45 | 🟢 +1.15% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $382.66 | 🔴 -1.70% | **BUY** | 96% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $585.71 | 🟢 +5.21% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,681.54 | 🟢 +0.27% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,121.04 | 🔴 -2.42% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 68% | Extreme gain today (+2.51%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 72% | Extreme gain today (+3.35%) — mean reversion pullback likely |
| 3 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.07%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 78% | Extreme gain today (+4.66%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 78% | Extreme gain today (+5.20%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.15%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 85% | Moderate negative momentum (-1.70%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 78% | Extreme gain today (+5.21%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.27%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.42%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
