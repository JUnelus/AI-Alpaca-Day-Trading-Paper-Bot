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

> 🕐 **Last updated:** 2026-07-08 14:35 UTC &nbsp;|&nbsp; **Trades today:** 9 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$96,427.59` |
| 💸 Cash Available    | `$-36,269.60` |
| 🧾 Buying Power      | `$170,955.94` |
| 🟢 Total P&L | `+$12,881.11` &nbsp; `(+128.81%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$12,881.11` (+128.81%)
- **Yesterday-to-today P&L:** `$-927.34`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 97% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **META** | BUY | 98% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 74% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 50.00 | $305.42 | $309.47 | $15,473.50 | 🟢 +$202.59 | +1.33% |
| **AMZN** | STOCK | 28.00 | $237.74 | $242.26 | $6,783.28 | 🟢 +$126.64 | +1.90% |
| **AVGO** | STOCK | 12.00 | $374.95 | $387.44 | $4,649.28 | 🟢 +$149.86 | +3.33% |
| **BTC/USD** | CRYPTO | 0.2114 | $4,965.95 | $61,896.47 | $13,087.57 | 🟢 +$12,037.56 | +1146.42% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,736.10 | $1,088.95 | 🟢 +$1,088.95 | 0.00% |
| **GOOGL** | STOCK | 16.00 | $352.54 | $361.65 | $5,786.40 | 🟢 +$145.80 | +2.58% |
| **LLY** | STOCK | 16.00 | $1,151.91 | $1,231.28 | $19,700.48 | 🟢 +$1,269.91 | +6.89% |
| **META** | STOCK | 18.00 | $572.09 | $603.94 | $10,870.92 | 🟢 +$573.33 | +5.57% |
| **MSFT** | STOCK | 24.00 | $393.23 | $382.32 | $9,175.80 | 🔴 $-261.67 | -2.77% |
| **NVDA** | STOCK | 132.00 | $217.83 | $197.18 | $26,027.76 | 🔴 $-2,726.34 | -9.48% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.75 | $1,183.43 | 🟢 +$1,183.43 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $743.06 | $4,458.36 | 🔴 $-14.30 | -0.32% |
| **TSLA** | STOCK | 24.00 | $432.23 | $394.53 | $9,468.72 | 🔴 $-904.85 | -8.72% |
| **VTI** | ETF | 12.00 | $366.29 | $367.14 | $4,405.68 | 🟢 +$10.20 | +0.23% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $197.17 | 🟢 +0.12% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $309.60 | 🔴 -0.34% | **BUY** | 74% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $361.89 | 🔴 -1.40% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $382.69 | 🔴 -1.58% | **BUY** | 97% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $242.60 | 🔴 -1.37% | **BUY** | 85% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $367.36 | 🔴 -0.61% | **BUY** | 77% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $387.25 | 🟢 +4.44% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $604.25 | 🔴 -1.84% | **BUY** | 98% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,939.56 | 🔴 -2.20% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,230.34 | 🔴 -0.42% | **BUY** | 74% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.12%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.34%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.40%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.58%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Moderate negative momentum (-1.37%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 68% | Moderate negative momentum (-0.61%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 77% | Extreme gain today (+4.44%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-1.84%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.20%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 65% | Moderate negative momentum (-0.42%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
