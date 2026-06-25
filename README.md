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

> 🕐 **Last updated:** 2026-06-25 21:49 UTC &nbsp;|&nbsp; **Trades today:** 8 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$88,815.18` |
| 💸 Cash Available    | `$-23,469.64` |
| 🧾 Buying Power      | `$175,297.05` |
| 🔴 Total P&L | `$-10,209.05` &nbsp; `(-102.09%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-10,209.05` (-102.09%)
- **Yesterday-to-today P&L:** `$-2,528.76`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 96% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 57.00 | $307.33 | $275.15 | $15,683.55 | 🔴 $-1,834.25 | -10.47% |
| **AMZN** | STOCK | 30.00 | $241.04 | $226.97 | $6,809.10 | 🔴 $-422.23 | -5.84% |
| **AVGO** | STOCK | 6.0000 | $385.77 | $379.75 | $2,278.50 | 🔴 $-36.10 | -1.56% |
| **BTC/USD** | CRYPTO | 0.1768 | $64,503.31 | $59,773.80 | $10,569.78 | 🔴 $-836.32 | -7.33% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,574.06 | $987.31 | 🔴 $-343.88 | -25.83% |
| **GOOGL** | STOCK | 14.00 | $356.25 | $342.60 | $4,796.40 | 🔴 $-191.15 | -3.83% |
| **LLY** | STOCK | 12.00 | $1,126.41 | $1,128.99 | $13,547.88 | 🟢 +$30.96 | +0.23% |
| **META** | STOCK | 16.00 | $580.72 | $544.25 | $8,708.00 | 🔴 $-583.45 | -6.28% |
| **MSFT** | STOCK | 24.00 | $406.94 | $354.36 | $8,504.64 | 🔴 $-1,261.82 | -12.92% |
| **NVDA** | STOCK | 116.00 | $221.06 | $195.54 | $22,682.64 | 🔴 $-2,959.99 | -11.54% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $67.03 | $1,033.52 | 🔴 $-294.86 | -22.20% |
| **SPY** | STOCK | 6.0000 | $745.44 | $733.50 | $4,401.00 | 🔴 $-71.66 | -1.60% |
| **TSLA** | STOCK | 24.00 | $432.23 | $374.57 | $8,989.70 | 🔴 $-1,383.87 | -13.34% |
| **VTI** | ETF | 9.0000 | $366.75 | $364.48 | $3,280.32 | 🔴 $-20.42 | -0.62% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $195.74 | 🔴 -1.64% | **BUY** | 96% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $343.71 | 🔴 -0.46% | **BUY** | 76% |
| 3 | **AAPL** | Apple Inc. | STOCK | $275.15 | 🔴 -6.12% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $352.83 | 🔴 -3.46% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $227.01 | 🔴 -3.10% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $363.98 | 🟢 +0.09% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $378.91 | 🔴 -0.83% | **BUY** | 81% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $542.87 | 🔴 -2.65% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $59,817.30 | 🔴 -1.89% | **BUY** | 96% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,127.69 | 🟢 +0.93% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-1.64%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 67% | Moderate negative momentum (-0.46%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 78% | Extreme loss today (-6.12%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 72% | Extreme loss today (-3.46%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 70% | Extreme loss today (-3.10%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.09%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 71% | Moderate negative momentum (-0.83%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 68% | Extreme loss today (-2.65%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 84% | Moderate negative momentum (-1.89%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.93%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
