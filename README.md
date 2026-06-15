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

> 🕐 **Last updated:** 2026-06-15 22:02 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,750.10` |
| 💸 Cash Available    | `$6,163.60` |
| 🧾 Buying Power      | `$246,355.53` |
| 🔴 Total P&L | `$-3,196.19` &nbsp; `(-31.96%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-3,196.19` (-31.96%)
- **Yesterday-to-today P&L:** `+$2,285.00`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **META** | SELL | 100% | Take-profit trim after overextended rally |
| **LLY** | BUY | 72% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $308.82 | $296.08 | $15,396.16 | 🔴 $-662.25 | -4.12% |
| **AMZN** | STOCK | 20.00 | $243.99 | $248.40 | $4,968.00 | 🟢 +$88.13 | +1.81% |
| **AVGO** | STOCK | 11.00 | $393.05 | $394.85 | $4,343.35 | 🟢 +$19.83 | +0.46% |
| **BTC/USD** | CRYPTO | 0.0255 | $73,953.69 | $66,422.05 | $1,697.06 | 🔴 $-192.43 | -10.18% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,811.90 | $1,136.50 | 🔴 $-194.70 | -14.63% |
| **GOOGL** | STOCK | 7.0000 | $361.34 | $370.00 | $2,590.00 | 🟢 +$60.65 | +2.40% |
| **LLY** | STOCK | 4.0000 | $1,148.32 | $1,130.90 | $4,523.60 | 🔴 $-69.67 | -1.52% |
| **META** | STOCK | 12.00 | $596.84 | $593.50 | $7,122.00 | 🔴 $-40.09 | -0.56% |
| **MSFT** | STOCK | 16.00 | $422.42 | $399.75 | $6,396.00 | 🔴 $-362.66 | -5.37% |
| **NVDA** | STOCK | 100.00 | $223.97 | $212.10 | $21,210.00 | 🔴 $-1,187.39 | -5.30% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $74.29 | $1,145.46 | 🔴 $-182.92 | -13.77% |
| **SPY** | STOCK | 6.0000 | $745.44 | $754.64 | $4,527.84 | 🟢 +$55.18 | +1.23% |
| **TSLA** | STOCK | 24.00 | $432.23 | $409.26 | $9,822.16 | 🔴 $-551.41 | -5.32% |
| **VTI** | ETF | 4.0000 | $366.61 | $372.49 | $1,489.95 | 🟢 +$23.52 | +1.60% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $212.45 | 🟢 +3.54% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $369.35 | 🟢 +2.69% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $296.42 | 🟢 +1.82% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $399.76 | 🟢 +2.31% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $246.02 | 🟢 +3.13% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $372.53 | 🟢 +1.68% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $393.94 | 🟢 +3.11% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $593.48 | 🟢 +4.67% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $66,384.63 | 🟢 +1.04% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,129.35 | 🔴 -0.32% | **BUY** | 72% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 73% | Extreme gain today (+3.54%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 68% | Extreme gain today (+2.69%) — mean reversion pullback likely |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.82%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+2.31%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 71% | Extreme gain today (+3.13%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.68%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 71% | Extreme gain today (+3.11%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 78% | Extreme gain today (+4.67%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.04%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.32%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
