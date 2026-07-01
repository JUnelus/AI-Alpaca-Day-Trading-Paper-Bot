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

> 🕐 **Last updated:** 2026-07-01 21:46 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,332.72` |
| 💸 Cash Available    | `$-28,437.28` |
| 🧾 Buying Power      | `$183,330.68` |
| 🔴 Total P&L | `$-3,472.06` &nbsp; `(-34.72%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-3,472.06` (-34.72%)
- **Yesterday-to-today P&L:** `+$1,792.98`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | SELL | 100% | Take-profit trim after overextended rally |
| **LLY** | BUY | 77% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $305.99 | $293.80 | $17,628.00 | 🔴 $-731.46 | -3.98% |
| **AMZN** | STOCK | 28.00 | $237.74 | $241.70 | $6,767.60 | 🟢 +$110.96 | +1.67% |
| **AVGO** | STOCK | 10.00 | $379.55 | $369.38 | $3,693.80 | 🔴 $-101.68 | -2.68% |
| **BTC/USD** | CRYPTO | 0.1947 | $63,955.48 | $60,778.40 | $11,832.64 | 🔴 $-618.53 | -4.97% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,627.50 | $1,020.83 | 🔴 $-310.36 | -23.31% |
| **GOOGL** | STOCK | 13.00 | $350.09 | $360.20 | $4,682.60 | 🟢 +$131.49 | +2.89% |
| **LLY** | STOCK | 13.00 | $1,139.08 | $1,188.00 | $15,444.00 | 🟢 +$635.90 | +4.29% |
| **META** | STOCK | 16.00 | $577.11 | $613.26 | $9,812.16 | 🟢 +$578.40 | +6.26% |
| **MSFT** | STOCK | 22.00 | $393.63 | $384.56 | $8,460.41 | 🔴 $-199.50 | -2.30% |
| **NVDA** | STOCK | 124.00 | $219.30 | $197.59 | $24,501.16 | 🔴 $-2,691.52 | -9.90% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $78.33 | $1,207.71 | 🔴 $-120.67 | -9.08% |
| **SPY** | STOCK | 6.0000 | $745.44 | $745.19 | $4,471.14 | 🔴 $-1.52 | -0.03% |
| **TSLA** | STOCK | 24.00 | $432.23 | $424.51 | $10,188.24 | 🔴 $-185.33 | -1.79% |
| **VTI** | ETF | 11.00 | $366.18 | $369.06 | $4,059.71 | 🟢 +$31.75 | +0.79% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $197.58 | 🔴 -1.25% | **BUY** | 85% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $361.21 | 🟢 +1.07% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $294.38 | 🟢 +1.73% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $384.28 | 🟢 +3.02% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $241.70 | 🟢 +1.41% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $369.27 | 🔴 -0.21% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $369.34 | 🔴 -2.23% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $612.91 | 🟢 +8.81% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $60,753.57 | 🟢 +3.80% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,191.74 | 🔴 -0.64% | **BUY** | 77% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Moderate negative momentum (-1.25%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.07%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.73%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 70% | Extreme gain today (+3.02%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.41%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.21%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 85% | Moderate negative momentum (-2.23%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 78% | Extreme gain today (+8.81%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 74% | Extreme gain today (+3.80%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 68% | Moderate negative momentum (-0.64%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
