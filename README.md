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

> 🕐 **Last updated:** 2026-08-25 21:23 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$108,517.30` |
| 💸 Cash Available    | `$-116,097.53` |
| 🧾 Buying Power      | `$96,593.93` |
| 🟢 Total P&L | `+$21,126.31` &nbsp; `(+211.26%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$21,126.31` (+211.26%)
- **Yesterday-to-today P&L:** `+$219.94`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 85% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $309.41 | $21,659.04 | 🟢 +$129.43 | +0.60% |
| **AMZN** | STOCK | 58.00 | $249.54 | $260.86 | $15,129.88 | 🟢 +$656.58 | +4.54% |
| **AVGO** | STOCK | 20.00 | $382.79 | $357.80 | $7,156.00 | 🔴 $-499.85 | -6.53% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $78,260.90 | $17,968.31 | 🟢 +$15,720.16 | +699.25% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,428.70 | $1,523.38 | 🟢 +$1,523.38 | 0.00% |
| **GOOGL** | STOCK | 31.00 | $351.54 | $347.10 | $10,760.13 | 🔴 $-137.46 | -1.26% |
| **LLY** | STOCK | 43.00 | $1,177.63 | $1,233.00 | $53,019.00 | 🟢 +$2,380.80 | +4.70% |
| **META** | STOCK | 33.00 | $591.43 | $568.04 | $18,745.28 | 🔴 $-771.91 | -3.96% |
| **MSFT** | STOCK | 32.00 | $416.49 | $491.33 | $15,722.66 | 🟢 +$2,395.03 | +17.97% |
| **NVDA** | STOCK | 177.00 | $214.65 | $213.78 | $37,838.79 | 🔴 $-154.79 | -0.41% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $96.49 | $1,487.70 | 🟢 +$1,487.70 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $765.98 | $4,595.88 | 🟢 +$123.22 | +2.75% |
| **TSLA** | STOCK | 24.00 | $432.23 | $350.83 | $8,419.92 | 🔴 $-1,953.65 | -18.83% |
| **VTI** | ETF | 28.00 | $370.04 | $378.17 | $10,588.87 | 🟢 +$227.67 | +2.20% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $213.05 | 🟢 +2.19% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $309.90 | 🔴 -0.14% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $346.96 | 🔴 -0.32% | **BUY** | 73% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $491.71 | 🟢 +0.90% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $261.06 | 🔴 -0.39% | **BUY** | 74% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $378.15 | 🟢 +0.29% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $356.74 | 🔴 -0.56% | **BUY** | 76% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $78,339.53 | 🔴 -0.81% | **BUY** | 79% |
| 9 | **META** | Meta Platforms Inc. | STOCK | $570.05 | 🟢 +1.97% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,233.66 | 🔴 -1.06% | **BUY** | 85% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+2.19%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.14%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.32%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.90%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.29%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 67% | Moderate negative momentum (-0.56%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 69% | Moderate negative momentum (-0.81%) — continuation expected |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.97%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 74% | Moderate negative momentum (-1.06%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
