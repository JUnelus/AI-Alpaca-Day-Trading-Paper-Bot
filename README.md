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

> 🕐 **Last updated:** 2026-06-08 14:55 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,416.38` |
| 💸 Cash Available    | `$28,537.16` |
| 🧾 Buying Power      | `$277,361.61` |
| 🔴 Total P&L | `$-3,528.35` &nbsp; `(-35.28%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-3,528.35` (-35.28%)
- **Yesterday-to-today P&L:** `+$1,013.94`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 78% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 45.00 | $311.37 | $314.36 | $14,146.22 | 🟢 +$134.53 | +0.96% |
| **AMZN** | STOCK | 6.0000 | $251.09 | $246.63 | $1,479.78 | 🔴 $-26.75 | -1.78% |
| **AVGO** | STOCK | 5.0000 | $405.01 | $397.92 | $1,989.59 | 🔴 $-35.46 | -1.75% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $63,903.87 | $1,632.72 | 🔴 $-256.77 | -13.59% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,687.28 | $1,058.33 | 🔴 $-272.86 | -20.50% |
| **GOOGL** | STOCK | 3.0000 | $365.62 | $363.33 | $1,089.99 | 🔴 $-6.86 | -0.63% |
| **META** | STOCK | 8.0000 | $614.41 | $589.11 | $4,712.88 | 🔴 $-202.39 | -4.12% |
| **MSFT** | STOCK | 8.0000 | $447.10 | $412.46 | $3,299.68 | 🔴 $-277.13 | -7.75% |
| **NVDA** | STOCK | 94.00 | $225.17 | $208.21 | $19,571.65 | 🔴 $-1,594.65 | -7.53% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $67.07 | $1,034.08 | 🔴 $-294.30 | -22.15% |
| **SPY** | STOCK | 6.0000 | $745.44 | $743.97 | $4,463.82 | 🔴 $-8.84 | -0.20% |
| **TSLA** | STOCK | 24.00 | $432.23 | $403.88 | $9,693.12 | 🔴 $-680.45 | -6.56% |
| **VTI** | ETF | 3.0000 | $369.03 | $366.89 | $1,100.68 | 🔴 $-6.41 | -0.58% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.35 | 🟢 +1.59% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $314.55 | 🟢 +2.35% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $363.55 | 🔴 -1.35% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $412.25 | 🔴 -1.06% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $246.64 | 🟢 +0.25% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $367.00 | 🟢 +0.99% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $398.26 | 🟢 +3.25% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $589.28 | 🔴 -0.63% | **BUY** | 78% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,858.36 | 🟢 +0.87% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,169.00 | 🟢 +3.32% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.59%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+2.35%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.35%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.06%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.25%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.99%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 71% | Extreme gain today (+3.25%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 69% | Moderate negative momentum (-0.63%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.87%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 72% | Extreme gain today (+3.32%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
