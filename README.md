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

> 🕐 **Last updated:** 2026-06-10 21:54 UTC &nbsp;|&nbsp; **Trades today:** 9 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$92,023.44` |
| 💸 Cash Available    | `$17,613.69` |
| 🧾 Buying Power      | `$248,519.63` |
| 🔴 Total P&L | `$-6,921.27` &nbsp; `(-69.21%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-6,921.27` (-69.21%)
- **Yesterday-to-today P&L:** `$-1,600.32`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **VTI** | BUY | 94% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 79% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 49.00 | $309.88 | $291.66 | $14,291.34 | 🔴 $-892.76 | -5.88% |
| **AMZN** | STOCK | 12.00 | $247.48 | $237.32 | $2,847.84 | 🔴 $-121.97 | -4.11% |
| **AVGO** | STOCK | 8.0000 | $397.17 | $371.00 | $2,968.00 | 🔴 $-209.32 | -6.59% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $61,178.46 | $1,563.09 | 🔴 $-326.40 | -17.27% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,608.80 | $1,009.10 | 🔴 $-322.09 | -24.20% |
| **GOOGL** | STOCK | 5.0000 | $365.74 | $355.86 | $1,779.30 | 🔴 $-49.41 | -2.70% |
| **LLY** | STOCK | 1.0000 | $1,155.00 | $1,133.68 | $1,133.68 | 🔴 $-21.32 | -1.85% |
| **META** | STOCK | 10.00 | $609.51 | $570.50 | $5,705.00 | 🔴 $-390.11 | -6.40% |
| **MSFT** | STOCK | 12.00 | $433.91 | $397.74 | $4,772.94 | 🔴 $-434.01 | -8.34% |
| **NVDA** | STOCK | 98.00 | $224.42 | $200.00 | $19,600.00 | 🔴 $-2,393.22 | -10.88% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $62.48 | $963.30 | 🔴 $-365.08 | -27.48% |
| **SPY** | STOCK | 6.0000 | $745.44 | $724.63 | $4,347.78 | 🔴 $-124.88 | -2.79% |
| **TSLA** | STOCK | 24.00 | $432.23 | $380.70 | $9,136.80 | 🔴 $-1,236.77 | -11.92% |
| **VTI** | ETF | 3.0000 | $369.03 | $357.72 | $1,073.16 | 🔴 $-33.93 | -3.07% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $200.42 | 🔴 -3.73% | **BUY** | 100% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $356.38 | 🔴 -2.16% | **BUY** | 100% |
| 3 | **AAPL** | Apple Inc. | STOCK | $291.58 | 🟢 +0.35% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $397.36 | 🔴 -1.50% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $238.00 | 🔴 -2.53% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $358.04 | 🔴 -1.55% | **BUY** | 94% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $372.10 | 🔴 -5.12% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $570.98 | 🔴 -2.33% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,168.79 | 🔴 -0.85% | **BUY** | 79% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,136.37 | 🔴 -0.73% | **BUY** | 79% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 74% | Extreme loss today (-3.73%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 85% | Moderate negative momentum (-2.16%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.35%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.50%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 68% | Extreme loss today (-2.53%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 83% | Moderate negative momentum (-1.55%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 78% | Extreme loss today (-5.12%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-2.33%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 70% | Moderate negative momentum (-0.85%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 69% | Moderate negative momentum (-0.73%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
