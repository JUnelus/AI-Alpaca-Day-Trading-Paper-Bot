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

> 🕐 **Last updated:** 2026-08-04 21:41 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$102,501.59` |
| 💸 Cash Available    | `$-76,854.14` |
| 🧾 Buying Power      | `$130,175.22` |
| 🟢 Total P&L | `+$16,597.78` &nbsp; `(+165.98%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$16,597.78` (+165.98%)
- **Yesterday-to-today P&L:** `+$2,092.73`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **META** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 75% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $307.67 | $310.31 | $18,618.77 | 🟢 +$158.50 | +0.86% |
| **AMZN** | STOCK | 37.00 | $239.83 | $277.70 | $10,274.90 | 🟢 +$1,401.17 | +15.79% |
| **AVGO** | STOCK | 13.00 | $381.89 | $416.03 | $5,408.39 | 🟢 +$443.87 | +8.94% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $64,166.40 | $17,823.93 | 🟢 +$12,578.16 | +239.78% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,872.42 | $1,174.46 | 🟢 +$1,174.46 | 0.00% |
| **GOOGL** | STOCK | 18.00 | $351.05 | $379.20 | $6,825.65 | 🟢 +$506.75 | +8.02% |
| **LLY** | STOCK | 34.00 | $1,158.57 | $1,125.79 | $38,276.86 | 🔴 $-1,114.45 | -2.83% |
| **META** | STOCK | 25.00 | $594.80 | $587.50 | $14,687.50 | 🔴 $-182.42 | -1.23% |
| **MSFT** | STOCK | 22.00 | $383.50 | $492.00 | $10,824.00 | 🟢 +$2,386.94 | +28.29% |
| **NVDA** | STOCK | 157.00 | $214.30 | $215.81 | $33,882.15 | 🟢 +$236.81 | +0.70% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.82 | $1,138.19 | 🟢 +$1,138.19 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $772.17 | $4,633.02 | 🟢 +$160.36 | +3.59% |
| **TSLA** | STOCK | 24.00 | $432.23 | $324.54 | $7,788.99 | 🔴 $-2,584.58 | -24.92% |
| **VTI** | ETF | 21.00 | $366.90 | $380.90 | $7,998.90 | 🟢 +$294.01 | +3.82% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $211.94 | 🟢 +2.56% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $377.65 | 🟢 +1.11% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $309.38 | 🟢 +1.96% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $492.81 | 🟢 +1.06% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $277.42 | 🔴 -2.32% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $380.82 | 🟢 +1.87% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $418.16 | 🟢 +6.61% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $587.94 | 🔴 -0.39% | **BUY** | 74% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,191.20 | 🟢 +1.16% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,115.68 | 🔴 -0.51% | **BUY** | 75% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 68% | Extreme gain today (+2.56%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.11%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.96%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.06%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.32%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.87%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 78% | Extreme gain today (+6.61%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.16%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 66% | Moderate negative momentum (-0.51%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
