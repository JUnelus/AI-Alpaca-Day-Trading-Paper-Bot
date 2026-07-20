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

> 🕐 **Last updated:** 2026-07-20 21:38 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,370.32` |
| 💸 Cash Available    | `$-68,385.66` |
| 🧾 Buying Power      | `$128,740.70` |
| 🟢 Total P&L | `+$14,227.34` &nbsp; `(+142.27%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$14,227.34` (+142.27%)
- **Yesterday-to-today P&L:** `$-380.07`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 51.00 | $306.35 | $326.61 | $16,657.11 | 🟢 +$1,033.24 | +6.61% |
| **AMZN** | STOCK | 46.00 | $240.48 | $249.96 | $11,498.16 | 🟢 +$436.19 | +3.94% |
| **AVGO** | STOCK | 13.00 | $379.10 | $378.64 | $4,922.32 | 🔴 $-6.03 | -0.12% |
| **BTC/USD** | CRYPTO | 0.2698 | $17,502.56 | $65,329.72 | $17,625.74 | 🟢 +$12,903.61 | +273.26% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,905.59 | $1,195.26 | 🟢 +$1,195.26 | 0.00% |
| **GOOGL** | STOCK | 27.00 | $353.13 | $352.52 | $9,518.04 | 🔴 $-16.34 | -0.17% |
| **LLY** | STOCK | 25.00 | $1,162.55 | $1,145.44 | $28,636.00 | 🔴 $-427.67 | -1.47% |
| **META** | STOCK | 22.00 | $599.63 | $645.33 | $14,197.26 | 🟢 +$1,005.33 | +7.62% |
| **MSFT** | STOCK | 31.00 | $391.06 | $401.30 | $12,440.30 | 🟢 +$317.38 | +2.62% |
| **NVDA** | STOCK | 141.00 | $216.01 | $202.67 | $28,577.01 | 🔴 $-1,880.64 | -6.17% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $77.77 | $1,199.13 | 🟢 +$1,199.13 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $741.94 | $4,451.64 | 🔴 $-21.02 | -0.47% |
| **TSLA** | STOCK | 24.00 | $432.23 | $370.08 | $8,881.92 | 🔴 $-1,491.65 | -14.38% |
| **VTI** | ETF | 19.00 | $367.28 | $366.26 | $6,958.94 | 🔴 $-19.45 | -0.28% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $203.28 | 🟢 +0.23% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $326.59 | 🔴 -2.14% | **BUY** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $351.99 | 🟢 +1.51% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $402.29 | 🟢 +2.15% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $249.99 | 🟢 +1.12% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $366.25 | 🔴 -0.21% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $378.16 | 🟢 +1.98% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $645.85 | 🔴 -0.02% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $65,396.86 | 🟢 +1.11% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,146.90 | 🔴 -2.73% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.23%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **SELL** | 85% | Moderate negative momentum (-2.14%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.51%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+2.15%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.12%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.21%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.98%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.02%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.11%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 69% | Extreme loss today (-2.73%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
