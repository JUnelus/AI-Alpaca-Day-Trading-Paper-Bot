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

> 🕐 **Last updated:** 2026-07-16 21:35 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$100,429.74` |
| 💸 Cash Available    | `$-56,166.75` |
| 🧾 Buying Power      | `$151,560.58` |
| 🟢 Total P&L | `+$16,261.53` &nbsp; `(+162.62%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$16,261.53` (+162.62%)
- **Yesterday-to-today P&L:** `$-1,355.95`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AMZN** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **VTI** | BUY | 75% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 81% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 49.00 | $305.86 | $332.80 | $16,307.20 | 🟢 +$1,320.26 | +8.81% |
| **AMZN** | STOCK | 40.00 | $239.44 | $249.88 | $9,995.20 | 🟢 +$417.40 | +4.36% |
| **AVGO** | STOCK | 10.00 | $380.67 | $377.15 | $3,771.50 | 🔴 $-35.22 | -0.93% |
| **BTC/USD** | CRYPTO | 0.2534 | $14,506.86 | $64,120.95 | $16,250.67 | 🟢 +$12,574.08 | +342.00% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,877.70 | $1,177.77 | 🟢 +$1,177.77 | 0.00% |
| **GOOGL** | STOCK | 24.00 | $353.63 | $356.26 | $8,550.24 | 🟢 +$63.15 | +0.74% |
| **LLY** | STOCK | 24.00 | $1,161.99 | $1,171.00 | $28,104.00 | 🟢 +$216.13 | +0.77% |
| **META** | STOCK | 18.00 | $590.18 | $663.98 | $11,951.64 | 🟢 +$1,328.47 | +12.51% |
| **MSFT** | STOCK | 29.00 | $391.00 | $400.15 | $11,604.35 | 🟢 +$265.46 | +2.34% |
| **NVDA** | STOCK | 135.00 | $216.52 | $206.82 | $27,920.70 | 🔴 $-1,309.15 | -4.48% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.67 | $1,166.74 | 🟢 +$1,166.74 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $750.08 | $4,500.48 | 🟢 +$27.82 | +0.62% |
| **TSLA** | STOCK | 24.00 | $432.23 | $390.33 | $9,368.01 | 🔴 $-1,005.56 | -9.69% |
| **VTI** | ETF | 16.00 | $367.11 | $370.50 | $5,928.00 | 🟢 +$54.19 | +0.92% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $207.40 | 🔴 -2.40% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $333.26 | 🟢 +1.76% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $354.46 | 🔴 -4.44% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $401.10 | 🟢 +1.38% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $249.89 | 🔴 -1.99% | **BUY** | 100% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $370.58 | 🔴 -0.49% | **BUY** | 75% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $374.45 | 🔴 -5.03% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $664.54 | 🔴 -2.46% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,127.65 | 🔴 -0.92% | **BUY** | 81% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,169.17 | 🟢 +1.08% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 85% | Moderate negative momentum (-2.40%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.76%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 77% | Extreme loss today (-4.44%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.38%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-1.99%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 66% | Moderate negative momentum (-0.49%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 78% | Extreme loss today (-5.03%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-2.46%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 71% | Moderate negative momentum (-0.92%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+1.08%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
