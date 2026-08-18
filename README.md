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

> 🕐 **Last updated:** 2026-08-18 21:22 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$103,446.29` |
| 💸 Cash Available    | `$-107,462.35` |
| 🧾 Buying Power      | `$89,173.78` |
| 🟢 Total P&L | `+$17,242.09` &nbsp; `(+172.42%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$17,242.09` (+172.42%)
- **Yesterday-to-today P&L:** `+$88.88`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 80% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $309.75 | $20,753.25 | 🟢 +$153.92 | +0.75% |
| **AMZN** | STOCK | 49.00 | $247.51 | $259.38 | $12,709.62 | 🟢 +$581.40 | +4.79% |
| **AVGO** | STOCK | 15.00 | $388.65 | $380.03 | $5,700.48 | 🔴 $-129.28 | -2.22% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $64,585.30 | $20,046.95 | 🟢 +$12,703.09 | +172.98% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,911.75 | $1,199.13 | 🟢 +$1,199.13 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $352.53 | $343.84 | $9,627.52 | 🔴 $-243.26 | -2.46% |
| **LLY** | STOCK | 41.00 | $1,168.10 | $1,226.00 | $50,266.00 | 🟢 +$2,373.82 | +4.96% |
| **META** | STOCK | 32.00 | $592.98 | $545.06 | $17,441.84 | 🔴 $-1,533.61 | -8.08% |
| **MSFT** | STOCK | 30.00 | $412.13 | $480.86 | $14,425.80 | 🟢 +$2,062.02 | +16.68% |
| **NVDA** | STOCK | 163.00 | $214.55 | $219.51 | $35,780.13 | 🟢 +$808.33 | +2.31% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.79 | $1,183.95 | 🟢 +$1,183.95 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $767.32 | $4,603.92 | 🟢 +$131.26 | +2.93% |
| **TSLA** | STOCK | 24.00 | $432.23 | $336.18 | $8,068.30 | 🔴 $-2,305.27 | -22.22% |
| **VTI** | ETF | 24.00 | $368.55 | $379.24 | $9,101.76 | 🟢 +$256.61 | +2.90% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $219.74 | 🔴 -2.34% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $310.03 | 🟢 +1.45% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $344.20 | 🟢 +0.06% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $481.63 | 🟢 +0.27% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $259.45 | 🔴 -0.71% | **BUY** | 80% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $379.04 | 🔴 -0.81% | **BUY** | 81% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $380.00 | 🔴 -3.17% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $543.67 | 🔴 -4.45% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,561.64 | 🟢 +0.12% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,225.73 | 🟢 +3.60% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-2.34%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.45%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.06%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.27%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 70% | Moderate negative momentum (-0.71%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 71% | Moderate negative momentum (-0.81%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 71% | Extreme loss today (-3.17%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 77% | Extreme loss today (-4.45%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.12%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 73% | Extreme gain today (+3.60%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
