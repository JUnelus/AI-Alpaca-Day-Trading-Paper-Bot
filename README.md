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

> 🕐 **Last updated:** 2026-07-31 21:37 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$96,183.21` |
| 💸 Cash Available    | `$-84,930.42` |
| 🧾 Buying Power      | `$104,597.90` |
| 🟢 Total P&L | `+$11,606.64` &nbsp; `(+116.07%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$11,606.64` (+116.07%)
- **Yesterday-to-today P&L:** `+$1,655.54`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | SELL | 100% | Take-profit trim after overextended rally |
| **AMZN** | SELL | 100% | Take-profit trim after overextended rally |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 76% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 57.00 | $307.82 | $306.48 | $17,469.58 | 🔴 $-75.89 | -0.43% |
| **AMZN** | STOCK | 51.00 | $238.56 | $270.65 | $13,803.15 | 🟢 +$1,636.75 | +13.45% |
| **AVGO** | STOCK | 15.00 | $380.94 | $388.01 | $5,820.15 | 🟢 +$106.06 | +1.86% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $62,968.26 | $17,491.12 | 🟢 +$12,245.35 | +233.43% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,861.30 | $1,167.48 | 🟢 +$1,167.48 | 0.00% |
| **GOOGL** | STOCK | 26.00 | $351.97 | $354.06 | $9,205.56 | 🟢 +$54.25 | +0.59% |
| **LLY** | STOCK | 31.00 | $1,161.03 | $1,148.25 | $35,595.75 | 🔴 $-396.29 | -1.10% |
| **META** | STOCK | 28.00 | $594.11 | $554.79 | $15,534.12 | 🔴 $-1,101.03 | -6.62% |
| **MSFT** | STOCK | 28.00 | $387.87 | $462.39 | $12,947.01 | 🟢 +$2,086.70 | +19.21% |
| **NVDA** | STOCK | 157.00 | $214.30 | $199.58 | $31,334.28 | 🔴 $-2,311.06 | -6.87% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.03 | $1,126.03 | 🟢 +$1,126.03 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $744.65 | $4,467.90 | 🔴 $-4.76 | -0.11% |
| **TSLA** | STOCK | 24.00 | $432.23 | $309.75 | $7,434.00 | 🔴 $-2,939.57 | -28.34% |
| **VTI** | ETF | 21.00 | $366.90 | $367.50 | $7,717.50 | 🟢 +$12.61 | +0.16% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $200.75 | 🟢 +2.93% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $308.91 | 🔴 -7.35% | **BUY** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $356.13 | 🟢 +6.73% | **SELL** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $464.72 | 🟢 +3.02% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $271.58 | 🟢 +15.32% | **SELL** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.21 | 🟢 +0.53% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $389.28 | 🟢 +0.37% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $556.71 | 🟢 +3.28% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,943.38 | 🔴 -2.76% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,148.84 | 🔴 -0.53% | **BUY** | 76% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 70% | Extreme gain today (+2.93%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **BUY** | 78% | Extreme loss today (-7.35%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 78% | Extreme gain today (+6.73%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 70% | Extreme gain today (+3.02%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 78% | Extreme gain today (+15.32%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.53%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (+0.37%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 71% | Extreme gain today (+3.28%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 69% | Extreme loss today (-2.76%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 67% | Moderate negative momentum (-0.53%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
