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

> 🕐 **Last updated:** 2026-08-07 14:10 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$105,810.55` |
| 💸 Cash Available    | `$-79,368.48` |
| 🧾 Buying Power      | `$134,568.51` |
| 🟢 Total P&L | `+$19,603.75` &nbsp; `(+196.04%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$19,603.75` (+196.04%)
- **Yesterday-to-today P&L:** `+$775.40`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 77% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 61.00 | $307.66 | $312.37 | $19,054.57 | 🟢 +$287.37 | +1.53% |
| **AMZN** | STOCK | 39.00 | $243.03 | $274.96 | $10,723.64 | 🟢 +$1,245.52 | +13.14% |
| **AVGO** | STOCK | 10.00 | $380.24 | $423.80 | $4,238.01 | 🟢 +$435.58 | +11.46% |
| **BTC/USD** | CRYPTO | 0.2941 | $21,410.95 | $64,739.24 | $19,042.12 | 🟢 +$12,744.40 | +202.37% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,913.70 | $1,200.35 | 🟢 +$1,200.35 | 0.00% |
| **GOOGL** | STOCK | 21.00 | $354.03 | $355.80 | $7,471.80 | 🟢 +$37.09 | +0.50% |
| **LLY** | STOCK | 33.00 | $1,160.01 | $1,189.07 | $39,239.14 | 🟢 +$958.66 | +2.50% |
| **META** | STOCK | 26.00 | $597.38 | $590.72 | $15,358.78 | 🔴 $-173.11 | -1.11% |
| **MSFT** | STOCK | 24.00 | $391.93 | $501.57 | $12,037.74 | 🟢 +$2,631.37 | +27.97% |
| **NVDA** | STOCK | 157.00 | $214.30 | $222.24 | $34,891.68 | 🟢 +$1,246.34 | +3.70% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.98 | $1,140.68 | 🟢 +$1,140.68 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $770.55 | $4,623.30 | 🟢 +$150.64 | +3.37% |
| **TSLA** | STOCK | 24.00 | $432.23 | $324.49 | $7,787.76 | 🔴 $-2,585.81 | -24.93% |
| **VTI** | ETF | 22.00 | $367.49 | $380.43 | $8,369.46 | 🟢 +$284.67 | +3.52% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $222.13 | 🟢 +1.44% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $312.44 | 🟢 +0.01% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $355.74 | 🔴 -0.56% | **BUY** | 77% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $501.27 | 🟢 +0.28% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $275.04 | 🟢 +1.02% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $380.42 | 🟢 +0.35% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $423.33 | 🟢 +0.66% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $590.19 | 🟢 +0.05% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,767.42 | 🟢 +0.79% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,189.51 | 🔴 -0.20% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.44%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.01%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 68% | Moderate negative momentum (-0.56%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.28%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+1.02%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.35%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+0.66%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.05%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.79%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.20%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
