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

> 🕐 **Last updated:** 2026-06-23 14:40 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,247.73` |
| 💸 Cash Available    | `$-13,183.06` |
| 🧾 Buying Power      | `$205,515.93` |
| 🔴 Total P&L | `$-6,308.65` &nbsp; `(-63.09%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-6,308.65` (-63.09%)
- **Yesterday-to-today P&L:** `$-882.85`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 78% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 54.00 | $308.45 | $299.69 | $16,183.26 | 🔴 $-472.93 | -2.84% |
| **AMZN** | STOCK | 28.00 | $241.88 | $236.11 | $6,611.08 | 🔴 $-161.67 | -2.39% |
| **AVGO** | STOCK | 3.0000 | $387.66 | $385.34 | $1,156.02 | 🔴 $-6.95 | -0.60% |
| **BTC/USD** | CRYPTO | 0.1337 | $65,691.42 | $62,483.04 | $8,356.34 | 🔴 $-429.08 | -4.88% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,659.60 | $1,040.97 | 🔴 $-290.22 | -21.80% |
| **GOOGL** | STOCK | 11.00 | $359.00 | $347.36 | $3,820.96 | 🔴 $-128.02 | -3.24% |
| **LLY** | STOCK | 12.00 | $1,126.41 | $1,103.18 | $13,238.16 | 🔴 $-278.76 | -2.06% |
| **META** | STOCK | 14.00 | $584.75 | $568.25 | $7,955.43 | 🔴 $-231.09 | -2.82% |
| **MSFT** | STOCK | 22.00 | $411.30 | $375.86 | $8,268.92 | 🔴 $-779.77 | -8.62% |
| **NVDA** | STOCK | 108.00 | $222.67 | $202.77 | $21,899.64 | 🔴 $-2,148.22 | -8.93% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $69.30 | $1,068.52 | 🔴 $-259.86 | -19.56% |
| **SPY** | STOCK | 6.0000 | $745.44 | $737.40 | $4,424.40 | 🔴 $-48.26 | -1.08% |
| **TSLA** | STOCK | 24.00 | $432.23 | $387.95 | $9,310.80 | 🔴 $-1,062.77 | -10.24% |
| **VTI** | ETF | 7.0000 | $367.24 | $365.66 | $2,559.62 | 🔴 $-11.04 | -0.43% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $202.88 | 🔴 -2.77% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $299.65 | 🟢 +0.89% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $347.48 | 🔴 -0.63% | **BUY** | 78% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $376.04 | 🟢 +2.37% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $236.13 | 🟢 +1.43% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.71 | 🔴 -0.84% | **BUY** | 81% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $385.56 | 🔴 -1.67% | **BUY** | 96% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $568.59 | 🟢 +0.84% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,492.54 | 🔴 -2.26% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,102.54 | 🟢 +0.04% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 69% | Extreme loss today (-2.77%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.89%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 69% | Moderate negative momentum (-0.63%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+2.37%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.43%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 71% | Moderate negative momentum (-0.84%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 84% | Moderate negative momentum (-1.67%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.84%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.26%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.04%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
