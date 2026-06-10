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

> 🕐 **Last updated:** 2026-06-10 14:42 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,193.33` |
| 💸 Cash Available    | `$19,711.37` |
| 🧾 Buying Power      | `$257,932.54` |
| 🔴 Total P&L | `$-5,750.37` &nbsp; `(-57.50%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,750.37` (-57.50%)
- **Yesterday-to-today P&L:** `$-429.42`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $310.31 | $289.19 | $13,880.88 | 🔴 $-1,014.01 | -6.81% |
| **AMZN** | STOCK | 10.00 | $248.75 | $241.12 | $2,411.25 | 🔴 $-76.26 | -3.07% |
| **AVGO** | STOCK | 7.0000 | $400.03 | $376.92 | $2,638.44 | 🔴 $-161.74 | -5.78% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $61,974.50 | $1,583.42 | 🔴 $-306.06 | -16.20% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,644.74 | $1,031.65 | 🔴 $-299.55 | -22.50% |
| **GOOGL** | STOCK | 5.0000 | $365.74 | $365.25 | $1,826.25 | 🔴 $-2.46 | -0.13% |
| **LLY** | STOCK | 1.0000 | $1,155.00 | $1,157.03 | $1,157.03 | 🟢 +$2.02 | +0.18% |
| **META** | STOCK | 10.00 | $609.51 | $583.07 | $5,830.65 | 🔴 $-264.46 | -4.34% |
| **MSFT** | STOCK | 12.00 | $433.91 | $402.71 | $4,832.58 | 🔴 $-374.36 | -7.19% |
| **NVDA** | STOCK | 96.00 | $224.81 | $205.92 | $19,768.32 | 🔴 $-1,813.00 | -8.40% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $65.12 | $1,004.04 | 🔴 $-324.34 | -24.42% |
| **SPY** | STOCK | 6.0000 | $745.44 | $736.60 | $4,419.60 | 🔴 $-53.06 | -1.19% |
| **TSLA** | STOCK | 24.00 | $432.23 | $388.58 | $9,325.92 | 🔴 $-1,047.65 | -10.10% |
| **VTI** | ETF | 3.0000 | $369.03 | $363.88 | $1,091.65 | 🔴 $-15.44 | -1.39% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $206.28 | 🔴 -0.92% | **BUY** | 83% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $365.57 | 🟢 +0.36% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $289.40 | 🔴 -0.39% | **BUY** | 75% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $402.87 | 🔴 -0.13% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $241.25 | 🔴 -1.21% | **BUY** | 85% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $364.04 | 🟢 +0.10% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $377.76 | 🔴 -3.67% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $583.49 | 🔴 -0.19% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,046.74 | 🟢 +0.58% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,157.50 | 🟢 +1.12% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 73% | Moderate negative momentum (-0.92%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.36%) — no trend to carry forward |
| 3 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.13%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Moderate negative momentum (-1.21%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.10%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 73% | Extreme loss today (-3.67%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.19%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.58%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.12%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
