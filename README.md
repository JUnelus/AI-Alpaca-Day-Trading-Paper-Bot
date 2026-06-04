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

> 🕐 **Last updated:** 2026-06-04 21:50 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$97,060.68` |
| 💸 Cash Available    | `$36,480.91` |
| 🧾 Buying Power      | `$257,572.70` |
| 🔴 Total P&L | `$-1,873.55` &nbsp; `(-18.74%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,873.55` (-18.74%)
- **Yesterday-to-today P&L:** `+$169.56`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 84% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 44.00 | $311.04 | $311.48 | $13,705.02 | 🟢 +$19.43 | +0.14% |
| **AMZN** | STOCK | 2.0000 | $252.84 | $253.86 | $507.72 | 🟢 +$2.05 | +0.41% |
| **AVGO** | STOCK | 2.0000 | $410.99 | $417.51 | $835.02 | 🟢 +$13.05 | +1.59% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $63,490.20 | $1,108.65 | 🔴 $-244.74 | -18.08% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,766.40 | $1,107.96 | 🔴 $-223.23 | -16.77% |
| **GOOGL** | STOCK | 1.0000 | $363.26 | $372.30 | $372.30 | 🟢 +$9.04 | +2.49% |
| **META** | STOCK | 6.0000 | $618.45 | $626.25 | $3,757.50 | 🟢 +$46.81 | +1.26% |
| **MSFT** | STOCK | 6.0000 | $457.79 | $427.85 | $2,567.10 | 🔴 $-179.65 | -6.54% |
| **NVDA** | STOCK | 90.00 | $225.81 | $217.45 | $19,570.50 | 🔴 $-752.38 | -3.70% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $67.95 | $1,047.71 | 🔴 $-280.67 | -21.13% |
| **SPY** | STOCK | 6.0000 | $744.36 | $756.02 | $4,536.12 | 🟢 +$69.98 | +1.57% |
| **TSLA** | STOCK | 24.00 | $432.23 | $417.41 | $10,017.84 | 🔴 $-355.73 | -3.43% |
| **VTI** | ETF | 1.0000 | $370.55 | $373.05 | $373.05 | 🟢 +$2.50 | +0.67% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $218.66 | 🟢 +1.82% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $311.23 | 🟢 +0.31% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $372.19 | 🟢 +3.68% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $428.05 | 🟢 +0.17% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $253.79 | 🟢 +1.51% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $373.38 | 🟢 +0.47% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $418.91 | 🔴 -12.59% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $627.57 | 🟢 +0.74% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,347.50 | 🔴 -1.09% | **BUY** | 84% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,125.27 | 🟢 +4.31% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.82%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.31%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 73% | Extreme gain today (+3.68%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.17%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.51%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.47%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 78% | Extreme loss today (-12.59%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.74%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 74% | Moderate negative momentum (-1.09%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 77% | Extreme gain today (+4.31%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
