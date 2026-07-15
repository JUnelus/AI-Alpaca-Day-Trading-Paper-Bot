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

> 🕐 **Last updated:** 2026-07-15 14:22 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$101,008.90` |
| 💸 Cash Available    | `$-54,334.37` |
| 🧾 Buying Power      | `$155,473.44` |
| 🟢 Total P&L | `+$16,928.29` &nbsp; `(+169.28%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$16,928.29` (+169.28%)
- **Yesterday-to-today P&L:** `+$1,378.34`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $305.86 | $325.26 | $17,238.78 | 🟢 +$1,028.41 | +6.34% |
| **AMZN** | STOCK | 40.00 | $239.44 | $254.64 | $10,185.60 | 🟢 +$607.80 | +6.35% |
| **AVGO** | STOCK | 9.0000 | $380.33 | $391.18 | $3,520.62 | 🟢 +$97.61 | +2.85% |
| **BTC/USD** | CRYPTO | 0.2453 | $12,850.06 | $65,211.29 | $15,993.60 | 🟢 +$12,842.02 | +407.48% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,922.85 | $1,206.09 | 🟢 +$1,206.09 | 0.00% |
| **GOOGL** | STOCK | 24.00 | $353.63 | $366.65 | $8,799.60 | 🟢 +$312.51 | +3.68% |
| **LLY** | STOCK | 23.00 | $1,162.94 | $1,139.64 | $26,211.72 | 🔴 $-535.83 | -2.00% |
| **META** | STOCK | 17.00 | $585.08 | $671.71 | $11,419.07 | 🟢 +$1,472.70 | +14.81% |
| **MSFT** | STOCK | 29.00 | $391.00 | $396.87 | $11,509.23 | 🟢 +$170.34 | +1.50% |
| **NVDA** | STOCK | 133.00 | $216.63 | $210.85 | $28,043.05 | 🔴 $-769.23 | -2.67% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $78.09 | $1,204.01 | 🟢 +$1,204.01 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $754.75 | $4,528.50 | 🟢 +$55.84 | +1.25% |
| **TSLA** | STOCK | 24.00 | $432.23 | $396.75 | $9,522.12 | 🔴 $-851.45 | -8.21% |
| **VTI** | ETF | 16.00 | $367.11 | $372.58 | $5,961.28 | 🟢 +$87.47 | +1.49% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $211.09 | 🔴 -0.34% | **BUY** | 73% |
| 2 | **AAPL** | Apple Inc. | STOCK | $325.32 | 🟢 +3.32% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $366.25 | 🟢 +1.87% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $397.50 | 🟢 +3.27% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $254.64 | 🟢 +2.89% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $372.64 | 🟢 +0.40% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $391.50 | 🟢 +0.61% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $668.96 | 🟢 +1.20% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $65,362.21 | 🟢 +0.57% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,138.18 | 🔴 -1.25% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.34%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **SELL** | 72% | Extreme gain today (+3.32%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.87%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 71% | Extreme gain today (+3.27%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 69% | Extreme gain today (+2.89%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.40%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+0.61%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.20%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.57%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 75% | Moderate negative momentum (-1.25%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
