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

> 🕐 **Last updated:** 2026-07-10 14:38 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,619.56` |
| 💸 Cash Available    | `$-43,185.64` |
| 🧾 Buying Power      | `$168,800.54` |
| 🟢 Total P&L | `+$15,786.96` &nbsp; `(+157.87%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$15,786.96` (+157.87%)
- **Yesterday-to-today P&L:** `+$665.10`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **META** | SELL | 100% | Take-profit trim after overextended rally |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 51.00 | $305.55 | $312.79 | $15,952.29 | 🟢 +$369.18 | +2.37% |
| **AMZN** | STOCK | 34.00 | $238.28 | $245.47 | $8,345.98 | 🟢 +$244.36 | +3.02% |
| **AVGO** | STOCK | 6.0000 | $373.38 | $398.71 | $2,392.26 | 🟢 +$152.01 | +6.79% |
| **BTC/USD** | CRYPTO | 0.2284 | $9,202.82 | $63,882.08 | $14,590.70 | 🟢 +$12,488.77 | +594.16% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,783.62 | $1,118.76 | 🟢 +$1,118.76 | 0.00% |
| **GOOGL** | STOCK | 20.00 | $353.48 | $354.47 | $7,089.40 | 🟢 +$19.76 | +0.28% |
| **LLY** | STOCK | 18.00 | $1,160.16 | $1,187.57 | $21,376.21 | 🟢 +$493.36 | +2.36% |
| **META** | STOCK | 19.00 | $575.01 | $667.60 | $12,684.40 | 🟢 +$1,759.23 | +16.10% |
| **MSFT** | STOCK | 27.00 | $391.53 | $383.31 | $10,349.37 | 🔴 $-221.85 | -2.10% |
| **NVDA** | STOCK | 136.00 | $217.36 | $207.30 | $28,192.80 | 🔴 $-1,368.66 | -4.63% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $77.70 | $1,198.12 | 🟢 +$1,198.12 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $751.94 | $4,511.64 | 🟢 +$38.98 | +0.87% |
| **TSLA** | STOCK | 24.00 | $432.23 | $408.39 | $9,801.36 | 🔴 $-572.21 | -5.52% |
| **VTI** | ETF | 14.00 | $366.54 | $371.34 | $5,198.76 | 🟢 +$67.15 | +1.31% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $207.33 | 🟢 +2.24% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $312.69 | 🔴 -1.12% | **BUY** | 85% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $354.43 | 🔴 -1.24% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $382.88 | 🔴 -0.39% | **BUY** | 75% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $245.36 | 🔴 -0.68% | **BUY** | 79% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $371.20 | 🔴 -0.07% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $399.18 | 🔴 -0.48% | **BUY** | 75% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $667.35 | 🟢 +5.68% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,999.20 | 🟢 +1.32% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,187.28 | 🔴 -2.44% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+2.24%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.12%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.24%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 70% | Moderate negative momentum (-0.68%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.07%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 66% | Moderate negative momentum (-0.48%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 78% | Extreme gain today (+5.68%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.32%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.44%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
