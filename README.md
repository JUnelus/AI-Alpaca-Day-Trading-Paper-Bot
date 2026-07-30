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

> 🕐 **Last updated:** 2026-07-30 21:39 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,283.79` |
| 💸 Cash Available    | `$-86,068.04` |
| 🧾 Buying Power      | `$95,579.63` |
| 🟢 Total P&L | `+$9,951.09` &nbsp; `(+99.51%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$9,951.09` (+99.51%)
- **Yesterday-to-today P&L:** `+$2,836.80`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **MSFT** | SELL | 100% | Take-profit trim after overextended rally |
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 55.00 | $307.98 | $308.94 | $16,991.58 | 🟢 +$52.87 | +0.31% |
| **AMZN** | STOCK | 56.00 | $239.07 | $257.58 | $14,424.64 | 🟢 +$1,036.61 | +7.74% |
| **AVGO** | STOCK | 17.00 | $379.18 | $388.75 | $6,608.75 | 🟢 +$162.66 | +2.52% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $64,651.42 | $17,958.66 | 🟢 +$12,712.89 | +242.35% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,920.85 | $1,204.83 | 🟢 +$1,204.83 | 0.00% |
| **GOOGL** | STOCK | 29.00 | $352.30 | $333.95 | $9,684.55 | 🔴 $-532.10 | -5.21% |
| **LLY** | STOCK | 29.00 | $1,162.51 | $1,157.69 | $33,573.01 | 🔴 $-139.89 | -0.41% |
| **META** | STOCK | 27.00 | $595.72 | $540.45 | $14,592.15 | 🔴 $-1,492.16 | -9.28% |
| **MSFT** | STOCK | 31.00 | $392.64 | $447.10 | $13,860.10 | 🟢 +$1,688.29 | +13.87% |
| **NVDA** | STOCK | 157.00 | $214.30 | $195.89 | $30,754.73 | 🔴 $-2,890.61 | -8.59% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $74.25 | $1,144.84 | 🟢 +$1,144.84 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $741.75 | $4,450.48 | 🔴 $-22.18 | -0.50% |
| **TSLA** | STOCK | 24.00 | $432.23 | $308.80 | $7,411.20 | 🔴 $-2,962.37 | -28.56% |
| **VTI** | ETF | 21.00 | $366.90 | $366.30 | $7,692.30 | 🔴 $-12.59 | -0.16% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $333.43 | 🔴 -1.41% | **BUY** | 85% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $195.04 | 🟢 +2.65% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $333.66 | 🔴 -0.91% | **BUY** | 83% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $451.10 | 🟢 +15.51% | **SELL** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $235.50 | 🟢 +3.90% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $366.27 | 🟢 +1.62% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $387.84 | 🟢 +4.73% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $539.03 | 🔴 -7.95% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,695.17 | 🟢 +1.24% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,154.97 | 🔴 -4.55% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.41%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 68% | Extreme gain today (+2.65%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 73% | Moderate negative momentum (-0.91%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 78% | Extreme gain today (+15.51%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Extreme gain today (+3.90%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.62%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 78% | Extreme gain today (+4.73%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 78% | Extreme loss today (-7.95%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.24%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 78% | Extreme loss today (-4.55%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
