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

> 🕐 **Last updated:** 2026-08-19 21:22 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$108,506.17` |
| 💸 Cash Available    | `$-108,086.23` |
| 🧾 Buying Power      | `$102,550.96` |
| 🟢 Total P&L | `+$21,196.48` &nbsp; `(+211.96%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$21,196.48` (+211.96%)
- **Yesterday-to-today P&L:** `+$3,954.39`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | SELL | 100% | Take-profit trim after overextended rally |
| **LLY** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $316.43 | $21,201.08 | 🟢 +$601.74 | +2.92% |
| **AMZN** | STOCK | 51.00 | $248.09 | $266.17 | $13,574.67 | 🟢 +$922.07 | +7.29% |
| **AVGO** | STOCK | 17.00 | $386.18 | $364.11 | $6,189.87 | 🔴 $-375.27 | -5.72% |
| **BTC/USD** | CRYPTO | 0.2889 | $23,659.74 | $69,632.20 | $20,116.39 | 🟢 +$13,281.21 | +194.31% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,266.48 | $1,421.63 | 🟢 +$1,421.63 | 0.00% |
| **GOOGL** | STOCK | 29.00 | $352.18 | $344.12 | $9,979.48 | 🔴 $-233.74 | -2.29% |
| **LLY** | STOCK | 40.00 | $1,168.10 | $1,279.99 | $51,199.60 | 🟢 +$4,475.52 | +9.58% |
| **META** | STOCK | 33.00 | $591.43 | $547.42 | $18,064.80 | 🔴 $-1,452.39 | -7.44% |
| **MSFT** | STOCK | 30.00 | $412.13 | $484.52 | $14,535.60 | 🟢 +$2,171.82 | +17.57% |
| **NVDA** | STOCK | 167.00 | $214.69 | $218.30 | $36,456.10 | 🟢 +$602.88 | +1.68% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $86.53 | $1,334.19 | 🟢 +$1,334.19 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $769.04 | $4,614.24 | 🟢 +$141.58 | +3.17% |
| **TSLA** | STOCK | 24.00 | $432.23 | $350.00 | $8,400.00 | 🔴 $-1,973.57 | -19.02% |
| **VTI** | ETF | 25.00 | $369.04 | $380.19 | $9,504.75 | 🟢 +$278.81 | +3.02% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $217.56 | 🔴 -0.99% | **BUY** | 84% |
| 2 | **AAPL** | Apple Inc. | STOCK | $316.83 | 🟢 +2.19% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $344.72 | 🟢 +0.15% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $484.31 | 🟢 +0.56% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $265.84 | 🟢 +2.46% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $379.99 | 🟢 +0.25% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $362.48 | 🔴 -4.61% | **BUY** | 100% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $69,662.49 | 🟢 +7.69% | **SELL** | 100% |
| 9 | **META** | Meta Platforms Inc. | STOCK | $546.03 | 🟢 +0.43% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,280.34 | 🟢 +4.46% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 74% | Moderate negative momentum (-0.99%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+2.19%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.15%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.56%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+2.46%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.25%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 78% | Extreme loss today (-4.61%) — mean reversion pullback likely |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 78% | Extreme gain today (+7.69%) — mean reversion pullback likely |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.43%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 77% | Extreme gain today (+4.46%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
