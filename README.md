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

> 🕐 **Last updated:** 2026-06-24 14:38 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$91,884.76` |
| 💸 Cash Available    | `$-17,523.00` |
| 🧾 Buying Power      | `$197,218.65` |
| 🔴 Total P&L | `$-7,143.20` &nbsp; `(-71.43%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-7,143.20` (-71.43%)
- **Yesterday-to-today P&L:** `$-69.30`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 55.00 | $308.19 | $295.59 | $16,257.45 | 🔴 $-692.96 | -4.09% |
| **AMZN** | STOCK | 28.00 | $241.88 | $237.96 | $6,662.88 | 🔴 $-109.87 | -1.62% |
| **AVGO** | STOCK | 5.0000 | $386.87 | $384.03 | $1,920.15 | 🔴 $-14.19 | -0.73% |
| **BTC/USD** | CRYPTO | 0.1507 | $65,254.65 | $61,230.95 | $9,227.21 | 🔴 $-606.35 | -6.17% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,645.60 | $1,032.19 | 🔴 $-299.01 | -22.46% |
| **GOOGL** | STOCK | 13.00 | $357.33 | $350.43 | $4,555.52 | 🔴 $-89.80 | -1.93% |
| **LLY** | STOCK | 12.00 | $1,126.41 | $1,111.94 | $13,343.34 | 🔴 $-173.58 | -1.28% |
| **META** | STOCK | 14.00 | $584.75 | $560.82 | $7,851.48 | 🔴 $-335.04 | -4.09% |
| **MSFT** | STOCK | 22.00 | $411.30 | $373.12 | $8,208.64 | 🔴 $-840.05 | -9.28% |
| **NVDA** | STOCK | 112.00 | $221.92 | $200.23 | $22,425.47 | 🔴 $-2,429.33 | -9.77% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $69.25 | $1,067.70 | 🔴 $-260.68 | -19.62% |
| **SPY** | STOCK | 6.0000 | $745.44 | $736.81 | $4,420.86 | 🔴 $-51.80 | -1.16% |
| **TSLA** | STOCK | 24.00 | $432.23 | $381.00 | $9,144.00 | 🔴 $-1,229.57 | -11.85% |
| **VTI** | ETF | 9.0000 | $366.75 | $365.53 | $3,289.77 | 🔴 $-10.97 | -0.33% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $200.18 | 🟢 +0.07% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $295.47 | 🟢 +0.40% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $350.43 | 🟢 +1.24% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $373.09 | 🔴 -0.23% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $237.97 | 🟢 +1.65% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.58 | 🟢 +0.52% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $384.15 | 🟢 +1.05% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $561.29 | 🔴 -0.16% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $61,237.82 | 🔴 -2.25% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,111.87 | 🟢 +0.43% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.07%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.40%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.24%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.23%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.65%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.52%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.05%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.16%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.25%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.43%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
