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

> 🕐 **Last updated:** 2026-08-25 14:02 UTC &nbsp;|&nbsp; **Trades today:** 0 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$109,467.09` |
| 💸 Cash Available    | `$-116,097.53` |
| 🧾 Buying Power      | `$101,388.07` |
| 🟢 Total P&L | `+$22,074.33` &nbsp; `(+220.74%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$22,074.33` (+220.74%)
- **Yesterday-to-today P&L:** `+$1,167.96`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **BTC/USD** | BUY | 72% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $310.01 | $21,700.86 | 🟢 +$171.26 | +0.80% |
| **AMZN** | STOCK | 58.00 | $249.54 | $261.62 | $15,173.96 | 🟢 +$700.66 | +4.84% |
| **AVGO** | STOCK | 20.00 | $382.79 | $359.46 | $7,189.30 | 🔴 $-466.55 | -6.09% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $78,624.89 | $18,051.88 | 🟢 +$15,803.73 | +702.97% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,459.66 | $1,542.80 | 🟢 +$1,542.80 | 0.00% |
| **GOOGL** | STOCK | 31.00 | $351.54 | $347.82 | $10,782.42 | 🔴 $-115.17 | -1.06% |
| **LLY** | STOCK | 43.00 | $1,177.63 | $1,256.61 | $54,034.01 | 🟢 +$3,395.82 | +6.71% |
| **META** | STOCK | 33.00 | $591.43 | $564.20 | $18,618.60 | 🔴 $-898.59 | -4.60% |
| **MSFT** | STOCK | 32.00 | $416.49 | $487.16 | $15,589.12 | 🟢 +$2,261.49 | +16.97% |
| **NVDA** | STOCK | 177.00 | $214.65 | $213.40 | $37,771.80 | 🔴 $-221.78 | -0.58% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $97.13 | $1,497.60 | 🟢 +$1,497.60 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $765.73 | $4,594.35 | 🟢 +$121.69 | +2.72% |
| **TSLA** | STOCK | 24.00 | $432.23 | $351.27 | $8,430.47 | 🔴 $-1,943.10 | -18.73% |
| **VTI** | ETF | 28.00 | $370.04 | $378.06 | $10,585.68 | 🟢 +$224.48 | +2.17% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $213.29 | 🟢 +2.31% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $310.14 | 🔴 -0.06% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $347.74 | 🔴 -0.09% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $487.02 | 🔴 -0.06% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $261.77 | 🔴 -0.11% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $378.09 | 🟢 +0.27% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $359.60 | 🟢 +0.23% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $78,670.36 | 🔴 -0.39% | **BUY** | 72% |
| 9 | **META** | Meta Platforms Inc. | STOCK | $564.33 | 🟢 +0.95% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,256.26 | 🟢 +0.75% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+2.31%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.06%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.09%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.06%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.11%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.27%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (+0.23%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.95%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.75%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
