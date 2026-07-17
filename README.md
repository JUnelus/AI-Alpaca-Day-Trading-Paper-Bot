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

> 🕐 **Last updated:** 2026-07-17 14:16 UTC &nbsp;|&nbsp; **Trades today:** 9 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,747.82` |
| 💸 Cash Available    | `$-59,318.42` |
| 🧾 Buying Power      | `$141,755.90` |
| 🟢 Total P&L | `+$14,600.04` &nbsp; `(+146.00%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$14,600.04` (+146.00%)
- **Yesterday-to-today P&L:** `$-1,661.49`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 78% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 78% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 76% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 49.00 | $305.45 | $329.95 | $16,167.54 | 🟢 +$1,200.41 | +8.02% |
| **AMZN** | STOCK | 44.00 | $240.09 | $247.72 | $10,899.90 | 🟢 +$335.74 | +3.18% |
| **AVGO** | STOCK | 11.00 | $379.59 | $372.35 | $4,095.80 | 🔴 $-79.71 | -1.91% |
| **BTC/USD** | CRYPTO | 0.2617 | $16,053.40 | $63,363.48 | $16,583.30 | 🟢 +$12,381.85 | +294.70% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,830.38 | $1,148.09 | 🟢 +$1,148.09 | 0.00% |
| **GOOGL** | STOCK | 25.00 | $353.37 | $345.95 | $8,648.75 | 🔴 $-185.54 | -2.10% |
| **LLY** | STOCK | 24.00 | $1,161.99 | $1,182.34 | $28,376.16 | 🟢 +$488.29 | +1.75% |
| **META** | STOCK | 19.00 | $593.24 | $633.73 | $12,040.87 | 🟢 +$769.27 | +6.82% |
| **MSFT** | STOCK | 29.00 | $391.00 | $392.60 | $11,385.40 | 🟢 +$46.51 | +0.41% |
| **NVDA** | STOCK | 137.00 | $216.30 | $205.39 | $28,138.43 | 🔴 $-1,495.17 | -5.05% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $74.44 | $1,147.77 | 🟢 +$1,147.77 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $746.63 | $4,479.78 | 🟢 +$7.12 | +0.16% |
| **TSLA** | STOCK | 24.00 | $432.23 | $382.50 | $9,180.01 | 🔴 $-1,193.56 | -11.51% |
| **VTI** | ETF | 17.00 | $367.08 | $368.78 | $6,269.26 | 🟢 +$28.98 | +0.46% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $205.13 | 🔴 -1.09% | **BUY** | 85% |
| 2 | **AAPL** | Apple Inc. | STOCK | $330.24 | 🔴 -0.91% | **BUY** | 84% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $347.26 | 🔴 -2.03% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $392.88 | 🔴 -2.05% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $248.33 | 🔴 -0.62% | **BUY** | 78% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.92 | 🔴 -0.45% | **BUY** | 75% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $371.93 | 🔴 -0.67% | **BUY** | 78% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $637.37 | 🔴 -4.09% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,376.80 | 🔴 -0.64% | **BUY** | 76% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,181.99 | 🟢 +1.10% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Moderate negative momentum (-1.09%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 74% | Moderate negative momentum (-0.91%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 85% | Moderate negative momentum (-2.03%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-2.05%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 69% | Moderate negative momentum (-0.62%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 66% | Moderate negative momentum (-0.45%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 69% | Moderate negative momentum (-0.67%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 75% | Extreme loss today (-4.09%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 67% | Moderate negative momentum (-0.64%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.10%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
