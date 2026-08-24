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

> 🕐 **Last updated:** 2026-08-24 21:23 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$108,297.37` |
| 💸 Cash Available    | `$-113,691.26` |
| 🧾 Buying Power      | `$98,459.31` |
| 🟢 Total P&L | `+$20,906.37` &nbsp; `(+209.06%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$20,906.37` (+209.06%)
- **Yesterday-to-today P&L:** `+$1,141.18`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **VTI** | BUY | 72% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 78% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $310.81 | $21,756.79 | 🟢 +$227.19 | +1.06% |
| **AMZN** | STOCK | 58.00 | $249.54 | $262.22 | $15,208.97 | 🟢 +$735.67 | +5.08% |
| **AVGO** | STOCK | 19.00 | $383.90 | $359.10 | $6,822.90 | 🔴 $-471.16 | -6.46% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $78,891.46 | $18,113.08 | 🟢 +$15,864.94 | +705.69% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,481.00 | $1,556.18 | 🟢 +$1,556.18 | 0.00% |
| **GOOGL** | STOCK | 31.00 | $351.54 | $348.20 | $10,794.20 | 🔴 $-103.39 | -0.95% |
| **LLY** | STOCK | 42.00 | $1,176.04 | $1,251.03 | $52,543.30 | 🟢 +$3,149.67 | +6.38% |
| **META** | STOCK | 33.00 | $591.43 | $559.01 | $18,447.33 | 🔴 $-1,069.86 | -5.48% |
| **MSFT** | STOCK | 32.00 | $416.49 | $487.41 | $15,597.12 | 🟢 +$2,269.49 | +17.03% |
| **NVDA** | STOCK | 175.00 | $214.70 | $208.70 | $36,522.24 | 🔴 $-1,049.90 | -2.79% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $96.82 | $1,492.85 | 🟢 +$1,492.85 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $764.00 | $4,584.00 | 🟢 +$111.34 | +2.49% |
| **TSLA** | STOCK | 24.00 | $432.23 | $348.25 | $8,357.98 | 🔴 $-2,015.59 | -19.43% |
| **VTI** | ETF | 27.00 | $369.73 | $377.47 | $10,191.69 | 🟢 +$208.94 | +2.09% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.48 | 🔴 -2.91% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $310.34 | 🟢 +0.32% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $348.06 | 🟢 +0.94% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $487.31 | 🟢 +0.84% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $262.07 | 🟢 +1.33% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $377.07 | 🔴 -0.31% | **BUY** | 72% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $358.76 | 🔴 -2.63% | **BUY** | 100% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $78,944.76 | 🟢 +1.56% | HOLD | — |
| 9 | **META** | Meta Platforms Inc. | STOCK | $559.02 | 🟢 +1.66% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,246.93 | 🔴 -0.67% | **BUY** | 78% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 70% | Extreme loss today (-2.91%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.32%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.94%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.84%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.33%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.31%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 68% | Extreme loss today (-2.63%) — mean reversion pullback likely |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.56%) — continuation expected |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.66%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 69% | Moderate negative momentum (-0.67%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
