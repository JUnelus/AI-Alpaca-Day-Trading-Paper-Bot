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

> 🕐 **Last updated:** 2026-08-10 21:27 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$106,582.87` |
| 💸 Cash Available    | `$-83,095.60` |
| 🧾 Buying Power      | `$128,987.46` |
| 🟢 Total P&L | `+$20,377.38` &nbsp; `(+203.77%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$20,377.38` (+203.77%)
- **Yesterday-to-today P&L:** `+$561.85`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AAPL** | BUY | 97% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 62.00 | $307.64 | $307.60 | $19,071.20 | 🔴 $-2.43 | -0.01% |
| **AMZN** | STOCK | 39.00 | $243.03 | $277.48 | $10,821.72 | 🟢 +$1,343.61 | +14.18% |
| **AVGO** | STOCK | 10.00 | $380.24 | $421.65 | $4,216.48 | 🟢 +$414.06 | +10.89% |
| **BTC/USD** | CRYPTO | 0.3022 | $22,565.81 | $63,985.92 | $19,337.53 | 🟢 +$12,517.80 | +183.55% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,874.70 | $1,175.89 | 🟢 +$1,175.89 | 0.00% |
| **GOOGL** | STOCK | 23.00 | $354.15 | $357.36 | $8,219.28 | 🟢 +$73.92 | +0.91% |
| **LLY** | STOCK | 34.00 | $1,161.41 | $1,229.00 | $41,786.00 | 🟢 +$2,298.14 | +5.82% |
| **META** | STOCK | 26.00 | $597.38 | $594.06 | $15,445.68 | 🔴 $-86.21 | -0.56% |
| **MSFT** | STOCK | 24.00 | $391.93 | $506.50 | $12,156.00 | 🟢 +$2,749.63 | +29.23% |
| **NVDA** | STOCK | 159.00 | $214.40 | $218.76 | $34,782.84 | 🟢 +$693.99 | +2.04% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.19 | $1,174.73 | 🟢 +$1,174.73 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $773.02 | $4,638.12 | 🟢 +$165.46 | +3.70% |
| **TSLA** | STOCK | 24.00 | $432.23 | $329.98 | $7,919.52 | 🔴 $-2,454.05 | -23.66% |
| **VTI** | ETF | 22.00 | $367.49 | $381.71 | $8,397.64 | 🟢 +$312.85 | +3.87% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $217.55 | 🔴 -2.86% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $308.26 | 🔴 -1.62% | **BUY** | 97% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $357.52 | 🟢 +0.91% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $506.06 | 🟢 +1.21% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $278.09 | 🟢 +1.32% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $381.63 | 🔴 -0.04% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $422.40 | 🔴 -1.25% | **BUY** | 85% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $594.92 | 🟢 +0.48% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,032.59 | 🔴 -1.28% | **BUY** | 85% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,231.94 | 🟢 +3.90% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 69% | Extreme loss today (-2.86%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **SELL** | 85% | Moderate negative momentum (-1.62%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.91%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.21%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.32%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.04%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 75% | Moderate negative momentum (-1.25%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.48%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 75% | Moderate negative momentum (-1.28%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 74% | Extreme gain today (+3.90%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
