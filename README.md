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

> 🕐 **Last updated:** 2026-07-23 14:31 UTC &nbsp;|&nbsp; **Trades today:** 0 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,702.03` |
| 💸 Cash Available    | `$-75,035.14` |
| 🧾 Buying Power      | `$0.00` |
| 🟢 Total P&L | `+$11,556.29` &nbsp; `(+115.56%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$11,556.29` (+115.56%)
- **Yesterday-to-today P&L:** `$-2,419.61`
- **Executed today:** No buy/sell orders were approved in this run.

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $322.05 | $17,068.65 | 🟢 +$794.78 | +4.88% |
| **AMZN** | STOCK | 50.00 | $240.90 | $234.57 | $11,728.50 | 🔴 $-316.33 | -2.63% |
| **AVGO** | STOCK | 13.00 | $379.10 | $395.40 | $5,140.14 | 🟢 +$211.79 | +4.30% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $65,153.10 | $18,098.01 | 🟢 +$12,852.24 | +245.00% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,900.25 | $1,191.91 | 🟢 +$1,191.91 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $318.51 | $8,918.42 | 🔴 $-965.55 | -9.77% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,178.50 | $31,819.50 | 🟢 +$447.47 | +1.43% |
| **META** | STOCK | 23.00 | $600.93 | $607.40 | $13,970.20 | 🟢 +$148.80 | +1.08% |
| **MSFT** | STOCK | 33.00 | $391.33 | $383.85 | $12,666.89 | 🔴 $-247.08 | -1.91% |
| **NVDA** | STOCK | 143.00 | $215.88 | $208.42 | $29,804.06 | 🔴 $-1,066.88 | -3.46% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.89 | $1,185.60 | 🟢 +$1,185.60 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $739.47 | $4,436.82 | 🔴 $-35.84 | -0.80% |
| **TSLA** | STOCK | 24.00 | $432.23 | $323.65 | $7,767.60 | 🔴 $-2,605.97 | -25.12% |
| **VTI** | ETF | 19.00 | $367.28 | $365.25 | $6,939.75 | 🔴 $-38.64 | -0.55% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $208.57 | 🔴 -1.64% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $321.72 | 🔴 -1.28% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $318.35 | 🔴 -6.94% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $383.37 | 🔴 -1.79% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $234.54 | 🔴 -4.21% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.32 | 🔴 -0.96% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $395.67 | 🔴 -0.29% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $606.65 | 🔴 -3.27% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $65,097.71 | 🔴 -1.49% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,178.14 | 🟢 +1.30% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-1.64%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.28%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 78% | Extreme loss today (-6.94%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.79%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 76% | Extreme loss today (-4.21%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 73% | Moderate negative momentum (-0.96%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (-0.29%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 71% | Extreme loss today (-3.27%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 75% | Moderate negative momentum (-1.49%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.30%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
