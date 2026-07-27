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

> 🕐 **Last updated:** 2026-07-27 14:39 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,222.46` |
| 💸 Cash Available    | `$-78,178.33` |
| 🧾 Buying Power      | `$109,366.79` |
| 🟢 Total P&L | `+$11,077.87` &nbsp; `(+110.78%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$11,077.87` (+110.78%)
- **Yesterday-to-today P&L:** `$-141.78`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 95% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $337.41 | $17,882.73 | 🟢 +$1,608.86 | +9.89% |
| **AMZN** | STOCK | 54.00 | $240.34 | $234.03 | $12,637.62 | 🔴 $-340.97 | -2.63% |
| **AVGO** | STOCK | 15.00 | $380.02 | $375.68 | $5,635.20 | 🔴 $-65.10 | -1.14% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $64,500.00 | $17,916.60 | 🟢 +$12,670.83 | +241.54% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,921.18 | $1,205.04 | 🟢 +$1,205.04 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $325.44 | $9,112.32 | 🔴 $-771.65 | -7.81% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,203.17 | $32,485.59 | 🟢 +$1,113.56 | +3.55% |
| **META** | STOCK | 24.00 | $601.30 | $602.21 | $14,453.04 | 🟢 +$21.92 | +0.15% |
| **MSFT** | STOCK | 33.00 | $391.33 | $390.47 | $12,885.51 | 🔴 $-28.46 | -0.22% |
| **NVDA** | STOCK | 147.00 | $215.64 | $199.47 | $29,322.09 | 🔴 $-2,376.59 | -7.50% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.18 | $1,159.18 | 🟢 +$1,159.18 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $738.00 | $4,428.03 | 🔴 $-44.63 | -1.00% |
| **TSLA** | STOCK | 24.00 | $432.23 | $306.30 | $7,351.20 | 🔴 $-3,022.37 | -29.14% |
| **VTI** | ETF | 19.00 | $367.28 | $364.56 | $6,926.64 | 🔴 $-51.75 | -0.74% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $337.52 | 🟢 +1.35% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $199.46 | 🔴 -3.57% | **BUY** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $325.52 | 🟢 +1.81% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $390.45 | 🟢 +2.29% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $234.05 | 🟢 +0.84% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $364.55 | 🔴 -0.07% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $375.69 | 🔴 -1.63% | **BUY** | 95% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $602.39 | 🟢 +1.21% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,544.91 | 🔴 -1.21% | **BUY** | 85% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,202.84 | 🟢 +0.57% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.35%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 73% | Extreme loss today (-3.57%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.81%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+2.29%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.84%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.07%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 84% | Moderate negative momentum (-1.63%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.21%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 75% | Moderate negative momentum (-1.21%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.57%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
