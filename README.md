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

> 🕐 **Last updated:** 2026-08-20 14:00 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$108,339.17` |
| 💸 Cash Available    | `$-107,611.91` |
| 🧾 Buying Power      | `$99,106.89` |
| 🟢 Total P&L | `+$21,731.61` &nbsp; `(+217.32%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$21,731.61` (+217.32%)
- **Yesterday-to-today P&L:** `+$535.13`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 82% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $317.51 | $21,272.92 | 🟢 +$673.59 | +3.27% |
| **AMZN** | STOCK | 51.00 | $248.09 | $262.85 | $13,405.09 | 🟢 +$752.50 | +5.95% |
| **AVGO** | STOCK | 18.00 | $385.06 | $363.23 | $6,538.14 | 🔴 $-392.99 | -5.67% |
| **BTC/USD** | CRYPTO | 0.2889 | $20,769.05 | $71,691.60 | $20,711.34 | 🟢 +$14,711.27 | +245.18% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,276.41 | $1,427.86 | 🟢 +$1,427.86 | 0.00% |
| **GOOGL** | STOCK | 29.00 | $352.18 | $343.05 | $9,948.45 | 🔴 $-264.77 | -2.59% |
| **LLY** | STOCK | 39.00 | $1,168.68 | $1,272.58 | $49,630.62 | 🟢 +$4,052.12 | +8.89% |
| **META** | STOCK | 33.00 | $591.43 | $547.39 | $18,064.03 | 🔴 $-1,453.15 | -7.45% |
| **MSFT** | STOCK | 30.00 | $412.13 | $481.71 | $14,451.30 | 🟢 +$2,087.52 | +16.88% |
| **NVDA** | STOCK | 169.00 | $214.73 | $217.82 | $36,812.43 | 🟢 +$523.41 | +1.44% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $86.96 | $1,340.82 | 🟢 +$1,340.82 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $766.74 | $4,600.44 | 🟢 +$127.78 | +2.86% |
| **TSLA** | STOCK | 24.00 | $432.23 | $344.94 | $8,278.56 | 🔴 $-2,095.01 | -20.20% |
| **VTI** | ETF | 25.00 | $369.04 | $378.67 | $9,466.62 | 🟢 +$240.69 | +2.61% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $217.69 | 🟢 +0.06% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $317.28 | 🟢 +0.14% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $343.11 | 🔴 -0.47% | **BUY** | 76% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $481.37 | 🔴 -0.61% | **BUY** | 79% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $262.90 | 🔴 -1.10% | **BUY** | 85% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $378.58 | 🔴 -0.37% | **BUY** | 73% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $363.30 | 🟢 +0.23% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $71,633.50 | 🟢 +3.35% | HOLD | — |
| 9 | **META** | Meta Platforms Inc. | STOCK | $547.67 | 🟢 +0.30% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,268.94 | 🔴 -0.89% | **BUY** | 82% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.06%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.14%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 67% | Moderate negative momentum (-0.47%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 69% | Moderate negative momentum (-0.61%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Moderate negative momentum (-1.10%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.37%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (+0.23%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 72% | Extreme gain today (+3.35%) — mean reversion pullback likely |
| 9 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.30%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 72% | Moderate negative momentum (-0.89%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
