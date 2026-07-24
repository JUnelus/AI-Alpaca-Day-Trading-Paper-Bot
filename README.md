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

> 🕐 **Last updated:** 2026-07-24 14:22 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$95,669.98` |
| 💸 Cash Available    | `$-75,035.15` |
| 🧾 Buying Power      | `$114,528.06` |
| 🟢 Total P&L | `+$11,526.50` &nbsp; `(+115.27%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$11,526.50` (+115.27%)
- **Yesterday-to-today P&L:** `+$72.08`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 97% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $307.05 | $328.91 | $17,432.23 | 🟢 +$1,158.36 | +7.12% |
| **AMZN** | STOCK | 51.00 | $240.73 | $232.40 | $11,852.41 | 🔴 $-424.91 | -3.46% |
| **AVGO** | STOCK | 13.00 | $379.10 | $383.19 | $4,981.47 | 🟢 +$53.12 | +1.08% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $63,745.49 | $17,707.01 | 🟢 +$12,461.24 | +237.55% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,853.40 | $1,162.53 | 🟢 +$1,162.53 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $321.07 | $8,989.96 | 🔴 $-894.01 | -9.05% |
| **LLY** | STOCK | 27.00 | $1,161.93 | $1,204.49 | $32,521.23 | 🟢 +$1,149.20 | +3.66% |
| **META** | STOCK | 23.00 | $600.93 | $605.10 | $13,917.18 | 🟢 +$95.78 | +0.69% |
| **MSFT** | STOCK | 33.00 | $391.33 | $382.92 | $12,636.36 | 🔴 $-277.61 | -2.15% |
| **NVDA** | STOCK | 143.00 | $215.88 | $207.75 | $29,708.97 | 🔴 $-1,161.98 | -3.76% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $74.00 | $1,140.99 | 🟢 +$1,140.99 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $739.32 | $4,435.92 | 🔴 $-36.74 | -0.82% |
| **TSLA** | STOCK | 24.00 | $432.23 | $313.15 | $7,515.60 | 🔴 $-2,857.97 | -27.55% |
| **VTI** | ETF | 19.00 | $367.28 | $365.10 | $6,936.90 | 🔴 $-41.49 | -0.59% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $207.72 | 🔴 -0.50% | **BUY** | 76% |
| 2 | **AAPL** | Apple Inc. | STOCK | $328.74 | 🟢 +2.20% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $321.05 | 🟢 +1.06% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $382.88 | 🟢 +0.34% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $232.44 | 🔴 -0.52% | **BUY** | 76% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $365.07 | 🟢 +0.10% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $383.06 | 🔴 -2.40% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $604.52 | 🔴 -0.26% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,770.34 | 🔴 -1.99% | **BUY** | 97% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,204.33 | 🟢 +1.56% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 67% | Moderate negative momentum (-0.50%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+2.20%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.06%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.34%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 67% | Moderate negative momentum (-0.52%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.10%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 85% | Moderate negative momentum (-2.40%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.26%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-1.99%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.56%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
