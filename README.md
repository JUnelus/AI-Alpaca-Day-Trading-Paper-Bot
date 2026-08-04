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

> 🕐 **Last updated:** 2026-08-04 14:35 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$100,928.60` |
| 💸 Cash Available    | `$-77,220.63` |
| 🧾 Buying Power      | `$126,783.48` |
| 🟢 Total P&L | `+$15,107.81` &nbsp; `(+151.08%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$15,107.81` (+151.08%)
- **Yesterday-to-today P&L:** `+$602.76`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AMZN** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **META** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $307.67 | $306.26 | $18,375.60 | 🔴 $-84.67 | -0.46% |
| **AMZN** | STOCK | 36.00 | $238.76 | $278.52 | $10,026.72 | 🟢 +$1,431.51 | +16.65% |
| **AVGO** | STOCK | 16.00 | $381.89 | $409.52 | $6,552.40 | 🟢 +$442.22 | +7.24% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $63,823.93 | $17,728.80 | 🟢 +$12,483.03 | +237.96% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,866.29 | $1,170.61 | 🟢 +$1,170.61 | 0.00% |
| **GOOGL** | STOCK | 18.00 | $351.05 | $375.64 | $6,761.61 | 🟢 +$442.71 | +7.01% |
| **LLY** | STOCK | 34.00 | $1,158.57 | $1,122.82 | $38,175.88 | 🔴 $-1,215.43 | -3.09% |
| **META** | STOCK | 24.00 | $595.27 | $583.33 | $13,999.92 | 🔴 $-286.45 | -2.01% |
| **MSFT** | STOCK | 22.00 | $383.50 | $496.41 | $10,921.04 | 🟢 +$2,483.98 | +29.44% |
| **NVDA** | STOCK | 157.00 | $214.30 | $210.37 | $33,028.09 | 🔴 $-617.25 | -1.83% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.27 | $1,129.73 | 🟢 +$1,129.73 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $765.06 | $4,590.37 | 🟢 +$117.71 | +2.63% |
| **TSLA** | STOCK | 24.00 | $432.23 | $323.33 | $7,759.92 | 🔴 $-2,613.65 | -25.20% |
| **VTI** | ETF | 21.00 | $366.90 | $377.56 | $7,928.65 | 🟢 +$223.76 | +2.90% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $210.18 | 🟢 +1.72% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $375.92 | 🟢 +0.65% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $306.30 | 🟢 +0.95% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $496.21 | 🟢 +1.76% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $278.73 | 🔴 -1.86% | **BUY** | 99% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $377.48 | 🟢 +0.97% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $409.48 | 🟢 +4.40% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $583.58 | 🔴 -1.13% | **BUY** | 85% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,872.37 | 🟢 +0.66% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,122.74 | 🟢 +0.12% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.72%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.65%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.95%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.76%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-1.86%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.97%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 77% | Extreme gain today (+4.40%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 75% | Moderate negative momentum (-1.13%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.66%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.12%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
