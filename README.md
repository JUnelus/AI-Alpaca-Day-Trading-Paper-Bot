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

> 🕐 **Last updated:** 2026-06-25 14:39 UTC &nbsp;|&nbsp; **Trades today:** 8 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$89,434.96` |
| 💸 Cash Available    | `$-21,343.47` |
| 🧾 Buying Power      | `$182,254.78` |
| 🔴 Total P&L | `$-9,583.31` &nbsp; `(-95.83%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-9,583.31` (-95.83%)
- **Yesterday-to-today P&L:** `$-1,903.03`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 57.00 | $307.33 | $279.39 | $15,925.23 | 🔴 $-1,592.58 | -9.09% |
| **AMZN** | STOCK | 28.00 | $241.88 | $229.25 | $6,419.00 | 🔴 $-353.75 | -5.22% |
| **AVGO** | STOCK | 5.0000 | $386.87 | $380.17 | $1,900.83 | 🔴 $-33.51 | -1.73% |
| **BTC/USD** | CRYPTO | 0.1681 | $64,746.14 | $59,705.84 | $10,033.67 | 🔴 $-847.03 | -7.78% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,569.50 | $984.45 | 🔴 $-346.74 | -26.05% |
| **GOOGL** | STOCK | 14.00 | $356.25 | $342.20 | $4,790.80 | 🔴 $-196.75 | -3.94% |
| **LLY** | STOCK | 12.00 | $1,126.41 | $1,131.14 | $13,573.68 | 🟢 +$56.76 | +0.42% |
| **META** | STOCK | 15.00 | $582.43 | $555.07 | $8,326.05 | 🔴 $-410.33 | -4.70% |
| **MSFT** | STOCK | 24.00 | $406.94 | $358.38 | $8,601.24 | 🔴 $-1,165.22 | -11.93% |
| **NVDA** | STOCK | 115.00 | $221.28 | $195.09 | $22,434.78 | 🔴 $-3,012.76 | -11.84% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $66.33 | $1,022.74 | 🔴 $-305.64 | -23.01% |
| **SPY** | STOCK | 6.0000 | $745.44 | $736.52 | $4,419.15 | 🔴 $-53.51 | -1.20% |
| **TSLA** | STOCK | 24.00 | $432.23 | $377.48 | $9,059.50 | 🔴 $-1,314.07 | -12.67% |
| **VTI** | ETF | 9.0000 | $366.75 | $365.84 | $3,292.56 | 🔴 $-8.18 | -0.25% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $194.87 | 🔴 -2.08% | **BUY** | 100% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $341.90 | 🔴 -0.98% | **BUY** | 84% |
| 3 | **AAPL** | Apple Inc. | STOCK | $279.24 | 🔴 -4.72% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $358.46 | 🔴 -1.92% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $229.17 | 🔴 -2.18% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.63 | 🟢 +0.54% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $379.80 | 🔴 -0.59% | **BUY** | 77% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $554.48 | 🔴 -0.57% | **BUY** | 77% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $59,559.13 | 🔴 -2.31% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,132.47 | 🟢 +1.36% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-2.08%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 74% | Moderate negative momentum (-0.98%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 78% | Extreme loss today (-4.72%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.92%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.18%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.54%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 68% | Moderate negative momentum (-0.59%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 68% | Moderate negative momentum (-0.57%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.31%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.36%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
