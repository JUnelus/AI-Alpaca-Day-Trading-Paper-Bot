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

> 🕐 **Last updated:** 2026-08-14 21:22 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$104,137.53` |
| 💸 Cash Available    | `$-98,739.53` |
| 🧾 Buying Power      | `$102,937.51` |
| 🟢 Total P&L | `+$17,933.30` &nbsp; `(+179.33%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$17,933.30` (+179.33%)
- **Yesterday-to-today P&L:** `$-1,858.15`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AMZN** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 82% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $305.75 | $20,485.25 | 🔴 $-114.08 | -0.55% |
| **AMZN** | STOCK | 44.00 | $246.06 | $262.74 | $11,560.56 | 🟢 +$733.75 | +6.78% |
| **AVGO** | STOCK | 13.00 | $388.66 | $393.53 | $5,115.92 | 🟢 +$63.32 | +1.25% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $62,857.65 | $19,510.70 | 🟢 +$12,166.83 | +165.67% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,876.80 | $1,177.20 | 🟢 +$1,177.20 | 0.00% |
| **GOOGL** | STOCK | 25.00 | $353.71 | $347.15 | $8,678.75 | 🔴 $-163.89 | -1.85% |
| **LLY** | STOCK | 40.00 | $1,167.80 | $1,182.00 | $47,280.00 | 🟢 +$567.82 | +1.22% |
| **META** | STOCK | 28.00 | $596.63 | $589.88 | $16,516.64 | 🔴 $-188.87 | -1.13% |
| **MSFT** | STOCK | 28.00 | $407.09 | $495.25 | $13,867.00 | 🟢 +$2,468.55 | +21.66% |
| **NVDA** | STOCK | 161.00 | $214.48 | $224.99 | $36,223.39 | 🟢 +$1,692.05 | +4.90% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.24 | $1,160.11 | 🟢 +$1,160.11 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $776.04 | $4,656.24 | 🟢 +$183.58 | +4.10% |
| **TSLA** | STOCK | 24.00 | $432.23 | $341.60 | $8,198.40 | 🔴 $-2,175.17 | -20.97% |
| **VTI** | ETF | 22.00 | $367.49 | $383.95 | $8,446.90 | 🟢 +$362.11 | +4.48% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $225.16 | 🔴 -0.06% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $305.93 | 🟢 +0.22% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $345.90 | 🔴 -0.13% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $495.40 | 🔴 -0.30% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $262.65 | 🔴 -0.94% | **BUY** | 83% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $383.85 | 🔴 -0.12% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $392.99 | 🔴 -5.94% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $589.85 | 🔴 -0.86% | **BUY** | 82% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,844.37 | 🔴 -0.92% | **BUY** | 81% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,180.16 | 🔴 -2.39% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.06%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.22%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.13%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.30%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 73% | Moderate negative momentum (-0.94%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.12%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 78% | Extreme loss today (-5.94%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 72% | Moderate negative momentum (-0.86%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 71% | Moderate negative momentum (-0.92%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.39%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
