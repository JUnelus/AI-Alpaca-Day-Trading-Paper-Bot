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

> 🕐 **Last updated:** 2026-08-10 14:11 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$106,768.00` |
| 💸 Cash Available    | `$-81,809.83` |
| 🧾 Buying Power      | `$132,411.92` |
| 🟢 Total P&L | `+$20,563.30` &nbsp; `(+205.63%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$20,563.30` (+205.63%)
- **Yesterday-to-today P&L:** `+$747.76`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **AAPL** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 73% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 61.00 | $307.66 | $306.42 | $18,691.31 | 🔴 $-75.89 | -0.40% |
| **AMZN** | STOCK | 39.00 | $243.03 | $275.94 | $10,761.66 | 🟢 +$1,283.55 | +13.54% |
| **AVGO** | STOCK | 10.00 | $380.24 | $430.69 | $4,306.95 | 🟢 +$504.53 | +13.27% |
| **BTC/USD** | CRYPTO | 0.3022 | $22,565.81 | $64,573.14 | $19,515.00 | 🟢 +$12,695.26 | +186.15% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,896.81 | $1,189.76 | 🟢 +$1,189.76 | 0.00% |
| **GOOGL** | STOCK | 23.00 | $354.15 | $354.64 | $8,156.72 | 🟢 +$11.36 | +0.14% |
| **LLY** | STOCK | 34.00 | $1,161.41 | $1,212.69 | $41,231.35 | 🟢 +$1,743.49 | +4.42% |
| **META** | STOCK | 26.00 | $597.38 | $598.01 | $15,548.39 | 🟢 +$16.50 | +0.11% |
| **MSFT** | STOCK | 24.00 | $391.93 | $508.66 | $12,207.84 | 🟢 +$2,801.47 | +29.78% |
| **NVDA** | STOCK | 157.00 | $214.30 | $221.76 | $34,817.11 | 🟢 +$1,171.76 | +3.48% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.61 | $1,181.20 | 🟢 +$1,181.20 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $773.95 | $4,643.70 | 🟢 +$171.04 | +3.82% |
| **TSLA** | STOCK | 24.00 | $432.23 | $330.00 | $7,920.00 | 🔴 $-2,453.57 | -23.65% |
| **VTI** | ETF | 22.00 | $367.49 | $382.17 | $8,407.63 | 🟢 +$322.84 | +3.99% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $221.98 | 🔴 -0.89% | **BUY** | 83% |
| 2 | **AAPL** | Apple Inc. | STOCK | $306.29 | 🔴 -2.25% | **BUY** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $354.85 | 🟢 +0.15% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $508.33 | 🟢 +1.67% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $275.77 | 🟢 +0.47% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $382.29 | 🟢 +0.13% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $432.31 | 🟢 +1.06% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $598.49 | 🟢 +1.08% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,570.54 | 🔴 -0.45% | **BUY** | 73% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,212.77 | 🟢 +2.28% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 73% | Moderate negative momentum (-0.89%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 85% | Moderate negative momentum (-2.25%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.15%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.67%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.47%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.13%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.06%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+1.08%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 64% | Moderate negative momentum (-0.45%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+2.28%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
