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

> 🕐 **Last updated:** 2026-06-16 22:01 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$94,935.43` |
| 💸 Cash Available    | `$3,957.15` |
| 🧾 Buying Power      | `$237,108.62` |
| 🔴 Total P&L | `$-3,989.58` &nbsp; `(-39.90%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-3,989.58` (-39.90%)
- **Yesterday-to-today P&L:** `$-793.39`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 80% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 77% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $308.82 | $298.99 | $15,547.48 | 🔴 $-510.93 | -3.18% |
| **AMZN** | STOCK | 20.00 | $243.99 | $246.00 | $4,920.00 | 🟢 +$40.13 | +0.82% |
| **AVGO** | STOCK | 12.00 | $391.94 | $377.50 | $4,530.00 | 🔴 $-173.29 | -3.68% |
| **BTC/USD** | CRYPTO | 0.0335 | $72,003.08 | $65,743.09 | $2,204.34 | 🔴 $-209.89 | -8.69% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,794.20 | $1,125.39 | 🔴 $-205.80 | -15.46% |
| **GOOGL** | STOCK | 7.0000 | $361.34 | $371.75 | $2,602.24 | 🟢 +$72.89 | +2.88% |
| **LLY** | STOCK | 5.0000 | $1,147.65 | $1,121.90 | $5,609.52 | 🔴 $-128.75 | -2.24% |
| **META** | STOCK | 10.00 | $594.97 | $599.50 | $5,995.00 | 🟢 +$45.27 | +0.76% |
| **MSFT** | STOCK | 17.00 | $420.74 | $392.79 | $6,677.43 | 🔴 $-475.06 | -6.64% |
| **NVDA** | STOCK | 102.00 | $223.68 | $207.85 | $21,200.63 | 🔴 $-1,614.71 | -7.08% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $74.01 | $1,141.08 | 🔴 $-187.30 | -14.10% |
| **SPY** | STOCK | 6.0000 | $745.44 | $750.40 | $4,502.40 | 🟢 +$29.74 | +0.66% |
| **TSLA** | STOCK | 24.00 | $432.23 | $403.59 | $9,686.16 | 🔴 $-687.41 | -6.63% |
| **VTI** | ETF | 4.0000 | $366.61 | $370.49 | $1,481.96 | 🟢 +$15.53 | +1.06% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $207.41 | 🔴 -2.37% | **BUY** | 100% |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $373.25 | 🟢 +1.06% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $299.24 | 🟢 +0.95% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $393.83 | 🔴 -1.48% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $246.00 | 🔴 -0.01% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $370.37 | 🔴 -0.58% | **BUY** | 77% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $376.71 | 🔴 -4.37% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $600.21 | 🟢 +1.13% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $65,680.42 | 🔴 -0.91% | **BUY** | 80% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,122.50 | 🔴 -0.61% | **BUY** | 77% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-2.37%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.06%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.95%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.48%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.01%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 68% | Moderate negative momentum (-0.58%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 77% | Extreme loss today (-4.37%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.13%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 71% | Moderate negative momentum (-0.91%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 68% | Moderate negative momentum (-0.61%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
