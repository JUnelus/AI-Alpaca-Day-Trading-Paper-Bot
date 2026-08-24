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

> 🕐 **Last updated:** 2026-08-24 14:01 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$108,386.41` |
| 💸 Cash Available    | `$-111,661.43` |
| 🧾 Buying Power      | `$101,626.02` |
| 🟢 Total P&L | `+$20,995.41` &nbsp; `(+209.95%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$20,995.41` (+209.95%)
- **Yesterday-to-today P&L:** `+$1,230.22`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AVGO** | BUY | 95% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 79% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 70.00 | $307.57 | $312.68 | $21,887.60 | 🟢 +$357.99 | +1.66% |
| **AMZN** | STOCK | 58.00 | $249.54 | $262.90 | $15,248.49 | 🟢 +$775.19 | +5.36% |
| **AVGO** | STOCK | 18.00 | $385.06 | $362.84 | $6,531.12 | 🔴 $-400.01 | -5.77% |
| **BTC/USD** | CRYPTO | 0.2296 | $9,791.79 | $78,660.28 | $18,060.00 | 🟢 +$15,811.86 | +703.33% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,493.82 | $1,564.22 | 🟢 +$1,564.22 | 0.00% |
| **GOOGL** | STOCK | 31.00 | $351.54 | $348.73 | $10,810.63 | 🔴 $-86.96 | -0.80% |
| **LLY** | STOCK | 41.00 | $1,174.30 | $1,244.82 | $51,037.62 | 🟢 +$2,891.21 | +6.01% |
| **META** | STOCK | 33.00 | $591.43 | $553.95 | $18,280.35 | 🔴 $-1,236.84 | -6.34% |
| **MSFT** | STOCK | 32.00 | $416.49 | $487.63 | $15,604.32 | 🟢 +$2,276.69 | +17.08% |
| **NVDA** | STOCK | 173.00 | $214.75 | $209.84 | $36,303.18 | 🔴 $-849.27 | -2.29% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $94.78 | $1,461.39 | 🟢 +$1,461.39 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $763.74 | $4,582.44 | 🟢 +$109.78 | +2.45% |
| **TSLA** | STOCK | 24.00 | $432.23 | $353.78 | $8,490.72 | 🔴 $-1,882.85 | -18.15% |
| **VTI** | ETF | 27.00 | $369.73 | $377.25 | $10,185.75 | 🟢 +$203.00 | +2.03% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $209.59 | 🔴 -2.39% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $312.51 | 🟢 +1.02% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $348.66 | 🟢 +1.11% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $487.14 | 🟢 +0.81% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $262.74 | 🟢 +1.59% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $377.13 | 🔴 -0.29% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $362.50 | 🔴 -1.61% | **BUY** | 95% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $78,669.38 | 🟢 +1.20% | HOLD | — |
| 9 | **META** | Meta Platforms Inc. | STOCK | $553.50 | 🟢 +0.65% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,246.27 | 🔴 -0.73% | **BUY** | 79% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-2.39%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.02%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.11%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.81%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.59%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.29%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 84% | Moderate negative momentum (-1.61%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.20%) — continuation expected |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.65%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 69% | Moderate negative momentum (-0.73%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
