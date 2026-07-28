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

> 🕐 **Last updated:** 2026-07-28 21:37 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,422.08` |
| 💸 Cash Available    | `$-81,028.49` |
| 🧾 Buying Power      | `$107,468.90` |
| 🟢 Total P&L | `+$11,277.50` &nbsp; `(+112.77%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$11,277.50` (+112.77%)
- **Yesterday-to-today P&L:** `+$773.01`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AVGO** | BUY | 77% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $339.90 | $18,014.70 | 🟢 +$1,740.83 | +10.70% |
| **AMZN** | STOCK | 58.00 | $239.64 | $231.20 | $13,409.60 | 🔴 $-489.60 | -3.52% |
| **AVGO** | STOCK | 17.00 | $379.48 | $380.95 | $6,476.15 | 🟢 +$25.02 | +0.39% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $63,849.04 | $17,735.78 | 🟢 +$12,490.01 | +238.10% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,917.20 | $1,202.54 | 🟢 +$1,202.54 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $334.33 | $9,361.28 | 🔴 $-522.69 | -5.29% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,220.24 | $32,946.48 | 🟢 +$1,574.45 | +5.02% |
| **META** | STOCK | 24.00 | $601.30 | $594.33 | $14,263.92 | 🔴 $-167.20 | -1.16% |
| **MSFT** | STOCK | 33.00 | $391.33 | $394.08 | $13,004.64 | 🟢 +$90.67 | +0.70% |
| **NVDA** | STOCK | 153.00 | $214.88 | $197.00 | $30,141.00 | 🔴 $-2,736.39 | -8.32% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.91 | $1,139.66 | 🟢 +$1,139.66 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $741.17 | $4,447.02 | 🔴 $-25.64 | -0.57% |
| **TSLA** | STOCK | 24.00 | $432.23 | $306.20 | $7,348.86 | 🔴 $-3,024.71 | -29.16% |
| **VTI** | ETF | 19.00 | $367.28 | $366.26 | $6,958.94 | 🔴 $-19.45 | -0.28% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $340.08 | 🟢 +0.94% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $197.01 | 🟢 +0.25% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $333.71 | 🟢 +2.19% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $393.35 | 🟢 +1.09% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $230.86 | 🔴 -0.23% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.99 | 🟢 +0.22% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $380.91 | 🔴 -0.60% | **BUY** | 77% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $593.41 | 🔴 -0.08% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,918.00 | 🟢 +0.34% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,220.66 | 🟢 +1.93% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.94%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.25%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+2.19%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.09%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.23%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.22%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 68% | Moderate negative momentum (-0.60%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.08%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.34%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.93%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
