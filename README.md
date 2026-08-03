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

> 🕐 **Last updated:** 2026-08-03 21:38 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,783.52` |
| 💸 Cash Available    | `$-81,292.41` |
| 🧾 Buying Power      | `$118,239.52` |
| 🟢 Total P&L | `+$14,505.05` &nbsp; `(+145.05%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$14,505.05` (+145.05%)
- **Yesterday-to-today P&L:** `+$2,898.42`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | SELL | 100% | Take-profit trim after overextended rally |
| **AAPL** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **MSFT** | SELL | 100% | Take-profit trim after overextended rally |
| **AMZN** | SELL | 100% | Take-profit trim after overextended rally |
| **META** | SELL | 100% | Take-profit trim after overextended rally |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 59.00 | $307.74 | $303.87 | $17,928.33 | 🔴 $-228.36 | -1.26% |
| **AMZN** | STOCK | 41.00 | $238.78 | $281.86 | $11,556.26 | 🟢 +$1,766.37 | +18.04% |
| **AVGO** | STOCK | 16.00 | $381.89 | $392.11 | $6,273.76 | 🟢 +$163.58 | +2.68% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $63,671.02 | $17,686.33 | 🟢 +$12,440.56 | +237.15% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,863.40 | $1,168.80 | 🟢 +$1,168.80 | 0.00% |
| **GOOGL** | STOCK | 22.00 | $350.99 | $371.99 | $8,183.78 | 🟢 +$462.10 | +5.98% |
| **LLY** | STOCK | 33.00 | $1,159.80 | $1,122.45 | $37,040.85 | 🔴 $-1,232.46 | -3.22% |
| **META** | STOCK | 26.00 | $594.11 | $589.25 | $15,320.50 | 🔴 $-126.42 | -0.82% |
| **MSFT** | STOCK | 25.00 | $385.20 | $486.99 | $12,174.72 | 🟢 +$2,544.74 | +26.43% |
| **NVDA** | STOCK | 157.00 | $214.30 | $206.75 | $32,459.75 | 🔴 $-1,185.59 | -3.52% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.86 | $1,138.88 | 🟢 +$1,138.88 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $757.93 | $4,547.58 | 🟢 +$74.92 | +1.68% |
| **TSLA** | STOCK | 24.00 | $432.23 | $322.60 | $7,742.40 | 🔴 $-2,631.17 | -25.36% |
| **VTI** | ETF | 21.00 | $366.90 | $374.00 | $7,854.00 | 🟢 +$149.11 | +1.94% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $206.64 | 🟢 +2.93% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $373.51 | 🟢 +4.88% | **SELL** | 100% |
| 3 | **AAPL** | Apple Inc. | STOCK | $303.42 | 🔴 -1.78% | **BUY** | 99% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $487.65 | 🟢 +4.93% | **SELL** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $284.02 | 🟢 +4.58% | **SELL** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $373.84 | 🟢 +1.53% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $392.23 | 🟢 +0.76% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $590.24 | 🟢 +6.02% | **SELL** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,619.32 | 🟢 +0.17% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,121.36 | 🔴 -2.39% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 70% | Extreme gain today (+2.93%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **SELL** | 78% | Extreme gain today (+4.88%) — mean reversion pullback likely |
| 3 | **AAPL** | Apple Inc. | **SELL** | 85% | Moderate negative momentum (-1.78%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 78% | Extreme gain today (+4.93%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 78% | Extreme gain today (+4.58%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+1.53%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+0.76%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 78% | Extreme gain today (+6.02%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.17%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.39%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
