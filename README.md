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

> 🕐 **Last updated:** 2026-07-07 21:43 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$97,354.91` |
| 💸 Cash Available    | `$-34,363.84` |
| 🧾 Buying Power      | `$178,447.90` |
| 🟢 Total P&L | `+$13,808.45` &nbsp; `(+138.08%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$13,808.45` (+138.08%)
- **Yesterday-to-today P&L:** `+$15,249.08`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 83% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 48.00 | $305.22 | $310.56 | $14,906.70 | 🟢 +$256.16 | +1.75% |
| **AMZN** | STOCK | 28.00 | $237.74 | $245.20 | $6,865.60 | 🟢 +$208.96 | +3.14% |
| **AVGO** | STOCK | 11.00 | $374.42 | $367.84 | $4,046.29 | 🔴 $-72.33 | -1.76% |
| **BTC/USD** | CRYPTO | 0.2114 | $4,965.81 | $63,367.13 | $13,398.53 | 🟢 +$12,348.55 | +1176.07% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,771.82 | $1,111.36 | 🟢 +$1,111.36 | 0.00% |
| **GOOGL** | STOCK | 16.00 | $352.54 | $366.04 | $5,856.64 | 🟢 +$216.04 | +3.83% |
| **LLY** | STOCK | 16.00 | $1,151.91 | $1,235.96 | $19,775.43 | 🟢 +$1,344.86 | +7.30% |
| **META** | STOCK | 18.00 | $572.09 | $615.52 | $11,079.36 | 🟢 +$781.77 | +7.59% |
| **MSFT** | STOCK | 24.00 | $393.23 | $389.50 | $9,348.00 | 🔴 $-89.47 | -0.95% |
| **NVDA** | STOCK | 132.00 | $217.83 | $195.95 | $25,865.40 | 🔴 $-2,888.70 | -10.05% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $80.75 | $1,245.12 | 🟢 +$1,245.12 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $746.11 | $4,476.66 | 🟢 +$4.00 | +0.09% |
| **TSLA** | STOCK | 24.00 | $432.23 | $403.50 | $9,684.00 | 🔴 $-689.57 | -6.65% |
| **VTI** | ETF | 11.00 | $366.18 | $369.06 | $4,059.66 | 🟢 +$31.70 | +0.79% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $196.93 | 🟢 +0.71% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $310.66 | 🔴 -0.64% | **BUY** | 79% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $367.03 | 🟢 +0.16% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $388.84 | 🟢 +0.54% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $245.98 | 🟢 +0.75% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $369.61 | 🔴 -0.55% | **BUY** | 76% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $370.78 | 🔴 -0.83% | **BUY** | 81% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $615.58 | 🟢 +2.55% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,338.88 | 🔴 -1.06% | **BUY** | 83% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,235.56 | 🟢 +2.96% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+0.71%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 70% | Moderate negative momentum (-0.64%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.16%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.54%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.75%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 67% | Moderate negative momentum (-0.55%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 71% | Moderate negative momentum (-0.83%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 68% | Extreme gain today (+2.55%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 73% | Moderate negative momentum (-1.06%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 70% | Extreme gain today (+2.96%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
