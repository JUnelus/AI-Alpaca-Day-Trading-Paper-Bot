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

> 🕐 **Last updated:** 2026-08-12 21:29 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$105,010.47` |
| 💸 Cash Available    | `$-92,827.72` |
| 🧾 Buying Power      | `$112,875.64` |
| 🟢 Total P&L | `+$18,806.23` &nbsp; `(+188.06%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$18,806.23` (+188.06%)
- **Yesterday-to-today P&L:** `$-127.77`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 66.00 | $307.51 | $302.15 | $19,942.10 | 🔴 $-353.75 | -1.74% |
| **AMZN** | STOCK | 42.00 | $245.13 | $267.64 | $11,240.88 | 🟢 +$945.33 | +9.18% |
| **AVGO** | STOCK | 12.00 | $387.61 | $415.88 | $4,990.56 | 🟢 +$339.22 | +7.29% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $63,577.10 | $19,734.01 | 🟢 +$12,390.15 | +168.71% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,875.57 | $1,176.43 | 🟢 +$1,176.43 | 0.00% |
| **GOOGL** | STOCK | 25.00 | $353.71 | $343.95 | $8,598.75 | 🔴 $-243.89 | -2.76% |
| **LLY** | STOCK | 37.00 | $1,165.32 | $1,221.00 | $45,177.00 | 🟢 +$2,060.14 | +4.78% |
| **META** | STOCK | 27.00 | $597.06 | $579.42 | $15,644.34 | 🔴 $-476.17 | -2.95% |
| **MSFT** | STOCK | 27.00 | $403.81 | $491.55 | $13,271.85 | 🟢 +$2,368.87 | +21.73% |
| **NVDA** | STOCK | 161.00 | $214.48 | $223.55 | $35,991.55 | 🟢 +$1,460.21 | +4.23% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.03 | $1,172.27 | 🟢 +$1,172.27 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $772.55 | $4,635.30 | 🟢 +$162.64 | +3.64% |
| **TSLA** | STOCK | 24.00 | $432.23 | $327.51 | $7,860.24 | 🔴 $-2,513.33 | -24.23% |
| **VTI** | ETF | 22.00 | $367.49 | $381.95 | $8,402.90 | 🟢 +$318.11 | +3.93% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $224.09 | 🟢 +3.03% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $302.25 | 🔴 -0.87% | **BUY** | 83% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $343.54 | 🔴 -0.08% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $492.43 | 🔴 -2.26% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $267.28 | 🔴 -1.83% | **BUY** | 99% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $381.83 | 🟢 +0.31% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $416.05 | 🔴 -0.01% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $578.85 | 🔴 -3.38% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,425.67 | 🔴 -0.16% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,220.28 | 🟢 +0.43% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 70% | Extreme gain today (+3.03%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **SELL** | 73% | Moderate negative momentum (-0.87%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.08%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-2.26%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-1.83%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.31%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (-0.01%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 72% | Extreme loss today (-3.38%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.16%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.43%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
