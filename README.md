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

> 🕐 **Last updated:** 2026-05-14 21:40 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$102,293.55` |
| 💸 Cash Available    | `$47,717.48` |
| 🧾 Buying Power      | `$139,763.42` |
| 🟢 Total P&L | `+$1,687.35` &nbsp; `(+16.87%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$1,687.35` (+16.87%)
- **Yesterday-to-today P&L:** `+$1,154.98`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | Positive momentum detected |
| **MSFT** | BUY | 81% | Positive momentum detected |
| **SPY** | BUY | 76% | Positive momentum detected |
| **BTC/USD** | BUY | 100% | Positive momentum detected |
| **ETH/USD** | BUY | 96% | Positive momentum detected |
| **SOL/USD** | BUY | 97% | Positive momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **BTC/USD** | CRYPTO | 0.0187 | $80,193.00 | $81,455.77 | $1,519.41 | 🟢 +$23.55 | +1.57% |
| **META** | STOCK | 2.0000 | $620.18 | $617.18 | $1,234.36 | 🔴 $-6.00 | -0.48% |
| **MSFT** | STOCK | 3.0000 | $407.74 | $408.00 | $1,224.00 | 🟢 +$0.78 | +0.06% |
| **NVDA** | STOCK | 176.00 | $226.51 | $235.90 | $41,518.40 | 🟢 +$1,652.62 | +4.15% |
| **SPY** | ETF | 6.0000 | $744.97 | $747.70 | $4,486.20 | 🟢 +$16.40 | +0.37% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $298.21 | 🔴 -0.22% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $235.74 | 🟢 +4.39% | **BUY** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $443.30 | 🔴 -0.44% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $409.43 | 🟢 +1.04% | **BUY** | 81% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $267.22 | 🔴 -1.08% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $618.43 | 🟢 +0.29% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $748.17 | 🟢 +0.79% | **BUY** | 76% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $81,478.62 | 🟢 +2.76% | **BUY** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,298.61 | 🟢 +1.81% | **BUY** | 96% |
| 10 | **SOL/USD** | Solana | CRYPTO | $92.78 | 🟢 +1.83% | **BUY** | 97% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.22%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 77% | Extreme gain today (+4.39%) — mean reversion pullback likely |
| 3 | **TSLA** | Tesla Inc. | **SELL** | 61% | Moderate negative momentum (-0.44%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 71% | Moderate positive momentum (+1.04%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 72% | Moderate negative momentum (-1.08%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.29%) — no trend to carry forward |
| 7 | **SPY** | SPDR S&P 500 ETF | **BUY** | 67% | Moderate positive momentum (+0.79%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 69% | Extreme gain today (+2.76%) — mean reversion pullback likely |
| 9 | **ETH/USD** | Ethereum | **BUY** | 85% | Moderate positive momentum (+1.81%) — continuation expected |
| 10 | **SOL/USD** | Solana | **BUY** | 85% | Moderate positive momentum (+1.83%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
