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

> 🕐 **Last updated:** 2026-06-16 15:26 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,178.99` |
| 💸 Cash Available    | `$5,305.17` |
| 🧾 Buying Power      | `$242,823.12` |
| 🔴 Total P&L | `$-3,745.78` &nbsp; `(-37.46%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-3,745.78` (-37.46%)
- **Yesterday-to-today P&L:** `$-549.59`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 78% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $308.82 | $298.32 | $15,512.64 | 🔴 $-545.77 | -3.40% |
| **AMZN** | STOCK | 20.00 | $243.99 | $248.92 | $4,978.40 | 🟢 +$98.53 | +2.02% |
| **AVGO** | STOCK | 12.00 | $391.94 | $379.70 | $4,556.46 | 🔴 $-146.83 | -3.12% |
| **BTC/USD** | CRYPTO | 0.0335 | $72,003.08 | $65,744.56 | $2,204.39 | 🔴 $-209.85 | -8.69% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,776.85 | $1,114.51 | 🔴 $-216.68 | -16.28% |
| **GOOGL** | STOCK | 7.0000 | $361.34 | $375.39 | $2,627.73 | 🟢 +$98.38 | +3.89% |
| **LLY** | STOCK | 5.0000 | $1,147.65 | $1,128.06 | $5,640.30 | 🔴 $-97.97 | -1.71% |
| **META** | STOCK | 10.00 | $594.97 | $597.80 | $5,978.05 | 🟢 +$28.32 | +0.48% |
| **MSFT** | STOCK | 16.00 | $422.42 | $393.81 | $6,300.88 | 🔴 $-457.78 | -6.77% |
| **NVDA** | STOCK | 100.00 | $223.97 | $208.97 | $20,897.00 | 🔴 $-1,500.39 | -6.70% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $73.07 | $1,126.65 | 🔴 $-201.73 | -15.19% |
| **SPY** | STOCK | 6.0000 | $745.44 | $752.61 | $4,515.67 | 🟢 +$43.01 | +0.96% |
| **TSLA** | STOCK | 24.00 | $432.23 | $404.87 | $9,716.88 | 🔴 $-656.69 | -6.33% |
| **VTI** | ETF | 4.0000 | $366.61 | $371.52 | $1,486.08 | 🟢 +$19.65 | +1.34% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $209.29 | 🔴 -1.49% | **BUY** | 85% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $375.63 | 🟢 +1.70% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $298.20 | 🟢 +0.60% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $393.75 | 🔴 -1.50% | **BUY** | 96% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $248.95 | 🟢 +1.19% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $371.74 | 🔴 -0.21% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $380.77 | 🔴 -3.34% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $598.40 | 🟢 +0.83% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $65,769.41 | 🔴 -0.78% | **BUY** | 78% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,128.62 | 🔴 -0.06% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Moderate negative momentum (-1.49%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.70%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.60%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 84% | Moderate negative momentum (-1.50%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.19%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.21%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 72% | Extreme loss today (-3.34%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.83%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 69% | Moderate negative momentum (-0.78%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.06%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
