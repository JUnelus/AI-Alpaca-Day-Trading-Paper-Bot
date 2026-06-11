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

> 🕐 **Last updated:** 2026-06-11 14:59 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$91,879.35` |
| 💸 Cash Available    | `$13,548.13` |
| 🧾 Buying Power      | `$244,925.85` |
| 🔴 Total P&L | `$-7,065.35` &nbsp; `(-70.65%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-7,065.35` (-70.65%)
- **Yesterday-to-today P&L:** `$-144.08`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 49.00 | $309.88 | $289.92 | $14,206.08 | 🔴 $-978.03 | -6.44% |
| **AMZN** | STOCK | 14.00 | $245.98 | $235.81 | $3,301.34 | 🔴 $-142.42 | -4.14% |
| **AVGO** | STOCK | 9.0000 | $394.67 | $374.02 | $3,366.22 | 🔴 $-185.77 | -5.23% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $62,834.74 | $1,605.40 | 🔴 $-284.08 | -15.04% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,649.88 | $1,034.87 | 🔴 $-296.32 | -22.26% |
| **GOOGL** | STOCK | 6.0000 | $363.74 | $346.86 | $2,081.16 | 🔴 $-101.29 | -4.64% |
| **LLY** | STOCK | 2.0000 | $1,150.72 | $1,162.44 | $2,324.88 | 🟢 +$23.43 | +1.02% |
| **META** | STOCK | 11.00 | $605.17 | $558.23 | $6,140.53 | 🔴 $-516.35 | -7.76% |
| **MSFT** | STOCK | 13.00 | $430.65 | $387.07 | $5,031.91 | 🔴 $-566.49 | -10.12% |
| **NVDA** | STOCK | 100.00 | $223.97 | $200.24 | $20,024.00 | 🔴 $-2,373.39 | -10.60% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $63.83 | $984.14 | 🔴 $-344.24 | -25.91% |
| **SPY** | STOCK | 6.0000 | $745.44 | $725.65 | $4,353.90 | 🔴 $-118.76 | -2.66% |
| **TSLA** | STOCK | 24.00 | $432.23 | $384.38 | $9,225.00 | 🔴 $-1,148.57 | -11.07% |
| **VTI** | ETF | 4.0000 | $366.61 | $358.34 | $1,433.36 | 🔴 $-33.07 | -2.26% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $200.03 | 🔴 -0.20% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $289.69 | 🔴 -0.65% | **BUY** | 79% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $346.79 | 🔴 -2.69% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $386.85 | 🔴 -2.64% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $235.62 | 🔴 -1.00% | **BUY** | 84% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $358.21 | 🟢 +0.05% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $373.76 | 🟢 +0.45% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $557.88 | 🔴 -2.29% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,698.48 | 🟢 +2.03% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,162.17 | 🟢 +2.27% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.20%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **SELL** | 70% | Moderate negative momentum (-0.65%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 68% | Extreme loss today (-2.69%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 68% | Extreme loss today (-2.64%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 74% | Moderate negative momentum (-1.00%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.05%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+0.45%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-2.29%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+2.03%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+2.27%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
