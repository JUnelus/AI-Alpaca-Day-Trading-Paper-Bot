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

> 🕐 **Last updated:** 2026-06-08 21:52 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,801.85` |
| 💸 Cash Available    | `$27,171.92` |
| 🧾 Buying Power      | `$273,095.74` |
| 🔴 Total P&L | `$-4,142.88` &nbsp; `(-41.43%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-4,142.88` (-41.43%)
- **Yesterday-to-today P&L:** `+$399.41`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 45.00 | $311.37 | $300.26 | $13,511.70 | 🔴 $-499.99 | -3.57% |
| **AMZN** | STOCK | 6.0000 | $251.09 | $245.36 | $1,472.16 | 🔴 $-34.37 | -2.28% |
| **AVGO** | STOCK | 5.0000 | $405.01 | $397.30 | $1,986.50 | 🔴 $-38.55 | -1.90% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $63,721.76 | $1,628.07 | 🔴 $-261.42 | -13.84% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,708.77 | $1,071.81 | 🔴 $-259.39 | -19.49% |
| **GOOGL** | STOCK | 4.0000 | $365.06 | $363.70 | $1,454.82 | 🔴 $-5.41 | -0.37% |
| **META** | STOCK | 9.0000 | $611.63 | $586.24 | $5,276.16 | 🔴 $-228.47 | -4.15% |
| **MSFT** | STOCK | 9.0000 | $443.26 | $410.78 | $3,697.00 | 🔴 $-292.32 | -7.33% |
| **NVDA** | STOCK | 94.00 | $225.17 | $208.20 | $19,570.80 | 🔴 $-1,595.50 | -7.54% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $67.61 | $1,042.54 | 🔴 $-285.84 | -21.52% |
| **SPY** | STOCK | 6.0000 | $745.44 | $739.13 | $4,434.78 | 🔴 $-37.88 | -0.85% |
| **TSLA** | STOCK | 24.00 | $432.23 | $407.65 | $9,783.65 | 🔴 $-589.92 | -5.69% |
| **VTI** | ETF | 3.0000 | $369.03 | $364.42 | $1,093.26 | 🔴 $-13.83 | -1.25% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.64 | 🟢 +1.73% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $363.31 | 🔴 -1.42% | **BUY** | 85% |
| 3 | **AAPL** | Apple Inc. | STOCK | $301.54 | 🔴 -1.89% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $411.74 | 🔴 -1.18% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $245.22 | 🔴 -0.33% | **BUY** | 73% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $364.47 | 🟢 +0.30% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $396.60 | 🟢 +2.82% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $585.39 | 🔴 -1.28% | **BUY** | 85% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,745.16 | 🟢 +0.69% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,149.15 | 🟢 +1.57% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.73%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.42%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **SELL** | 85% | Moderate negative momentum (-1.89%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.18%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.33%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.30%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 69% | Extreme gain today (+2.82%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 75% | Moderate negative momentum (-1.28%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.69%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.57%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
