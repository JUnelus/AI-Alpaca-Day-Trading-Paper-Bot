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

> 🕐 **Last updated:** 2026-08-26 22:13 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$108,242.33` |
| 💸 Cash Available    | `$-120,884.08` |
| 🧾 Buying Power      | `$89,646.60` |
| 🟢 Total P&L | `+$20,851.34` &nbsp; `(+208.51%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$20,851.34` (+208.51%)
- **Yesterday-to-today P&L:** `$-274.97`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 72% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $311.50 | $21,805.00 | 🟢 +$275.39 | +1.28% |
| **AMZN** | STOCK | 60.00 | $249.93 | $262.52 | $15,751.20 | 🟢 +$755.30 | +5.04% |
| **AVGO** | STOCK | 22.00 | $380.33 | $358.20 | $7,880.40 | 🔴 $-486.94 | -5.82% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $78,861.10 | $18,106.11 | 🟢 +$15,857.96 | +705.38% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,504.27 | $1,570.78 | 🟢 +$1,570.78 | 0.00% |
| **GOOGL** | STOCK | 33.00 | $351.11 | $341.80 | $11,279.42 | 🔴 $-307.25 | -2.65% |
| **LLY** | STOCK | 45.00 | $1,179.49 | $1,191.00 | $53,595.00 | 🟢 +$517.99 | +0.98% |
| **META** | STOCK | 33.00 | $591.43 | $578.88 | $19,103.04 | 🔴 $-414.15 | -2.12% |
| **MSFT** | STOCK | 32.00 | $416.49 | $496.20 | $15,878.40 | 🟢 +$2,550.77 | +19.14% |
| **NVDA** | STOCK | 179.00 | $214.63 | $218.00 | $39,022.11 | 🟢 +$603.96 | +1.57% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $98.89 | $1,524.81 | 🟢 +$1,524.81 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $770.04 | $4,620.24 | 🟢 +$147.58 | +3.30% |
| **TSLA** | STOCK | 24.00 | $432.23 | $347.91 | $8,349.91 | 🔴 $-2,023.66 | -19.51% |
| **VTI** | ETF | 28.00 | $370.04 | $380.00 | $10,640.00 | 🟢 +$278.80 | +2.69% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $209.66 | 🔴 -1.59% | **BUY** | 96% |
| 2 | **AAPL** | Apple Inc. | STOCK | $313.45 | 🟢 +1.15% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $342.00 | 🔴 -1.43% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $496.37 | 🟢 +0.95% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $260.28 | 🔴 -0.30% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $378.23 | 🟢 +0.02% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $355.59 | 🔴 -0.32% | **BUY** | 72% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $78,785.41 | 🟢 +0.32% | HOLD | — |
| 9 | **META** | Meta Platforms Inc. | STOCK | $576.14 | 🟢 +1.07% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,189.41 | 🔴 -3.59% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 84% | Moderate negative momentum (-1.59%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.15%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.43%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.95%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.30%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.02%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (-0.32%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.32%) — no trend to carry forward |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.07%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 73% | Extreme loss today (-3.59%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
