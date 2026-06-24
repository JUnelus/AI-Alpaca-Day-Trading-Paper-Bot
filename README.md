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

> 🕐 **Last updated:** 2026-06-24 21:45 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$91,345.27` |
| 💸 Cash Available    | `$-18,047.99` |
| 🧾 Buying Power      | `$192,243.21` |
| 🔴 Total P&L | `$-7,680.28` &nbsp; `(-76.80%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-7,680.28` (-76.80%)
- **Yesterday-to-today P&L:** `$-606.38`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 55.00 | $308.19 | $293.54 | $16,144.70 | 🔴 $-805.72 | -4.75% |
| **AMZN** | STOCK | 28.00 | $241.88 | $234.69 | $6,571.32 | 🔴 $-201.43 | -2.97% |
| **AVGO** | STOCK | 5.0000 | $386.87 | $389.20 | $1,946.01 | 🟢 +$11.67 | +0.60% |
| **BTC/USD** | CRYPTO | 0.1593 | $65,027.92 | $61,033.80 | $9,721.08 | 🔴 $-636.16 | -6.14% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,617.21 | $1,014.38 | 🔴 $-316.81 | -23.80% |
| **GOOGL** | STOCK | 13.00 | $357.33 | $345.50 | $4,491.50 | 🔴 $-153.82 | -3.31% |
| **LLY** | STOCK | 12.00 | $1,126.41 | $1,111.50 | $13,338.00 | 🔴 $-178.92 | -1.32% |
| **META** | STOCK | 14.00 | $584.75 | $559.77 | $7,836.78 | 🔴 $-349.74 | -4.27% |
| **MSFT** | STOCK | 22.00 | $411.30 | $366.94 | $8,072.68 | 🔴 $-976.01 | -10.79% |
| **NVDA** | STOCK | 112.00 | $221.92 | $200.21 | $22,423.52 | 🔴 $-2,431.28 | -9.78% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $67.88 | $1,046.55 | 🔴 $-281.83 | -21.22% |
| **SPY** | STOCK | 6.0000 | $745.44 | $737.57 | $4,425.42 | 🔴 $-47.24 | -1.06% |
| **TSLA** | STOCK | 24.00 | $432.23 | $377.88 | $9,069.12 | 🔴 $-1,304.45 | -12.57% |
| **VTI** | ETF | 9.0000 | $366.75 | $365.80 | $3,292.20 | 🔴 $-8.54 | -0.26% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $199.00 | 🔴 -0.52% | **BUY** | 77% |
| 2 | **AAPL** | Apple Inc. | STOCK | $293.08 | 🔴 -0.41% | **BUY** | 75% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $345.29 | 🔴 -0.24% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $365.46 | 🔴 -2.27% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $234.27 | 🟢 +0.07% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $363.65 | 🔴 -0.01% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $382.07 | 🟢 +0.51% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $557.67 | 🔴 -0.81% | **BUY** | 81% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $60,998.71 | 🔴 -2.63% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,117.26 | 🟢 +0.92% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 67% | Moderate negative momentum (-0.52%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 66% | Moderate negative momentum (-0.41%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.24%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-2.27%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.07%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.01%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+0.51%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 71% | Moderate negative momentum (-0.81%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 68% | Extreme loss today (-2.63%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.92%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
