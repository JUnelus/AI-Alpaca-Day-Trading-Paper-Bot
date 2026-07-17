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

> 🕐 **Last updated:** 2026-07-17 21:31 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,754.53` |
| 💸 Cash Available    | `$-62,668.56` |
| 🧾 Buying Power      | `$137,509.58` |
| 🟢 Total P&L | `+$14,607.42` &nbsp; `(+146.07%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$14,607.42` (+146.07%)
- **Yesterday-to-today P&L:** `$-1,654.12`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 50.00 | $305.94 | $333.85 | $16,692.49 | 🟢 +$1,395.40 | +9.12% |
| **AMZN** | STOCK | 44.00 | $240.09 | $247.20 | $10,876.80 | 🟢 +$312.64 | +2.96% |
| **AVGO** | STOCK | 12.00 | $379.00 | $370.59 | $4,447.08 | 🔴 $-100.93 | -2.22% |
| **BTC/USD** | CRYPTO | 0.2617 | $16,053.40 | $64,151.74 | $16,789.60 | 🟢 +$12,588.15 | +299.61% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,842.11 | $1,155.45 | 🟢 +$1,155.45 | 0.00% |
| **GOOGL** | STOCK | 26.00 | $353.09 | $346.61 | $9,011.82 | 🔴 $-168.42 | -1.83% |
| **LLY** | STOCK | 24.00 | $1,161.99 | $1,174.82 | $28,195.67 | 🟢 +$307.80 | +1.10% |
| **META** | STOCK | 20.00 | $595.27 | $644.89 | $12,897.72 | 🟢 +$992.31 | +8.33% |
| **MSFT** | STOCK | 30.00 | $391.05 | $394.40 | $11,832.00 | 🟢 +$100.40 | +0.86% |
| **NVDA** | STOCK | 139.00 | $216.15 | $202.74 | $28,180.86 | 🔴 $-1,863.70 | -6.20% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $74.95 | $1,155.58 | 🟢 +$1,155.58 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $743.10 | $4,458.60 | 🔴 $-14.06 | -0.31% |
| **TSLA** | STOCK | 24.00 | $432.23 | $380.00 | $9,120.00 | 🔴 $-1,253.57 | -12.08% |
| **VTI** | ETF | 18.00 | $367.17 | $367.19 | $6,609.45 | 🟢 +$0.39 | +0.01% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $202.81 | 🔴 -2.21% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $333.74 | 🟢 +0.14% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $346.77 | 🔴 -2.17% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $393.82 | 🔴 -1.82% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $247.23 | 🔴 -1.06% | **BUY** | 85% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $367.01 | 🔴 -0.96% | **BUY** | 83% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $370.82 | 🔴 -0.97% | **BUY** | 83% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $646.01 | 🔴 -2.79% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,116.80 | 🟢 +0.52% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,179.11 | 🟢 +0.85% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-2.21%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.14%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 85% | Moderate negative momentum (-2.17%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.82%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 75% | Moderate negative momentum (-1.06%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 73% | Moderate negative momentum (-0.96%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 73% | Moderate negative momentum (-0.97%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 69% | Extreme loss today (-2.79%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.52%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.85%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
