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

> 🕐 **Last updated:** 2026-07-16 14:28 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$101,743.58` |
| 💸 Cash Available    | `$-54,162.35` |
| 🧾 Buying Power      | `$159,848.62` |
| 🟢 Total P&L | `+$17,576.45` &nbsp; `(+175.76%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$17,576.45` (+175.76%)
- **Yesterday-to-today P&L:** `$-41.03`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 81% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 49.00 | $305.86 | $330.23 | $16,181.27 | 🟢 +$1,194.33 | +7.97% |
| **AMZN** | STOCK | 40.00 | $239.44 | $255.51 | $10,220.40 | 🟢 +$642.60 | +6.71% |
| **AVGO** | STOCK | 9.0000 | $380.33 | $383.72 | $3,453.48 | 🟢 +$30.47 | +0.89% |
| **BTC/USD** | CRYPTO | 0.2453 | $12,850.06 | $64,601.25 | $15,843.99 | 🟢 +$12,692.40 | +402.73% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,890.50 | $1,185.80 | 🟢 +$1,185.80 | 0.00% |
| **GOOGL** | STOCK | 24.00 | $353.63 | $372.17 | $8,932.08 | 🟢 +$444.99 | +5.24% |
| **LLY** | STOCK | 24.00 | $1,161.99 | $1,175.92 | $28,222.08 | 🟢 +$334.21 | +1.20% |
| **META** | STOCK | 17.00 | $585.08 | $676.65 | $11,503.05 | 🟢 +$1,556.68 | +15.65% |
| **MSFT** | STOCK | 29.00 | $391.00 | $395.93 | $11,481.97 | 🟢 +$143.08 | +1.26% |
| **NVDA** | STOCK | 133.00 | $216.63 | $208.78 | $27,767.74 | 🔴 $-1,044.54 | -3.63% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.85 | $1,184.93 | 🟢 +$1,184.93 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $754.15 | $4,524.90 | 🟢 +$52.24 | +1.17% |
| **TSLA** | STOCK | 24.00 | $432.23 | $393.71 | $9,449.04 | 🔴 $-924.53 | -8.91% |
| **VTI** | ETF | 16.00 | $367.11 | $372.35 | $5,957.60 | 🟢 +$83.79 | +1.43% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.50 | 🔴 -1.88% | **BUY** | 99% |
| 2 | **AAPL** | Apple Inc. | STOCK | $330.56 | 🟢 +0.93% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $372.15 | 🟢 +0.33% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $395.12 | 🔴 -0.13% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $255.40 | 🟢 +0.17% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $372.16 | 🔴 -0.07% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $383.13 | 🔴 -2.83% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $675.65 | 🔴 -0.83% | **BUY** | 81% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,757.90 | 🟢 +0.05% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,176.46 | 🟢 +1.71% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-1.88%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.93%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.33%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.13%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.17%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.07%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 69% | Extreme loss today (-2.83%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 72% | Moderate negative momentum (-0.83%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.05%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.71%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
