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

> 🕐 **Last updated:** 2026-07-21 21:38 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,873.87` |
| 💸 Cash Available    | `$-71,107.58` |
| 🧾 Buying Power      | `$128,272.44` |
| 🟢 Total P&L | `+$15,728.00` &nbsp; `(+157.28%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$15,728.00` (+157.28%)
- **Yesterday-to-today P&L:** `+$1,500.66`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 73% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $306.72 | $325.18 | $16,909.36 | 🟢 +$960.05 | +6.02% |
| **AMZN** | STOCK | 48.00 | $240.78 | $247.15 | $11,863.20 | 🟢 +$305.92 | +2.65% |
| **AVGO** | STOCK | 13.00 | $379.10 | $386.21 | $5,020.74 | 🟢 +$92.39 | +1.87% |
| **BTC/USD** | CRYPTO | 0.2698 | $17,502.75 | $66,364.40 | $17,904.90 | 🟢 +$13,182.71 | +279.17% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,926.20 | $1,208.19 | 🟢 +$1,208.19 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $348.50 | $9,758.00 | 🔴 $-125.97 | -1.27% |
| **LLY** | STOCK | 26.00 | $1,162.08 | $1,173.06 | $30,499.56 | 🟢 +$285.52 | +0.94% |
| **META** | STOCK | 22.00 | $599.63 | $642.31 | $14,130.82 | 🟢 +$938.89 | +7.12% |
| **MSFT** | STOCK | 32.00 | $391.38 | $396.69 | $12,694.08 | 🟢 +$169.96 | +1.36% |
| **NVDA** | STOCK | 141.00 | $216.01 | $206.90 | $29,172.90 | 🔴 $-1,284.74 | -4.22% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $77.77 | $1,199.07 | 🟢 +$1,199.07 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $748.12 | $4,488.72 | 🟢 +$16.06 | +0.36% |
| **TSLA** | STOCK | 24.00 | $432.23 | $379.65 | $9,111.60 | 🔴 $-1,261.97 | -12.17% |
| **VTI** | ETF | 19.00 | $367.28 | $369.49 | $7,020.31 | 🟢 +$41.92 | +0.60% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $207.29 | 🟢 +1.97% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $327.74 | 🟢 +0.35% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $347.15 | 🔴 -1.38% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $397.75 | 🔴 -1.13% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $247.55 | 🔴 -0.98% | **BUY** | 84% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $369.45 | 🟢 +0.87% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $386.50 | 🟢 +2.21% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $643.81 | 🔴 -0.32% | **BUY** | 73% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $66,311.79 | 🟢 +1.70% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,175.41 | 🟢 +2.49% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.97%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.35%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.38%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.13%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 74% | Moderate negative momentum (-0.98%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.87%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+2.21%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.32%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.70%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+2.49%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
