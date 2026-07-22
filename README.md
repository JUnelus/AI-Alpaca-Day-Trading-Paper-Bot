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

> 🕐 **Last updated:** 2026-07-22 14:29 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,451.66` |
| 💸 Cash Available    | `$-71,643.03` |
| 🧾 Buying Power      | `$121,208.41` |
| 🟢 Total P&L | `+$14,306.30` &nbsp; `(+143.06%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$14,306.30` (+143.06%)
- **Yesterday-to-today P&L:** `$-1,421.70`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 94% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 93% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $306.72 | $324.58 | $16,878.16 | 🟢 +$928.85 | +5.82% |
| **AMZN** | STOCK | 48.00 | $240.78 | $243.78 | $11,701.44 | 🟢 +$144.16 | +1.25% |
| **AVGO** | STOCK | 13.00 | $379.10 | $386.11 | $5,019.43 | 🟢 +$91.08 | +1.85% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.58 | $65,633.27 | $18,231.39 | 🟢 +$12,985.70 | +247.55% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,934.40 | $1,213.33 | 🟢 +$1,213.33 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $353.00 | $347.75 | $9,737.00 | 🔴 $-146.97 | -1.49% |
| **LLY** | STOCK | 26.00 | $1,162.08 | $1,157.38 | $30,091.88 | 🔴 $-122.16 | -0.40% |
| **META** | STOCK | 22.00 | $599.63 | $629.37 | $13,846.14 | 🟢 +$654.21 | +4.96% |
| **MSFT** | STOCK | 32.00 | $391.38 | $389.85 | $12,475.20 | 🔴 $-48.92 | -0.39% |
| **NVDA** | STOCK | 141.00 | $216.01 | $206.63 | $29,135.53 | 🔴 $-1,322.11 | -4.34% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $77.72 | $1,198.35 | 🟢 +$1,198.35 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $747.29 | $4,483.74 | 🟢 +$11.08 | +0.25% |
| **TSLA** | STOCK | 24.00 | $432.23 | $377.52 | $9,060.48 | 🔴 $-1,313.09 | -12.66% |
| **VTI** | ETF | 19.00 | $367.28 | $369.01 | $7,011.19 | 🟢 +$32.80 | +0.47% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $206.62 | 🔴 -0.33% | **BUY** | 73% |
| 2 | **AAPL** | Apple Inc. | STOCK | $324.59 | 🔴 -0.96% | **BUY** | 84% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $347.23 | 🟢 +0.02% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $389.81 | 🔴 -2.00% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $243.83 | 🔴 -1.50% | **BUY** | 94% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.99 | 🔴 -0.12% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $385.82 | 🔴 -0.18% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $629.16 | 🔴 -2.28% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $65,569.71 | 🔴 -1.44% | **BUY** | 85% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,157.46 | 🔴 -1.53% | **BUY** | 93% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.33%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **SELL** | 74% | Moderate negative momentum (-0.96%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.02%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-2.00%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 83% | Moderate negative momentum (-1.50%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.12%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (-0.18%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-2.28%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 75% | Moderate negative momentum (-1.44%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 82% | Moderate negative momentum (-1.53%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
