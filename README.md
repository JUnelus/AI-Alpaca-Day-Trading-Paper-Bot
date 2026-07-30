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

> 🕐 **Last updated:** 2026-07-30 14:31 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,401.14` |
| 💸 Cash Available    | `$-87,649.57` |
| 🧾 Buying Power      | `$93,890.50` |
| 🟢 Total P&L | `+$10,256.56` &nbsp; `(+102.57%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$10,256.56` (+102.57%)
- **Yesterday-to-today P&L:** `+$3,142.27`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | SELL | 100% | Take-profit trim after overextended rally |
| **AMZN** | SELL | 100% | Take-profit trim after overextended rally |
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 55.00 | $307.98 | $330.92 | $18,200.60 | 🟢 +$1,261.89 | +7.45% |
| **AMZN** | STOCK | 62.00 | $239.07 | $237.80 | $14,743.60 | 🔴 $-78.86 | -0.53% |
| **AVGO** | STOCK | 20.00 | $379.18 | $386.90 | $7,738.10 | 🟢 +$154.47 | +2.04% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $64,810.54 | $18,002.86 | 🟢 +$12,757.09 | +243.19% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,914.50 | $1,200.85 | 🟢 +$1,200.85 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $332.67 | $9,314.76 | 🔴 $-569.21 | -5.76% |
| **LLY** | STOCK | 28.00 | $1,162.53 | $1,161.73 | $32,528.44 | 🔴 $-22.39 | -0.07% |
| **META** | STOCK | 26.00 | $598.21 | $530.74 | $13,799.24 | 🔴 $-1,754.26 | -11.28% |
| **MSFT** | STOCK | 34.00 | $392.64 | $450.31 | $15,310.71 | 🟢 +$1,960.98 | +14.69% |
| **NVDA** | STOCK | 157.00 | $214.30 | $196.84 | $30,903.88 | 🔴 $-2,741.46 | -8.15% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $74.13 | $1,142.92 | 🟢 +$1,142.92 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $738.57 | $4,431.42 | 🔴 $-41.24 | -0.92% |
| **TSLA** | STOCK | 24.00 | $432.23 | $308.65 | $7,407.66 | 🔴 $-2,965.91 | -28.59% |
| **VTI** | ETF | 21.00 | $366.90 | $364.60 | $7,656.60 | 🔴 $-48.29 | -0.63% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $330.77 | 🔴 -2.19% | **BUY** | 100% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $196.76 | 🟢 +3.55% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $332.15 | 🔴 -1.35% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $450.61 | 🟢 +15.38% | **SELL** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $237.69 | 🟢 +4.87% | **SELL** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $364.64 | 🟢 +1.17% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $386.77 | 🟢 +4.44% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $531.10 | 🔴 -9.31% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,736.05 | 🟢 +1.31% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,161.88 | 🔴 -3.98% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 85% | Moderate negative momentum (-2.19%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 73% | Extreme gain today (+3.55%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.35%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 78% | Extreme gain today (+15.38%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 78% | Extreme gain today (+4.87%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.17%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 77% | Extreme gain today (+4.44%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 78% | Extreme loss today (-9.31%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.31%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 75% | Extreme loss today (-3.98%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
