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

> 🕐 **Last updated:** 2026-08-21 21:22 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$108,945.39` |
| 💸 Cash Available    | `$-110,402.15` |
| 🧾 Buying Power      | `$106,085.13` |
| 🟢 Total P&L | `+$19,765.19` &nbsp; `(+197.65%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$19,765.19` (+197.65%)
- **Yesterday-to-today P&L:** `+$567.04`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 69.00 | $307.50 | $309.45 | $21,352.04 | 🟢 +$134.59 | +0.63% |
| **AMZN** | STOCK | 56.00 | $249.16 | $259.25 | $14,518.00 | 🟢 +$565.28 | +4.05% |
| **AVGO** | STOCK | 18.00 | $385.06 | $368.00 | $6,624.00 | 🔴 $-307.13 | -4.43% |
| **BTC/USD** | CRYPTO | 0.2296 | $17,584.56 | $77,703.90 | $17,840.42 | 🟢 +$13,803.10 | +341.89% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,453.24 | $1,538.77 | 🟢 +$1,538.77 | 0.00% |
| **GOOGL** | STOCK | 31.00 | $351.54 | $344.85 | $10,690.35 | 🔴 $-207.24 | -1.90% |
| **LLY** | STOCK | 41.00 | $1,174.30 | $1,255.50 | $51,475.50 | 🟢 +$3,329.09 | +6.91% |
| **META** | STOCK | 33.00 | $591.43 | $549.99 | $18,149.72 | 🔴 $-1,367.47 | -7.01% |
| **MSFT** | STOCK | 32.00 | $416.49 | $482.69 | $15,446.08 | 🟢 +$2,118.45 | +15.90% |
| **NVDA** | STOCK | 171.00 | $214.77 | $215.05 | $36,773.55 | 🟢 +$47.64 | +0.13% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $92.66 | $1,428.70 | 🟢 +$1,428.70 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $765.39 | $4,592.34 | 🟢 +$119.68 | +2.68% |
| **TSLA** | STOCK | 24.00 | $432.23 | $362.44 | $8,698.56 | 🔴 $-1,675.01 | -16.15% |
| **VTI** | ETF | 27.00 | $369.73 | $378.50 | $10,219.50 | 🟢 +$236.75 | +2.37% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $214.72 | 🔴 -0.98% | **BUY** | 84% |
| 2 | **AAPL** | Apple Inc. | STOCK | $309.35 | 🔴 -0.63% | **BUY** | 79% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $344.82 | 🟢 +1.22% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $483.24 | 🟢 +0.43% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $258.63 | 🔴 -0.57% | **BUY** | 77% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $378.24 | 🟢 +0.44% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $368.45 | 🟢 +1.21% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $77,716.73 | 🟢 +6.44% | **SELL** | 100% |
| 9 | **META** | Meta Platforms Inc. | STOCK | $549.90 | 🟢 +0.75% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,255.40 | 🟢 +0.88% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 74% | Moderate negative momentum (-0.98%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 69% | Moderate negative momentum (-0.63%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+1.22%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.43%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 68% | Moderate negative momentum (-0.57%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.44%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.21%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 78% | Extreme gain today (+6.44%) — mean reversion pullback likely |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.75%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.88%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
