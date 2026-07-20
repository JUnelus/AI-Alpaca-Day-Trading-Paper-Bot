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

> 🕐 **Last updated:** 2026-07-20 14:32 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,351.55` |
| 💸 Cash Available    | `$-66,240.09` |
| 🧾 Buying Power      | `$134,121.16` |
| 🟢 Total P&L | `+$15,201.50` &nbsp; `(+152.02%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$15,201.50` (+152.02%)
- **Yesterday-to-today P&L:** `+$594.09`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | BUY | 71% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 73% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 50.00 | $305.94 | $326.79 | $16,339.50 | 🟢 +$1,042.41 | +6.81% |
| **AMZN** | STOCK | 46.00 | $240.48 | $249.72 | $11,487.12 | 🟢 +$425.15 | +3.84% |
| **AVGO** | STOCK | 13.00 | $379.10 | $379.89 | $4,938.64 | 🟢 +$10.29 | +0.21% |
| **BTC/USD** | CRYPTO | 0.2698 | $17,502.56 | $64,417.45 | $17,379.62 | 🟢 +$12,657.48 | +268.05% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,860.69 | $1,167.10 | 🟢 +$1,167.10 | 0.00% |
| **GOOGL** | STOCK | 27.00 | $353.13 | $358.24 | $9,672.48 | 🟢 +$138.10 | +1.45% |
| **LLY** | STOCK | 24.00 | $1,161.99 | $1,175.04 | $28,200.96 | 🟢 +$313.09 | +1.12% |
| **META** | STOCK | 21.00 | $597.57 | $642.90 | $13,500.90 | 🟢 +$951.95 | +7.59% |
| **MSFT** | STOCK | 31.00 | $391.06 | $394.77 | $12,238.02 | 🟢 +$115.11 | +0.95% |
| **NVDA** | STOCK | 141.00 | $216.01 | $205.84 | $29,023.43 | 🔴 $-1,434.22 | -4.71% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.44 | $1,178.67 | 🟢 +$1,178.67 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $745.44 | $4,472.64 | 🔴 $-0.02 | -0.00% |
| **TSLA** | STOCK | 24.00 | $432.23 | $374.84 | $8,996.16 | 🔴 $-1,377.41 | -13.28% |
| **VTI** | ETF | 19.00 | $367.28 | $368.01 | $6,992.19 | 🟢 +$13.80 | +0.20% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $205.89 | 🟢 +1.52% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $326.92 | 🔴 -2.04% | **BUY** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $358.71 | 🟢 +3.44% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $394.76 | 🟢 +0.24% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $249.68 | 🟢 +0.99% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.19 | 🟢 +0.32% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $379.94 | 🟢 +2.46% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $642.77 | 🔴 -0.50% | **BUY** | 76% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,467.18 | 🔴 -0.33% | **BUY** | 71% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,175.05 | 🔴 -0.34% | **BUY** | 73% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.52%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 85% | Moderate negative momentum (-2.04%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 72% | Extreme gain today (+3.44%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.24%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.99%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.32%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+2.46%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 67% | Moderate negative momentum (-0.50%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.33%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (-0.34%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
