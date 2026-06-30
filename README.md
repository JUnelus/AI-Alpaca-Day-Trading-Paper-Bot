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

> 🕐 **Last updated:** 2026-06-30 14:37 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$92,904.60` |
| 💸 Cash Available    | `$-23,763.25` |
| 🧾 Buying Power      | `$185,446.50` |
| 🔴 Total P&L | `$-5,860.83` &nbsp; `(-58.61%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-5,860.83` (-58.61%)
- **Yesterday-to-today P&L:** `+$392.78`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **META** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $305.99 | $286.14 | $17,168.40 | 🔴 $-1,191.06 | -6.49% |
| **AMZN** | STOCK | 26.00 | $237.67 | $240.57 | $6,254.82 | 🟢 +$75.52 | +1.22% |
| **AVGO** | STOCK | 9.0000 | $380.51 | $377.42 | $3,396.78 | 🔴 $-27.81 | -0.81% |
| **BTC/USD** | CRYPTO | 0.1857 | $64,221.74 | $58,693.07 | $10,899.74 | 🔴 $-1,026.72 | -8.61% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,569.10 | $984.20 | 🔴 $-346.99 | -26.07% |
| **GOOGL** | STOCK | 13.00 | $353.61 | $353.95 | $4,601.35 | 🟢 +$4.44 | +0.10% |
| **LLY** | STOCK | 10.00 | $1,121.55 | $1,198.00 | $11,980.00 | 🟢 +$764.53 | +6.82% |
| **META** | STOCK | 17.00 | $578.39 | $555.00 | $9,435.00 | 🔴 $-397.68 | -4.04% |
| **MSFT** | STOCK | 22.00 | $393.63 | $372.22 | $8,188.84 | 🔴 $-471.07 | -5.44% |
| **NVDA** | STOCK | 122.00 | $219.68 | $197.94 | $24,148.68 | 🔴 $-2,652.43 | -9.90% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $73.79 | $1,137.70 | 🔴 $-190.68 | -14.35% |
| **SPY** | STOCK | 6.0000 | $745.44 | $744.86 | $4,469.16 | 🔴 $-3.50 | -0.08% |
| **TSLA** | STOCK | 24.00 | $432.23 | $414.36 | $9,944.64 | 🔴 $-428.93 | -4.13% |
| **VTI** | ETF | 11.00 | $366.18 | $369.05 | $4,059.49 | 🟢 +$31.53 | +0.78% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $197.88 | 🟢 +1.49% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $353.73 | 🟢 +0.02% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $286.14 | 🟢 +1.56% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $372.19 | 🟢 +0.98% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $240.63 | 🟢 +0.20% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $369.14 | 🟢 +0.55% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $377.78 | 🟢 +1.43% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $555.08 | 🔴 -1.34% | **BUY** | 85% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $58,727.75 | 🔴 -2.39% | **BUY** | 100% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,199.62 | 🔴 -2.46% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.49%) — continuation expected |
| 2 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.02%) — no trend to carry forward |
| 3 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.56%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.98%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.20%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.55%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.43%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 75% | Moderate negative momentum (-1.34%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.39%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.46%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
