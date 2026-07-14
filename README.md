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

> 🕐 **Last updated:** 2026-07-14 21:33 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,630.58` |
| 💸 Cash Available    | `$-54,334.36` |
| 🧾 Buying Power      | `$153,332.26` |
| 🟢 Total P&L | `+$15,549.95` &nbsp; `(+155.50%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$15,549.95` (+155.50%)
- **Yesterday-to-today P&L:** `+$1,378.63`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | SELL | 100% | Take-profit trim after overextended rally |
| **AAPL** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $305.86 | $314.77 | $16,682.81 | 🟢 +$472.44 | +2.91% |
| **AMZN** | STOCK | 40.00 | $239.44 | $247.15 | $9,886.00 | 🟢 +$308.20 | +3.22% |
| **AVGO** | STOCK | 9.0000 | $380.33 | $389.75 | $3,507.75 | 🟢 +$84.74 | +2.48% |
| **BTC/USD** | CRYPTO | 0.2453 | $12,850.06 | $64,616.66 | $15,847.77 | 🟢 +$12,696.18 | +402.85% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,875.77 | $1,176.56 | 🟢 +$1,176.56 | 0.00% |
| **GOOGL** | STOCK | 24.00 | $353.63 | $359.19 | $8,620.56 | 🟢 +$133.47 | +1.57% |
| **LLY** | STOCK | 23.00 | $1,162.94 | $1,156.12 | $26,590.71 | 🔴 $-156.84 | -0.59% |
| **META** | STOCK | 17.00 | $585.08 | $659.89 | $11,218.13 | 🟢 +$1,271.76 | +12.79% |
| **MSFT** | STOCK | 29.00 | $391.00 | $385.10 | $11,167.90 | 🔴 $-170.99 | -1.51% |
| **NVDA** | STOCK | 133.00 | $216.63 | $211.55 | $28,136.15 | 🔴 $-676.13 | -2.35% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.82 | $1,184.50 | 🟢 +$1,184.50 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $751.97 | $4,511.82 | 🟢 +$39.16 | +0.88% |
| **TSLA** | STOCK | 24.00 | $432.23 | $395.42 | $9,490.10 | 🔴 $-883.47 | -8.52% |
| **VTI** | ETF | 16.00 | $367.11 | $371.51 | $5,944.17 | 🟢 +$70.36 | +1.20% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $211.80 | 🟢 +4.06% | **SELL** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $314.86 | 🔴 -0.77% | **BUY** | 81% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $359.51 | 🟢 +1.99% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $384.93 | 🔴 -1.55% | **BUY** | 96% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $247.49 | 🟢 +0.07% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $371.16 | 🟢 +0.37% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $389.11 | 🟢 +1.32% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $661.04 | 🟢 +0.66% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,635.18 | 🟢 +3.79% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,152.54 | 🔴 -2.48% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 75% | Extreme gain today (+4.06%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **SELL** | 72% | Moderate negative momentum (-0.77%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.99%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.55%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.07%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.37%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.32%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.66%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 74% | Extreme gain today (+3.79%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.48%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
