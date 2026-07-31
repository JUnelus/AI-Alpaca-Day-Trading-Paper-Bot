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

> 🕐 **Last updated:** 2026-07-31 14:32 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$93,953.19` |
| 💸 Cash Available    | `$-85,860.55` |
| 🧾 Buying Power      | `$97,237.96` |
| 🟢 Total P&L | `+$9,520.94` &nbsp; `(+95.21%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$9,520.94` (+95.21%)
- **Yesterday-to-today P&L:** `$-430.15`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | SELL | 100% | Take-profit trim after overextended rally |
| **AMZN** | SELL | 100% | Take-profit trim after overextended rally |
| **AVGO** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 56.00 | $307.91 | $302.43 | $16,936.08 | 🔴 $-306.93 | -1.78% |
| **AMZN** | STOCK | 56.00 | $238.56 | $271.09 | $15,181.04 | 🟢 +$1,821.86 | +13.64% |
| **AVGO** | STOCK | 14.00 | $380.76 | $383.15 | $5,364.10 | 🟢 +$33.42 | +0.63% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $62,615.14 | $17,393.03 | 🟢 +$12,147.26 | +231.56% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,860.50 | $1,166.98 | 🟢 +$1,166.98 | 0.00% |
| **GOOGL** | STOCK | 30.00 | $351.97 | $347.50 | $10,425.00 | 🔴 $-134.20 | -1.27% |
| **LLY** | STOCK | 30.00 | $1,162.10 | $1,128.65 | $33,859.65 | 🔴 $-1,003.39 | -2.88% |
| **META** | STOCK | 28.00 | $594.11 | $546.98 | $15,315.44 | 🔴 $-1,319.71 | -7.93% |
| **MSFT** | STOCK | 28.00 | $387.87 | $453.17 | $12,688.76 | 🟢 +$1,828.45 | +16.84% |
| **NVDA** | STOCK | 157.00 | $214.30 | $196.99 | $30,927.43 | 🔴 $-2,717.91 | -8.08% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.36 | $1,131.20 | 🟢 +$1,131.20 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $740.44 | $4,442.64 | 🔴 $-30.02 | -0.67% |
| **TSLA** | STOCK | 24.00 | $432.23 | $304.58 | $7,310.04 | 🔴 $-3,063.53 | -29.53% |
| **VTI** | ETF | 21.00 | $366.90 | $365.35 | $7,672.35 | 🔴 $-32.54 | -0.42% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $197.41 | 🟢 +1.22% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $302.31 | 🔴 -9.33% | **BUY** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $348.07 | 🟢 +4.32% | **SELL** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $453.11 | 🟢 +0.44% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $271.23 | 🟢 +15.17% | **SELL** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.45 | 🔴 -0.22% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $383.19 | 🔴 -1.20% | **BUY** | 85% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $547.17 | 🟢 +1.51% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,587.88 | 🔴 -3.31% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,129.13 | 🔴 -2.24% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.22%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 78% | Extreme loss today (-9.33%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 77% | Extreme gain today (+4.32%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.44%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 78% | Extreme gain today (+15.17%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.22%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 75% | Moderate negative momentum (-1.20%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.51%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 72% | Extreme loss today (-3.31%) — mean reversion pullback likely |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.24%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
