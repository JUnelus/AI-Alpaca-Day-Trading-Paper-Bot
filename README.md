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

> 🕐 **Last updated:** 2026-07-21 14:28 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,861.27` |
| 💸 Cash Available    | `$-69,861.48` |
| 🧾 Buying Power      | `$130,051.54` |
| 🟢 Total P&L | `+$15,715.40` &nbsp; `(+157.15%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$15,715.40` (+157.15%)
- **Yesterday-to-today P&L:** `+$1,488.06`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 83% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $306.72 | $326.83 | $16,995.16 | 🟢 +$1,045.85 | +6.56% |
| **AMZN** | STOCK | 46.00 | $240.48 | $247.59 | $11,389.14 | 🟢 +$327.17 | +2.96% |
| **AVGO** | STOCK | 13.00 | $379.10 | $383.62 | $4,987.06 | 🟢 +$58.71 | +1.19% |
| **BTC/USD** | CRYPTO | 0.2698 | $17,502.75 | $66,670.68 | $17,987.53 | 🟢 +$13,265.35 | +280.92% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,926.03 | $1,208.08 | 🟢 +$1,208.08 | 0.00% |
| **GOOGL** | STOCK | 27.00 | $353.13 | $349.56 | $9,437.99 | 🔴 $-96.39 | -1.01% |
| **LLY** | STOCK | 26.00 | $1,162.08 | $1,161.68 | $30,203.68 | 🔴 $-10.36 | -0.03% |
| **META** | STOCK | 22.00 | $599.63 | $647.53 | $14,245.77 | 🟢 +$1,053.84 | +7.99% |
| **MSFT** | STOCK | 31.00 | $391.06 | $401.13 | $12,435.03 | 🟢 +$312.11 | +2.57% |
| **NVDA** | STOCK | 141.00 | $216.01 | $205.32 | $28,950.12 | 🔴 $-1,507.52 | -4.95% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $78.29 | $1,207.14 | 🟢 +$1,207.14 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $746.73 | $4,480.39 | 🟢 +$7.73 | +0.17% |
| **TSLA** | STOCK | 24.00 | $432.23 | $382.94 | $9,190.56 | 🔴 $-1,183.01 | -11.40% |
| **VTI** | ETF | 19.00 | $367.28 | $368.69 | $7,005.11 | 🟢 +$26.72 | +0.38% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $205.23 | 🟢 +0.96% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $326.81 | 🟢 +0.07% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $349.62 | 🔴 -0.67% | **BUY** | 79% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $401.07 | 🔴 -0.30% | **BUY** | 74% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $247.73 | 🔴 -0.90% | **BUY** | 83% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.67 | 🟢 +0.66% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $383.62 | 🟢 +1.44% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $647.50 | 🟢 +0.25% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $66,642.88 | 🟢 +2.20% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,162.43 | 🟢 +1.35% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+0.96%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.07%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 70% | Moderate negative momentum (-0.67%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.30%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 73% | Moderate negative momentum (-0.90%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.66%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.44%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.25%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+2.20%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.35%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
