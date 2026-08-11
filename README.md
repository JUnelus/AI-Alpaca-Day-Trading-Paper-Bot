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

> 🕐 **Last updated:** 2026-08-11 21:29 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$105,138.25` |
| 💸 Cash Available    | `$-86,914.84` |
| 🧾 Buying Power      | `$118,825.34` |
| 🟢 Total P&L | `+$18,934.00` &nbsp; `(+189.34%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$18,934.00` (+189.34%)
- **Yesterday-to-today P&L:** `$-1,443.38`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 64.00 | $307.64 | $304.95 | $19,516.80 | 🔴 $-172.32 | -0.88% |
| **AMZN** | STOCK | 40.00 | $243.84 | $272.42 | $10,896.80 | 🟢 +$1,143.33 | +11.72% |
| **AVGO** | STOCK | 11.00 | $384.11 | $416.36 | $4,579.96 | 🟢 +$354.74 | +8.40% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $63,559.97 | $19,728.69 | 🟢 +$12,384.83 | +168.64% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,882.60 | $1,180.84 | 🟢 +$1,180.84 | 0.00% |
| **GOOGL** | STOCK | 24.00 | $354.03 | $344.80 | $8,275.17 | 🔴 $-221.64 | -2.61% |
| **LLY** | STOCK | 35.00 | $1,163.09 | $1,215.00 | $42,525.00 | 🟢 +$1,816.86 | +4.46% |
| **META** | STOCK | 26.00 | $597.38 | $599.63 | $15,590.38 | 🟢 +$58.49 | +0.38% |
| **MSFT** | STOCK | 25.00 | $396.33 | $501.62 | $12,540.50 | 🟢 +$2,632.29 | +26.57% |
| **NVDA** | STOCK | 161.00 | $214.48 | $217.80 | $35,065.80 | 🟢 +$534.46 | +1.55% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.83 | $1,169.21 | 🟢 +$1,169.21 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $770.87 | $4,625.22 | 🟢 +$152.56 | +3.41% |
| **TSLA** | STOCK | 24.00 | $432.23 | $332.73 | $7,985.52 | 🔴 $-2,388.05 | -23.02% |
| **VTI** | ETF | 22.00 | $367.49 | $380.60 | $8,373.20 | 🟢 +$288.41 | +3.57% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $217.50 | 🔴 -0.02% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $304.91 | 🔴 -1.09% | **BUY** | 85% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $343.80 | 🔴 -3.84% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $503.81 | 🔴 -0.44% | **BUY** | 76% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $272.27 | 🔴 -2.09% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $380.65 | 🔴 -0.26% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $416.08 | 🔴 -1.50% | **BUY** | 85% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $599.12 | 🟢 +0.71% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,626.58 | 🔴 -0.45% | **BUY** | 73% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,215.02 | 🔴 -1.37% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.02%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.09%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 74% | Extreme loss today (-3.84%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 67% | Moderate negative momentum (-0.44%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.09%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.26%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 75% | Moderate negative momentum (-1.50%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.71%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 64% | Moderate negative momentum (-0.45%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 75% | Moderate negative momentum (-1.37%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
