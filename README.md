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

> 🕐 **Last updated:** 2026-07-14 14:24 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,318.01` |
| 💸 Cash Available    | `$-52,380.22` |
| 🧾 Buying Power      | `$152,433.94` |
| 🟢 Total P&L | `+$14,237.39` &nbsp; `(+142.37%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$14,237.39` (+142.37%)
- **Yesterday-to-today P&L:** `+$66.07`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 98% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 82% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $305.86 | $314.44 | $16,665.32 | 🟢 +$454.95 | +2.81% |
| **AMZN** | STOCK | 38.00 | $239.13 | $245.37 | $9,323.87 | 🟢 +$236.85 | +2.61% |
| **AVGO** | STOCK | 9.0000 | $380.33 | $391.25 | $3,521.30 | 🟢 +$98.29 | +2.87% |
| **BTC/USD** | CRYPTO | 0.2453 | $12,850.06 | $63,794.97 | $15,646.24 | 🟢 +$12,494.66 | +396.46% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,862.82 | $1,168.44 | 🟢 +$1,168.44 | 0.00% |
| **GOOGL** | STOCK | 24.00 | $353.63 | $355.49 | $8,531.76 | 🟢 +$44.67 | +0.53% |
| **LLY** | STOCK | 22.00 | $1,163.57 | $1,148.67 | $25,270.74 | 🔴 $-327.89 | -1.28% |
| **META** | STOCK | 17.00 | $585.08 | $659.26 | $11,207.42 | 🟢 +$1,261.05 | +12.68% |
| **MSFT** | STOCK | 29.00 | $391.00 | $384.24 | $11,142.96 | 🔴 $-195.93 | -1.73% |
| **NVDA** | STOCK | 133.00 | $216.63 | $205.69 | $27,356.77 | 🔴 $-1,455.51 | -5.05% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.76 | $1,183.61 | 🟢 +$1,183.61 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $750.35 | $4,502.10 | 🟢 +$29.44 | +0.66% |
| **TSLA** | STOCK | 24.00 | $432.23 | $398.48 | $9,563.52 | 🔴 $-810.05 | -7.81% |
| **VTI** | ETF | 16.00 | $367.11 | $370.54 | $5,928.64 | 🟢 +$54.83 | +0.93% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $205.62 | 🟢 +1.03% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $314.42 | 🔴 -0.91% | **BUY** | 84% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $355.48 | 🟢 +0.84% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $384.28 | 🔴 -1.72% | **BUY** | 98% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $245.25 | 🔴 -0.83% | **BUY** | 82% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $370.54 | 🟢 +0.21% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $391.15 | 🟢 +1.85% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $658.88 | 🟢 +0.33% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,777.26 | 🟢 +2.41% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,147.99 | 🔴 -2.87% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.03%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 74% | Moderate negative momentum (-0.91%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.84%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.72%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 72% | Moderate negative momentum (-0.83%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.21%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.85%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.33%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+2.41%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 69% | Extreme loss today (-2.87%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
