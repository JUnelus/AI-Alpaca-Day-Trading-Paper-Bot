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

> 🕐 **Last updated:** 2026-08-06 23:30 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$105,014.30` |
| 💸 Cash Available    | `$-79,009.70` |
| 🧾 Buying Power      | `$133,315.24` |
| 🟢 Total P&L | `+$18,828.35` &nbsp; `(+188.28%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$18,828.35` (+188.28%)
- **Yesterday-to-today P&L:** `+$635.47`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 76% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 61.00 | $307.66 | $312.50 | $19,062.50 | 🟢 +$295.30 | +1.57% |
| **AMZN** | STOCK | 39.00 | $243.03 | $272.05 | $10,609.95 | 🟢 +$1,131.84 | +11.94% |
| **AVGO** | STOCK | 10.00 | $380.24 | $421.50 | $4,215.00 | 🟢 +$412.58 | +10.85% |
| **BTC/USD** | CRYPTO | 0.2941 | $21,410.63 | $64,263.11 | $18,902.07 | 🟢 +$12,604.45 | +200.15% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,900.00 | $1,191.76 | 🟢 +$1,191.76 | 0.00% |
| **GOOGL** | STOCK | 20.00 | $353.80 | $358.67 | $7,173.41 | 🟢 +$97.43 | +1.38% |
| **LLY** | STOCK | 33.00 | $1,159.38 | $1,191.94 | $39,334.02 | 🟢 +$1,074.33 | +2.81% |
| **META** | STOCK | 26.00 | $597.38 | $589.40 | $15,324.40 | 🔴 $-207.49 | -1.34% |
| **MSFT** | STOCK | 24.00 | $391.93 | $498.69 | $11,968.56 | 🟢 +$2,562.19 | +27.24% |
| **NVDA** | STOCK | 157.00 | $214.30 | $219.55 | $34,469.35 | 🟢 +$824.01 | +2.45% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $72.80 | $1,122.51 | 🟢 +$1,122.51 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $768.80 | $4,612.83 | 🟢 +$140.17 | +3.13% |
| **TSLA** | STOCK | 24.00 | $432.23 | $320.25 | $7,686.00 | 🔴 $-2,687.57 | -25.91% |
| **VTI** | ETF | 22.00 | $367.49 | $379.62 | $8,351.64 | 🟢 +$266.85 | +3.30% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $218.99 | 🔴 -0.10% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $312.41 | 🟢 +0.45% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $357.75 | 🔴 -1.29% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $499.86 | 🟢 +2.54% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $272.26 | 🔴 -0.14% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $379.07 | 🔴 -0.15% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $420.56 | 🟢 +0.55% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $589.90 | 🟢 +0.19% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,183.74 | 🔴 -0.64% | **BUY** | 76% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,191.94 | 🟢 +1.89% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.10%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.45%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.29%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 68% | Extreme gain today (+2.54%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.14%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.15%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+0.55%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.19%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 67% | Moderate negative momentum (-0.64%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.89%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
