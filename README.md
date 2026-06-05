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

> 🕐 **Last updated:** 2026-06-05 14:40 UTC &nbsp;|&nbsp; **Trades today:** 8 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$96,022.67` |
| 💸 Cash Available    | `$35,037.26` |
| 🧾 Buying Power      | `$247,533.26` |
| 🔴 Total P&L | `$-2,923.02` &nbsp; `(-29.23%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-2,923.02` (-29.23%)
- **Yesterday-to-today P&L:** `$-1,049.46`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 44.00 | $311.29 | $313.69 | $13,802.58 | 🟢 +$105.69 | +0.77% |
| **AMZN** | STOCK | 4.0000 | $252.71 | $252.54 | $1,010.18 | 🔴 $-0.65 | -0.06% |
| **AVGO** | STOCK | 4.0000 | $407.01 | $401.58 | $1,606.32 | 🔴 $-21.74 | -1.34% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $60,882.10 | $1,063.11 | 🔴 $-290.28 | -21.45% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,615.58 | $1,013.36 | 🔴 $-317.84 | -23.88% |
| **GOOGL** | STOCK | 1.0000 | $363.26 | $369.15 | $369.15 | 🟢 +$5.89 | +1.62% |
| **META** | STOCK | 6.0000 | $618.45 | $615.42 | $3,692.52 | 🔴 $-18.17 | -0.49% |
| **MSFT** | STOCK | 6.0000 | $456.34 | $421.85 | $2,531.07 | 🔴 $-206.94 | -7.56% |
| **NVDA** | STOCK | 90.00 | $225.84 | $211.51 | $19,036.35 | 🔴 $-1,288.91 | -6.34% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $65.40 | $1,008.39 | 🔴 $-319.99 | -24.09% |
| **SPY** | STOCK | 6.0000 | $745.44 | $750.01 | $4,500.06 | 🟢 +$27.40 | +0.61% |
| **TSLA** | STOCK | 24.00 | $432.23 | $407.37 | $9,776.88 | 🔴 $-596.69 | -5.75% |
| **VTI** | ETF | 2.0000 | $370.14 | $369.75 | $739.50 | 🔴 $-0.78 | -0.11% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $211.81 | 🔴 -3.13% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $313.83 | 🟢 +0.84% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $368.78 | 🔴 -0.92% | **BUY** | 83% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $421.86 | 🔴 -1.45% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $252.70 | 🔴 -0.43% | **BUY** | 75% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $369.80 | 🔴 -0.96% | **BUY** | 83% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $401.89 | 🔴 -4.06% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $614.87 | 🔴 -2.02% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $60,865.18 | 🔴 -4.61% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,158.11 | 🟢 +2.92% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 71% | Extreme loss today (-3.13%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.84%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 73% | Moderate negative momentum (-0.92%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.45%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 66% | Moderate negative momentum (-0.43%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 73% | Moderate negative momentum (-0.96%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 75% | Extreme loss today (-4.06%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-2.02%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 78% | Extreme loss today (-4.61%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 70% | Extreme gain today (+2.92%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
