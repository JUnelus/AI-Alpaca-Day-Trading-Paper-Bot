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

> 🕐 **Last updated:** 2026-06-04 14:41 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$96,933.60` |
| 💸 Cash Available    | `$37,426.82` |
| 🧾 Buying Power      | `$260,207.59` |
| 🔴 Total P&L | `$-2,000.62` &nbsp; `(-20.01%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-2,000.62` (-20.01%)
- **Yesterday-to-today P&L:** `+$42.49`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 44.00 | $311.04 | $310.31 | $13,653.42 | 🔴 $-32.17 | -0.24% |
| **AMZN** | STOCK | 2.0000 | $252.84 | $254.07 | $508.15 | 🟢 +$2.48 | +0.49% |
| **AVGO** | STOCK | 1.0000 | $412.31 | $409.68 | $409.68 | 🔴 $-2.63 | -0.64% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $63,868.32 | $1,115.25 | 🔴 $-238.14 | -17.60% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,779.12 | $1,115.93 | 🔴 $-215.26 | -16.17% |
| **GOOGL** | STOCK | 1.0000 | $363.26 | $368.41 | $368.41 | 🟢 +$5.15 | +1.42% |
| **META** | STOCK | 6.0000 | $618.45 | $637.78 | $3,826.68 | 🟢 +$115.99 | +3.13% |
| **MSFT** | STOCK | 6.0000 | $457.79 | $430.33 | $2,581.98 | 🔴 $-164.77 | -6.00% |
| **NVDA** | STOCK | 90.00 | $225.81 | $214.49 | $19,304.10 | 🔴 $-1,018.78 | -5.01% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $69.96 | $1,078.73 | 🔴 $-249.65 | -18.79% |
| **SPY** | STOCK | 6.0000 | $744.36 | $754.16 | $4,524.96 | 🟢 +$58.82 | +1.32% |
| **TSLA** | STOCK | 24.00 | $432.23 | $421.27 | $10,110.48 | 🔴 $-263.09 | -2.54% |
| **VTI** | ETF | 1.0000 | $370.55 | $371.98 | $371.98 | 🟢 +$1.43 | +0.39% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $214.38 | 🔴 -0.17% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $310.33 | 🟢 +0.02% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $368.21 | 🟢 +2.57% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $430.06 | 🟢 +0.64% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $254.01 | 🟢 +1.60% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $371.89 | 🟢 +0.07% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $409.17 | 🔴 -14.62% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $635.85 | 🟢 +2.07% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,902.92 | 🔴 -0.23% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,128.81 | 🟢 +4.64% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.17%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.02%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 68% | Extreme gain today (+2.57%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.64%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.60%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.07%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 78% | Extreme loss today (-14.62%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+2.07%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.23%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 78% | Extreme gain today (+4.64%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
