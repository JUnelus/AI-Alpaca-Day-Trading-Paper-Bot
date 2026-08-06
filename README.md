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

> 🕐 **Last updated:** 2026-08-06 14:32 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$104,782.41` |
| 💸 Cash Available    | `$-78,122.68` |
| 🧾 Buying Power      | `$135,052.02` |
| 🟢 Total P&L | `+$18,595.50` &nbsp; `(+185.96%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$18,595.50` (+185.96%)
- **Yesterday-to-today P&L:** `+$402.63`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 72% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 61.00 | $307.66 | $312.78 | $19,079.57 | 🟢 +$312.37 | +1.66% |
| **AMZN** | STOCK | 39.00 | $243.03 | $273.67 | $10,673.13 | 🟢 +$1,195.02 | +12.61% |
| **AVGO** | STOCK | 10.00 | $380.24 | $424.81 | $4,248.10 | 🟢 +$445.68 | +11.72% |
| **BTC/USD** | CRYPTO | 0.2860 | $20,186.43 | $64,393.10 | $18,413.61 | 🟢 +$12,641.17 | +218.99% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,903.30 | $1,193.83 | 🟢 +$1,193.83 | 0.00% |
| **GOOGL** | STOCK | 19.00 | $353.45 | $360.48 | $6,849.02 | 🟢 +$133.56 | +1.99% |
| **LLY** | STOCK | 33.00 | $1,159.38 | $1,178.48 | $38,889.84 | 🟢 +$630.15 | +1.65% |
| **META** | STOCK | 26.00 | $597.38 | $591.13 | $15,369.51 | 🔴 $-162.38 | -1.05% |
| **MSFT** | STOCK | 24.00 | $391.93 | $495.90 | $11,901.60 | 🟢 +$2,495.23 | +26.53% |
| **NVDA** | STOCK | 157.00 | $214.30 | $219.50 | $34,461.50 | 🟢 +$816.16 | +2.43% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.33 | $1,130.66 | 🟢 +$1,130.66 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $770.41 | $4,622.46 | 🟢 +$149.80 | +3.35% |
| **TSLA** | STOCK | 24.00 | $432.23 | $321.07 | $7,705.80 | 🔴 $-2,667.77 | -25.72% |
| **VTI** | ETF | 22.00 | $367.49 | $380.31 | $8,366.82 | 🟢 +$282.03 | +3.49% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $219.60 | 🟢 +0.18% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $312.91 | 🟢 +0.61% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $360.45 | 🔴 -0.55% | **BUY** | 77% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $496.45 | 🟢 +1.85% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $273.32 | 🟢 +0.25% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $380.21 | 🟢 +0.15% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $424.30 | 🟢 +1.44% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $590.70 | 🟢 +0.33% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,316.15 | 🔴 -0.43% | **BUY** | 72% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,177.39 | 🟢 +0.64% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.18%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.61%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 68% | Moderate negative momentum (-0.55%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.85%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.25%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.15%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.44%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.33%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 64% | Moderate negative momentum (-0.43%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.64%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
