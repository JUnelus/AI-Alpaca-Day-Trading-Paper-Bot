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

> 🕐 **Last updated:** 2026-08-12 14:11 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$104,960.03` |
| 💸 Cash Available    | `$-89,965.47` |
| 🧾 Buying Power      | `$114,730.67` |
| 🟢 Total P&L | `+$18,755.79` &nbsp; `(+187.56%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$18,755.79` (+187.56%)
- **Yesterday-to-today P&L:** `$-178.21`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 99% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 96% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 80% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 65.00 | $307.59 | $302.72 | $19,676.80 | 🔴 $-316.30 | -1.58% |
| **AMZN** | STOCK | 41.00 | $244.52 | $270.35 | $11,084.15 | 🟢 +$1,058.97 | +10.56% |
| **AVGO** | STOCK | 12.00 | $387.61 | $421.92 | $5,063.04 | 🟢 +$411.70 | +8.85% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $63,793.65 | $19,801.23 | 🟢 +$12,457.36 | +169.63% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,888.93 | $1,184.81 | 🟢 +$1,184.81 | 0.00% |
| **GOOGL** | STOCK | 25.00 | $353.71 | $343.38 | $8,584.62 | 🔴 $-258.01 | -2.92% |
| **LLY** | STOCK | 36.00 | $1,164.20 | $1,204.44 | $43,360.02 | 🟢 +$1,448.98 | +3.46% |
| **META** | STOCK | 26.00 | $597.38 | $588.92 | $15,312.05 | 🔴 $-219.84 | -1.42% |
| **MSFT** | STOCK | 26.00 | $400.32 | $494.69 | $12,862.07 | 🟢 +$2,453.77 | +23.58% |
| **NVDA** | STOCK | 161.00 | $214.48 | $223.09 | $35,917.49 | 🟢 +$1,386.15 | +4.01% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.88 | $1,169.98 | 🟢 +$1,169.98 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $772.58 | $4,635.48 | 🟢 +$162.82 | +3.64% |
| **TSLA** | STOCK | 24.00 | $432.23 | $328.07 | $7,873.73 | 🔴 $-2,499.84 | -24.10% |
| **VTI** | ETF | 22.00 | $367.49 | $381.82 | $8,400.04 | 🟢 +$315.25 | +3.90% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $223.01 | 🟢 +2.54% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $302.94 | 🔴 -0.65% | **BUY** | 79% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $343.49 | 🔴 -0.09% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $494.77 | 🔴 -1.79% | **BUY** | 99% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $270.36 | 🔴 -0.70% | **BUY** | 79% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $381.80 | 🟢 +0.30% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $421.91 | 🟢 +1.40% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $589.29 | 🔴 -1.64% | **BUY** | 96% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,764.75 | 🟢 +0.38% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,205.11 | 🔴 -0.82% | **BUY** | 80% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 68% | Extreme gain today (+2.54%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **SELL** | 70% | Moderate negative momentum (-0.65%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.09%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.79%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 70% | Moderate negative momentum (-0.70%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.30%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.40%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 84% | Moderate negative momentum (-1.64%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.38%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 71% | Moderate negative momentum (-0.82%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
