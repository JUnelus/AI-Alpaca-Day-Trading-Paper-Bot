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

> 🕐 **Last updated:** 2026-06-26 21:43 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$90,484.92` |
| 💸 Cash Available    | `$-26,443.14` |
| 🧾 Buying Power      | `$177,350.59` |
| 🔴 Total P&L | `$-8,602.93` &nbsp; `(-86.03%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-8,602.93` (-86.03%)
- **Yesterday-to-today P&L:** `+$1,606.11`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **MSFT** | SELL | 100% | Take-profit trim after overextended rally |
| **VTI** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 58.00 | $306.80 | $281.68 | $16,337.44 | 🔴 $-1,457.10 | -8.19% |
| **AMZN** | STOCK | 32.00 | $240.18 | $232.42 | $7,437.42 | 🔴 $-248.41 | -3.23% |
| **AVGO** | STOCK | 8.0000 | $381.31 | $364.88 | $2,919.03 | 🔴 $-131.47 | -4.31% |
| **BTC/USD** | CRYPTO | 0.1768 | $64,498.90 | $59,991.60 | $10,608.30 | 🔴 $-797.03 | -6.99% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,571.49 | $985.70 | 🔴 $-345.49 | -25.95% |
| **GOOGL** | STOCK | 16.00 | $354.13 | $338.24 | $5,411.84 | 🔴 $-254.32 | -4.49% |
| **LLY** | STOCK | 11.00 | $1,126.41 | $1,211.60 | $13,327.60 | 🟢 +$937.09 | +7.56% |
| **META** | STOCK | 17.00 | $578.39 | $551.22 | $9,370.69 | 🔴 $-461.99 | -4.70% |
| **MSFT** | STOCK | 25.00 | $404.92 | $371.62 | $9,290.50 | 🔴 $-832.57 | -8.22% |
| **NVDA** | STOCK | 120.00 | $220.11 | $192.16 | $23,059.20 | 🔴 $-3,353.79 | -12.70% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $72.15 | $1,112.48 | 🔴 $-215.90 | -16.25% |
| **SPY** | STOCK | 6.0000 | $745.44 | $730.76 | $4,384.55 | 🔴 $-88.11 | -1.97% |
| **TSLA** | STOCK | 24.00 | $432.23 | $377.48 | $9,059.52 | 🔴 $-1,314.05 | -12.67% |
| **VTI** | ETF | 10.00 | $366.36 | $362.38 | $3,623.80 | 🔴 $-39.80 | -1.09% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $192.53 | 🔴 -1.64% | **BUY** | 96% |
| 2 | **AAPL** | Apple Inc. | STOCK | $283.78 | 🟢 +3.14% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $337.39 | 🔴 -1.84% | **BUY** | 99% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $372.97 | 🟢 +5.71% | **SELL** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $232.69 | 🟢 +2.50% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $362.22 | 🔴 -0.48% | **BUY** | 75% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $365.02 | 🔴 -3.67% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $550.25 | 🟢 +1.36% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $59,937.77 | 🟢 +0.40% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,208.12 | 🟢 +7.13% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-1.64%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 71% | Extreme gain today (+3.14%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 85% | Moderate negative momentum (-1.84%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 78% | Extreme gain today (+5.71%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 68% | Extreme gain today (+2.50%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 66% | Moderate negative momentum (-0.48%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 73% | Extreme loss today (-3.67%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.36%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.40%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 78% | Extreme gain today (+7.13%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
