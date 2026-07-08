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

> 🕐 **Last updated:** 2026-07-08 21:38 UTC &nbsp;|&nbsp; **Trades today:** 8 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$97,183.75` |
| 💸 Cash Available    | `$-39,066.96` |
| 🧾 Buying Power      | `$168,159.16` |
| 🟢 Total P&L | `+$13,601.78` &nbsp; `(+136.02%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$13,601.78` (+136.02%)
- **Yesterday-to-today P&L:** `$-206.67`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **AVGO** | SELL | 100% | Take-profit trim after overextended rally |
| **META** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 97% | DCA buy: quality asset on a deep pullback |
| **LLY** | BUY | 94% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 50.00 | $305.42 | $313.41 | $15,670.50 | 🟢 +$399.59 | +2.62% |
| **AMZN** | STOCK | 30.00 | $238.04 | $242.85 | $7,285.50 | 🟢 +$144.28 | +2.02% |
| **AVGO** | STOCK | 9.0000 | $374.95 | $388.23 | $3,494.07 | 🟢 +$119.50 | +3.54% |
| **BTC/USD** | CRYPTO | 0.2199 | $7,163.01 | $62,088.30 | $13,654.56 | 🟢 +$12,079.26 | +766.79% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,733.60 | $1,087.38 | 🟢 +$1,087.38 | 0.00% |
| **GOOGL** | STOCK | 17.00 | $353.08 | $360.99 | $6,136.77 | 🟢 +$134.46 | +2.24% |
| **LLY** | STOCK | 17.00 | $1,156.58 | $1,216.85 | $20,686.45 | 🟢 +$1,024.60 | +5.21% |
| **META** | STOCK | 19.00 | $573.76 | $603.05 | $11,457.91 | 🟢 +$556.39 | +5.10% |
| **MSFT** | STOCK | 25.00 | $392.79 | $383.20 | $9,580.00 | 🔴 $-239.87 | -2.44% |
| **NVDA** | STOCK | 132.00 | $217.83 | $202.93 | $26,786.76 | 🔴 $-1,967.34 | -6.84% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.85 | $1,184.96 | 🟢 +$1,184.96 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $744.30 | $4,465.80 | 🔴 $-6.86 | -0.15% |
| **TSLA** | STOCK | 24.00 | $432.23 | $393.40 | $9,441.60 | 🔴 $-931.97 | -8.98% |
| **VTI** | ETF | 13.00 | $366.36 | $367.70 | $4,780.04 | 🟢 +$17.38 | +0.37% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $204.12 | 🟢 +3.65% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $313.39 | 🟢 +0.88% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $361.92 | 🔴 -1.39% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $383.34 | 🔴 -1.41% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $243.62 | 🔴 -0.96% | **BUY** | 84% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $368.25 | 🔴 -0.37% | **BUY** | 73% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $388.69 | 🟢 +4.83% | **SELL** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $603.12 | 🔴 -2.02% | **BUY** | 100% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,074.83 | 🔴 -1.98% | **BUY** | 97% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,215.83 | 🔴 -1.60% | **BUY** | 94% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 73% | Extreme gain today (+3.65%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.88%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.39%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.41%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 74% | Moderate negative momentum (-0.96%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.37%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **SELL** | 78% | Extreme gain today (+4.83%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 85% | Moderate negative momentum (-2.02%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-1.98%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 83% | Moderate negative momentum (-1.60%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
