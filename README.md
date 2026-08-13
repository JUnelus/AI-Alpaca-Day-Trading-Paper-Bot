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

> 🕐 **Last updated:** 2026-08-13 14:11 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$106,495.46` |
| 💸 Cash Available    | `$-94,478.07` |
| 🧾 Buying Power      | `$115,209.13` |
| 🟢 Total P&L | `+$20,288.01` &nbsp; `(+202.88%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$20,288.01` (+202.88%)
- **Yesterday-to-today P&L:** `+$1,481.79`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **LLY** | BUY | 73% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $304.96 | $20,432.65 | 🔴 $-166.68 | -0.81% |
| **AMZN** | STOCK | 43.00 | $245.63 | $269.31 | $11,580.33 | 🟢 +$1,018.39 | +9.64% |
| **AVGO** | STOCK | 12.00 | $387.61 | $423.52 | $5,082.24 | 🟢 +$430.90 | +9.26% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $63,719.80 | $19,778.30 | 🟢 +$12,434.44 | +169.32% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,886.10 | $1,183.04 | 🟢 +$1,183.04 | 0.00% |
| **GOOGL** | STOCK | 25.00 | $353.71 | $346.52 | $8,663.00 | 🔴 $-179.64 | -2.03% |
| **LLY** | STOCK | 38.00 | $1,166.69 | $1,216.80 | $46,238.40 | 🟢 +$1,904.33 | +4.30% |
| **META** | STOCK | 28.00 | $596.63 | $588.99 | $16,491.58 | 🔴 $-213.93 | -1.28% |
| **MSFT** | STOCK | 28.00 | $407.09 | $500.61 | $14,017.08 | 🟢 +$2,618.63 | +22.97% |
| **NVDA** | STOCK | 161.00 | $214.48 | $226.13 | $36,406.93 | 🟢 +$1,875.59 | +5.43% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.25 | $1,175.68 | 🟢 +$1,175.68 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $778.48 | $4,670.85 | 🟢 +$198.19 | +4.43% |
| **TSLA** | STOCK | 24.00 | $432.23 | $333.52 | $8,004.48 | 🔴 $-2,369.09 | -22.84% |
| **VTI** | ETF | 22.00 | $367.49 | $384.68 | $8,462.96 | 🟢 +$378.17 | +4.68% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $226.31 | 🟢 +0.99% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $304.91 | 🟢 +0.88% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $346.51 | 🟢 +0.86% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $499.86 | 🟢 +1.51% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $268.94 | 🟢 +0.62% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $384.56 | 🟢 +0.71% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $422.81 | 🟢 +1.62% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $588.57 | 🟢 +1.68% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,674.25 | 🟢 +0.41% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,216.00 | 🔴 -0.35% | **BUY** | 73% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+0.99%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.88%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.86%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.51%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.62%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.71%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.62%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.68%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.41%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.35%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
