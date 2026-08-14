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

> 🕐 **Last updated:** 2026-08-14 14:11 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$104,983.62` |
| 💸 Cash Available    | `$-97,155.04` |
| 🧾 Buying Power      | `$108,140.99` |
| 🟢 Total P&L | `+$18,778.86` &nbsp; `(+187.79%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$18,778.86` (+187.79%)
- **Yesterday-to-today P&L:** `$-1,012.58`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $305.79 | $20,487.93 | 🔴 $-111.40 | -0.54% |
| **AMZN** | STOCK | 44.00 | $246.06 | $264.66 | $11,645.11 | 🟢 +$818.30 | +7.56% |
| **AVGO** | STOCK | 12.00 | $387.61 | $401.26 | $4,815.12 | 🟢 +$163.78 | +3.52% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $62,596.90 | $19,429.76 | 🟢 +$12,085.90 | +164.57% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,867.06 | $1,171.09 | 🟢 +$1,171.09 | 0.00% |
| **GOOGL** | STOCK | 25.00 | $353.71 | $348.19 | $8,704.88 | 🔴 $-137.76 | -1.56% |
| **LLY** | STOCK | 40.00 | $1,167.80 | $1,182.70 | $47,308.00 | 🟢 +$595.82 | +1.28% |
| **META** | STOCK | 28.00 | $596.63 | $598.26 | $16,751.28 | 🟢 +$45.77 | +0.27% |
| **MSFT** | STOCK | 28.00 | $407.09 | $497.77 | $13,937.56 | 🟢 +$2,539.11 | +22.28% |
| **NVDA** | STOCK | 161.00 | $214.48 | $226.03 | $36,391.64 | 🟢 +$1,860.29 | +5.39% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.39 | $1,162.42 | 🟢 +$1,162.42 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $778.44 | $4,670.64 | 🟢 +$197.98 | +4.43% |
| **TSLA** | STOCK | 24.00 | $432.23 | $349.24 | $8,381.76 | 🔴 $-1,991.81 | -19.20% |
| **VTI** | ETF | 22.00 | $367.49 | $384.74 | $8,464.18 | 🟢 +$379.39 | +4.69% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $226.24 | 🟢 +0.42% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $305.94 | 🟢 +0.22% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $347.79 | 🟢 +0.41% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $497.81 | 🟢 +0.19% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $264.52 | 🔴 -0.23% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $384.73 | 🟢 +0.11% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $401.02 | 🔴 -4.02% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $598.03 | 🟢 +0.51% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,574.41 | 🔴 -1.35% | **BUY** | 85% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,183.42 | 🔴 -2.12% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+0.42%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.22%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.41%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.19%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.23%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.11%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 75% | Extreme loss today (-4.02%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.51%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 75% | Moderate negative momentum (-1.35%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 85% | Moderate negative momentum (-2.12%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
