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

> 🕐 **Last updated:** 2026-07-13 14:39 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,347.54` |
| 💸 Cash Available    | `$-44,744.17` |
| 🧾 Buying Power      | `$165,628.38` |
| 🟢 Total P&L | `+$15,218.82` &nbsp; `(+152.19%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$15,218.82` (+152.19%)
- **Yesterday-to-today P&L:** `$-1,083.42`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 97% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 72% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $305.69 | $318.75 | $16,575.26 | 🟢 +$679.33 | +4.27% |
| **AMZN** | STOCK | 38.00 | $239.13 | $246.61 | $9,371.18 | 🟢 +$284.16 | +3.13% |
| **AVGO** | STOCK | 7.0000 | $377.02 | $394.40 | $2,760.80 | 🟢 +$121.64 | +4.61% |
| **BTC/USD** | CRYPTO | 0.2368 | $11,089.02 | $62,491.80 | $14,796.77 | 🟢 +$12,171.12 | +463.55% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,771.51 | $1,111.16 | 🟢 +$1,111.16 | 0.00% |
| **GOOGL** | STOCK | 22.00 | $353.62 | $354.79 | $7,805.38 | 🟢 +$25.75 | +0.33% |
| **LLY** | STOCK | 20.00 | $1,162.39 | $1,184.48 | $23,689.70 | 🟢 +$441.86 | +1.90% |
| **META** | STOCK | 15.00 | $575.02 | $658.30 | $9,874.50 | 🟢 +$1,249.20 | +14.48% |
| **MSFT** | STOCK | 28.00 | $391.24 | $385.88 | $10,804.78 | 🔴 $-149.83 | -1.37% |
| **NVDA** | STOCK | 130.00 | $217.29 | $208.15 | $27,059.50 | 🔴 $-1,188.56 | -4.21% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.82 | $1,169.05 | 🟢 +$1,169.05 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $752.20 | $4,513.20 | 🟢 +$40.54 | +0.91% |
| **TSLA** | STOCK | 24.00 | $432.23 | $398.70 | $9,568.92 | 🔴 $-804.65 | -7.76% |
| **VTI** | ETF | 14.00 | $366.54 | $371.40 | $5,199.65 | 🟢 +$68.04 | +1.33% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.09 | 🔴 -1.36% | **BUY** | 85% |
| 2 | **AAPL** | Apple Inc. | STOCK | $318.80 | 🟢 +1.10% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $354.84 | 🔴 -0.66% | **BUY** | 79% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $385.94 | 🟢 +0.22% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $246.59 | 🟢 +0.51% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $371.43 | 🔴 -0.34% | **BUY** | 73% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $394.36 | 🔴 -1.40% | **BUY** | 85% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $658.43 | 🔴 -1.61% | **BUY** | 96% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,492.88 | 🔴 -1.97% | **BUY** | 97% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,184.97 | 🔴 -0.30% | **BUY** | 72% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Moderate negative momentum (-1.36%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.10%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 69% | Moderate negative momentum (-0.66%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.22%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.51%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.34%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 75% | Moderate negative momentum (-1.40%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 84% | Moderate negative momentum (-1.61%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-1.97%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.30%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
