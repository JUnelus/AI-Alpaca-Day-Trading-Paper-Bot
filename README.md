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

> 🕐 **Last updated:** 2026-08-05 21:39 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$104,327.76` |
| 💸 Cash Available    | `$-77,283.39` |
| 🧾 Buying Power      | `$134,898.06` |
| 🟢 Total P&L | `+$18,192.88` &nbsp; `(+181.93%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$18,192.88` (+181.93%)
- **Yesterday-to-today P&L:** `+$1,595.10`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 97% | DCA buy: quality asset on a deep pullback |
| **VTI** | BUY | 72% | DCA buy: quality asset on a mild dip |
| **LLY** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 61.00 | $307.66 | $312.04 | $19,034.44 | 🟢 +$267.24 | +1.42% |
| **AMZN** | STOCK | 38.00 | $242.21 | $272.85 | $10,368.30 | 🟢 +$1,164.14 | +12.65% |
| **AVGO** | STOCK | 10.00 | $379.03 | $419.20 | $4,192.00 | 🟢 +$401.68 | +10.60% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $64,610.96 | $17,947.42 | 🟢 +$12,701.65 | +242.13% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,904.95 | $1,194.86 | 🟢 +$1,194.86 | 0.00% |
| **GOOGL** | STOCK | 18.00 | $352.96 | $362.68 | $6,528.24 | 🟢 +$174.97 | +2.75% |
| **LLY** | STOCK | 34.00 | $1,159.21 | $1,171.49 | $39,830.66 | 🟢 +$417.56 | +1.06% |
| **META** | STOCK | 26.00 | $597.38 | $590.50 | $15,353.00 | 🔴 $-178.89 | -1.15% |
| **MSFT** | STOCK | 23.00 | $387.66 | $486.00 | $11,178.00 | 🟢 +$2,261.91 | +25.37% |
| **NVDA** | STOCK | 157.00 | $214.30 | $219.83 | $34,513.31 | 🟢 +$867.97 | +2.58% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $74.18 | $1,143.72 | 🟢 +$1,143.72 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $770.55 | $4,623.30 | 🟢 +$150.64 | +3.37% |
| **TSLA** | STOCK | 24.00 | $432.23 | $321.73 | $7,721.52 | 🔴 $-2,652.05 | -25.57% |
| **VTI** | ETF | 21.00 | $366.90 | $380.11 | $7,982.38 | 🟢 +$277.49 | +3.60% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $219.22 | 🟢 +3.43% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $311.00 | 🟢 +0.52% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $362.43 | 🔴 -4.03% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $487.46 | 🔴 -1.09% | **BUY** | 85% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $272.65 | 🔴 -1.72% | **BUY** | 97% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $379.65 | 🔴 -0.31% | **BUY** | 72% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $418.28 | 🟢 +0.03% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $588.77 | 🟢 +0.14% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,637.51 | 🟢 +0.90% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,169.86 | 🟢 +4.86% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 72% | Extreme gain today (+3.43%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+0.52%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 75% | Extreme loss today (-4.03%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 75% | Moderate negative momentum (-1.09%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-1.72%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.31%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (+0.03%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.14%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.90%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 78% | Extreme gain today (+4.86%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
