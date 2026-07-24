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

> 🕐 **Last updated:** 2026-07-24 21:37 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,364.25` |
| 💸 Cash Available    | `$-76,299.09` |
| 🧾 Buying Power      | `$111,253.85` |
| 🟢 Total P&L | `+$11,219.65` &nbsp; `(+112.20%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$11,219.65` (+112.20%)
- **Yesterday-to-today P&L:** `$-234.78`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 98% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $333.57 | $17,679.22 | 🟢 +$1,405.34 | +8.64% |
| **AMZN** | STOCK | 52.00 | $240.57 | $231.89 | $12,058.36 | 🔴 $-451.43 | -3.61% |
| **AVGO** | STOCK | 14.00 | $379.41 | $382.99 | $5,361.90 | 🟢 +$50.11 | +0.94% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $64,153.30 | $17,820.29 | 🟢 +$12,574.52 | +239.71% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,860.00 | $1,166.67 | 🟢 +$1,166.67 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $320.09 | $8,962.49 | 🔴 $-921.48 | -9.32% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,196.00 | $32,292.00 | 🟢 +$919.97 | +2.93% |
| **META** | STOCK | 23.00 | $600.93 | $595.99 | $13,707.77 | 🔴 $-113.63 | -0.82% |
| **MSFT** | STOCK | 33.00 | $391.33 | $381.60 | $12,592.90 | 🔴 $-321.07 | -2.49% |
| **NVDA** | STOCK | 145.00 | $215.77 | $206.97 | $30,010.56 | 🔴 $-1,275.92 | -4.08% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.58 | $1,134.58 | 🟢 +$1,134.58 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $739.12 | $4,434.72 | 🔴 $-37.94 | -0.85% |
| **TSLA** | STOCK | 24.00 | $432.23 | $313.04 | $7,512.96 | 🔴 $-2,860.61 | -27.58% |
| **VTI** | ETF | 19.00 | $367.28 | $364.68 | $6,928.92 | 🔴 $-49.47 | -0.71% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $206.84 | 🔴 -0.92% | **BUY** | 83% |
| 2 | **AAPL** | Apple Inc. | STOCK | $333.02 | 🟢 +3.53% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $319.74 | 🟢 +0.65% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $381.70 | 🟢 +0.03% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $232.11 | 🔴 -0.66% | **BUY** | 79% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $364.80 | 🟢 +0.03% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $381.92 | 🔴 -2.69% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $595.19 | 🔴 -1.80% | **BUY** | 98% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,128.86 | 🔴 -1.44% | **BUY** | 85% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,196.03 | 🟢 +0.86% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 73% | Moderate negative momentum (-0.92%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 73% | Extreme gain today (+3.53%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.65%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.03%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 69% | Moderate negative momentum (-0.66%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.03%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 68% | Extreme loss today (-2.69%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-1.80%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 75% | Moderate negative momentum (-1.44%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.86%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
