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

> 🕐 **Last updated:** 2026-07-13 21:32 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,298.72` |
| 💸 Cash Available    | `$-48,652.34` |
| 🧾 Buying Power      | `$157,035.06` |
| 🟢 Total P&L | `+$14,171.32` &nbsp; `(+141.71%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$14,171.32` (+141.71%)
- **Yesterday-to-today P&L:** `$-2,130.91`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 80% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 76% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $305.69 | $317.11 | $16,489.53 | 🟢 +$593.61 | +3.73% |
| **AMZN** | STOCK | 38.00 | $239.13 | $247.10 | $9,389.80 | 🟢 +$302.78 | +3.33% |
| **AVGO** | STOCK | 8.0000 | $379.21 | $384.21 | $3,073.68 | 🟢 +$40.02 | +1.32% |
| **BTC/USD** | CRYPTO | 0.2453 | $12,850.01 | $62,029.90 | $15,213.34 | 🟢 +$12,061.77 | +382.72% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,759.50 | $1,103.63 | 🟢 +$1,103.63 | 0.00% |
| **GOOGL** | STOCK | 23.00 | $353.67 | $352.39 | $8,104.88 | 🔴 $-29.62 | -0.36% |
| **LLY** | STOCK | 21.00 | $1,163.49 | $1,183.50 | $24,853.50 | 🟢 +$420.30 | +1.72% |
| **META** | STOCK | 16.00 | $580.24 | $656.39 | $10,502.24 | 🟢 +$1,218.45 | +13.12% |
| **MSFT** | STOCK | 28.00 | $391.24 | $390.45 | $10,932.60 | 🔴 $-22.01 | -0.20% |
| **NVDA** | STOCK | 131.00 | $217.22 | $203.45 | $26,651.95 | 🔴 $-1,804.25 | -6.34% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $74.50 | $1,148.73 | 🟢 +$1,148.73 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $748.21 | $4,489.26 | 🟢 +$16.60 | +0.37% |
| **TSLA** | STOCK | 24.00 | $432.23 | $393.88 | $9,453.01 | 🔴 $-920.56 | -8.87% |
| **VTI** | ETF | 15.00 | $366.87 | $369.66 | $5,544.90 | 🟢 +$41.87 | +0.76% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $203.53 | 🔴 -3.52% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $317.31 | 🟢 +0.63% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $352.51 | 🔴 -1.31% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $390.99 | 🟢 +1.53% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $247.31 | 🟢 +0.80% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $369.78 | 🔴 -0.78% | **BUY** | 80% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $384.05 | 🔴 -3.98% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $656.73 | 🔴 -1.86% | **BUY** | 99% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,962.83 | 🔴 -2.80% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,181.87 | 🔴 -0.56% | **BUY** | 76% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 73% | Extreme loss today (-3.52%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.63%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.31%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.53%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.80%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 70% | Moderate negative momentum (-0.78%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 75% | Extreme loss today (-3.98%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-1.86%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 69% | Extreme loss today (-2.80%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 67% | Moderate negative momentum (-0.56%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
