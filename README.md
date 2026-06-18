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

> 🕐 **Last updated:** 2026-06-18 14:42 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,830.56` |
| 💸 Cash Available    | `$-4,821.50` |
| 🧾 Buying Power      | `$221,478.38` |
| 🔴 Total P&L | `$-5,069.73` &nbsp; `(-50.70%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,069.73` (-50.70%)
- **Yesterday-to-today P&L:** `+$120.01`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **BTC/USD** | BUY | 80% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $308.65 | $299.28 | $15,861.84 | 🔴 $-496.70 | -3.04% |
| **AMZN** | STOCK | 24.00 | $243.35 | $239.73 | $5,753.52 | 🔴 $-87.00 | -1.49% |
| **AVGO** | STOCK | 7.0000 | $386.50 | $408.15 | $2,857.05 | 🟢 +$151.53 | +5.60% |
| **BTC/USD** | CRYPTO | 0.0742 | $68,126.31 | $63,940.30 | $4,747.18 | 🔴 $-310.79 | -6.14% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,739.20 | $1,090.90 | 🔴 $-240.30 | -18.05% |
| **GOOGL** | STOCK | 9.0000 | $362.27 | $363.08 | $3,267.72 | 🟢 +$7.28 | +0.22% |
| **LLY** | STOCK | 8.0000 | $1,136.10 | $1,097.40 | $8,779.20 | 🔴 $-309.59 | -3.41% |
| **META** | STOCK | 12.00 | $588.59 | $569.69 | $6,836.23 | 🔴 $-226.83 | -3.21% |
| **MSFT** | STOCK | 20.00 | $415.30 | $377.97 | $7,559.40 | 🔴 $-746.65 | -8.99% |
| **NVDA** | STOCK | 106.00 | $223.07 | $208.85 | $22,138.63 | 🔴 $-1,507.17 | -6.37% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $71.26 | $1,098.76 | 🔴 $-229.62 | -17.29% |
| **SPY** | STOCK | 6.0000 | $745.44 | $745.97 | $4,475.82 | 🟢 +$3.16 | +0.07% |
| **TSLA** | STOCK | 24.00 | $432.23 | $386.98 | $9,287.52 | 🔴 $-1,086.05 | -10.47% |
| **VTI** | ETF | 6.0000 | $367.86 | $369.36 | $2,216.13 | 🟢 +$9.00 | +0.41% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.92 | 🟢 +2.09% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $363.02 | 🔴 -0.21% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $299.30 | 🟢 +1.13% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $377.93 | 🔴 -0.26% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $239.79 | 🟢 +0.96% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $369.42 | 🟢 +1.00% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $408.10 | 🟢 +3.87% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $569.66 | 🟢 +0.37% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,889.58 | 🔴 -0.85% | **BUY** | 80% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,097.17 | 🔴 -1.33% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+2.09%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.21%) — no trend to carry forward |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.13%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.26%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.96%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.00%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 74% | Extreme gain today (+3.87%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.37%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 70% | Moderate negative momentum (-0.85%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 75% | Moderate negative momentum (-1.33%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
