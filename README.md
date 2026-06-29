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

> 🕐 **Last updated:** 2026-06-29 14:56 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$92,281.87` |
| 💸 Cash Available    | `$-25,189.23` |
| 🧾 Buying Power      | `$184,971.90` |
| 🔴 Total P&L | `$-6,759.64` &nbsp; `(-67.60%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-6,759.64` (-67.60%)
- **Yesterday-to-today P&L:** `+$1,843.29`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 78% | DCA buy: quality asset on a mild dip |
| **AMZN** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 58.00 | $306.80 | $282.20 | $16,367.60 | 🔴 $-1,426.94 | -8.02% |
| **AMZN** | STOCK | 32.00 | $240.18 | $245.51 | $7,856.32 | 🟢 +$170.49 | +2.22% |
| **AVGO** | STOCK | 9.0000 | $380.51 | $370.17 | $3,331.53 | 🔴 $-93.06 | -2.72% |
| **BTC/USD** | CRYPTO | 0.1768 | $64,498.90 | $59,273.21 | $10,481.26 | 🔴 $-924.06 | -8.10% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,568.02 | $983.52 | 🔴 $-347.67 | -26.12% |
| **GOOGL** | STOCK | 17.00 | $353.61 | $350.55 | $5,959.35 | 🔴 $-51.99 | -0.86% |
| **LLY** | STOCK | 10.00 | $1,123.81 | $1,218.25 | $12,182.50 | 🟢 +$944.39 | +8.40% |
| **META** | STOCK | 17.00 | $578.39 | $566.24 | $9,626.08 | 🔴 $-206.60 | -2.10% |
| **MSFT** | STOCK | 21.00 | $404.92 | $373.65 | $7,846.76 | 🔴 $-656.62 | -7.72% |
| **NVDA** | STOCK | 122.00 | $219.68 | $194.41 | $23,718.02 | 🔴 $-3,083.09 | -11.50% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $73.56 | $1,134.14 | 🔴 $-194.24 | -14.62% |
| **SPY** | STOCK | 6.0000 | $745.44 | $737.66 | $4,425.96 | 🔴 $-46.70 | -1.04% |
| **TSLA** | STOCK | 24.00 | $432.23 | $397.45 | $9,538.80 | 🔴 $-834.77 | -8.05% |
| **VTI** | ETF | 11.00 | $366.18 | $365.38 | $4,019.17 | 🔴 $-8.79 | -0.22% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $194.29 | 🟢 +0.91% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $350.50 | 🟢 +3.89% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $282.18 | 🔴 -0.56% | **BUY** | 78% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $374.06 | 🟢 +0.29% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $245.55 | 🟢 +5.53% | **SELL** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.41 | 🟢 +0.88% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $370.05 | 🟢 +1.38% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $566.33 | 🟢 +2.92% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $59,403.14 | 🔴 -0.12% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,220.13 | 🟢 +0.99% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+0.91%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 74% | Extreme gain today (+3.89%) — mean reversion pullback likely |
| 3 | **AAPL** | Apple Inc. | **SELL** | 69% | Moderate negative momentum (-0.56%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.29%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 78% | Extreme gain today (+5.53%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.88%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.38%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 70% | Extreme gain today (+2.92%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.12%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.99%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
