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

> 🕐 **Last updated:** 2026-07-10 21:36 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$100,317.02` |
| 💸 Cash Available    | `$-44,979.50` |
| 🧾 Buying Power      | `$169,707.75` |
| 🟢 Total P&L | `+$16,302.23` &nbsp; `(+163.02%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$16,302.23` (+163.02%)
- **Yesterday-to-today P&L:** `+$1,180.38`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | SELL | 100% | Take-profit trim after overextended rally |
| **GOOGL** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **META** | SELL | 100% | Take-profit trim after overextended rally |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $305.69 | $315.03 | $16,381.56 | 🟢 +$485.63 | +3.06% |
| **AMZN** | STOCK | 36.00 | $238.68 | $245.78 | $8,848.08 | 🟢 +$255.52 | +2.97% |
| **AVGO** | STOCK | 7.0000 | $377.02 | $399.80 | $2,798.60 | 🟢 +$159.44 | +6.04% |
| **BTC/USD** | CRYPTO | 0.2284 | $9,202.82 | $63,851.33 | $14,583.67 | 🟢 +$12,481.74 | +593.82% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,792.20 | $1,124.14 | 🟢 +$1,124.14 | 0.00% |
| **GOOGL** | STOCK | 21.00 | $353.53 | $357.00 | $7,497.00 | 🟢 +$72.81 | +0.98% |
| **LLY** | STOCK | 19.00 | $1,161.66 | $1,189.00 | $22,591.00 | 🟢 +$519.54 | +2.35% |
| **META** | STOCK | 17.00 | $575.01 | $667.58 | $11,348.91 | 🟢 +$1,573.76 | +16.10% |
| **MSFT** | STOCK | 28.00 | $391.24 | $385.20 | $10,785.60 | 🔴 $-169.01 | -1.54% |
| **NVDA** | STOCK | 136.00 | $217.36 | $210.34 | $28,606.24 | 🔴 $-955.22 | -3.23% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $77.87 | $1,200.66 | 🟢 +$1,200.66 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $755.20 | $4,531.20 | 🟢 +$58.54 | +1.31% |
| **TSLA** | STOCK | 24.00 | $432.23 | $407.48 | $9,779.54 | 🔴 $-594.03 | -5.73% |
| **VTI** | ETF | 14.00 | $366.54 | $372.88 | $5,220.32 | 🟢 +$88.71 | +1.73% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $210.96 | 🟢 +4.03% | **SELL** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $315.32 | 🔴 -0.28% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $357.18 | 🔴 -0.48% | **BUY** | 76% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $385.10 | 🟢 +0.19% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $245.34 | 🔴 -0.69% | **BUY** | 79% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $372.69 | 🟢 +0.33% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $399.97 | 🔴 -0.28% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $669.21 | 🟢 +5.97% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,969.92 | 🟢 +1.28% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,188.58 | 🔴 -2.33% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Extreme gain today (+4.03%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.28%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 67% | Moderate negative momentum (-0.48%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.19%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 70% | Moderate negative momentum (-0.69%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.33%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (-0.28%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 78% | Extreme gain today (+5.97%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.28%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.33%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
