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

> 🕐 **Last updated:** 2026-05-14 03:31 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$100,654.75` |
| 💸 Cash Available    | `$62,766.97` |
| 🧾 Buying Power      | `$6,137.32` |
| 🟢 Total P&L | `+$679.25` &nbsp; `(+6.79%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$679.25` (+6.79%)
- **Yesterday-to-today P&L:** `+$146.88`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 88% | Positive momentum detected |
| **NVDA** | BUY | 100% | Positive momentum detected |
| **TSLA** | BUY | 100% | Positive momentum detected |
| **AMZN** | BUY | 92% | Positive momentum detected |
| **META** | BUY | 100% | Positive momentum detected |
| **SPY** | BUY | 71% | Positive momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 162.00 | $294.91 | $298.60 | $48,373.20 | 🟢 +$596.99 | +1.25% |
| **AMZN** | STOCK 📉 SHORT | -56.0000 | $263.79 | $270.09 | $-15,125.04 | 🔴 $-352.90 | +2.39% |
| **META** | STOCK | 50.00 | $599.90 | $613.49 | $30,674.50 | 🟢 +$679.59 | +2.27% |
| **MSFT** | STOCK 📉 SHORT | -75.0000 | $403.01 | $403.75 | $-30,281.25 | 🔴 $-55.74 | +0.18% |
| **NVDA** | STOCK | 146.00 | $225.41 | $227.82 | $33,261.72 | 🟢 +$351.36 | +1.07% |
| **TSLA** | STOCK 📉 SHORT | -65.0000 | $438.08 | $446.39 | $-29,015.35 | 🔴 $-540.04 | +1.90% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $298.87 | 🟢 +1.38% | **BUY** | 88% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $225.83 | 🟢 +2.29% | **BUY** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $445.27 | 🟢 +2.73% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $405.21 | 🔴 -0.63% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $270.13 | 🟢 +1.62% | **BUY** | 92% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $616.63 | 🟢 +2.26% | **BUY** | 100% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $742.31 | 🟢 +0.56% | **BUY** | 71% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $79,280.16 | 🔴 -0.01% | HOLD | — |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,248.30 | 🔴 -0.41% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $90.44 | 🔴 -0.73% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 77% | Moderate positive momentum (+1.38%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 85% | Moderate positive momentum (+2.29%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **SELL** | 69% | Extreme gain today (+2.73%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 64% | Moderate negative momentum (-0.63%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 81% | Moderate positive momentum (+1.62%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **BUY** | 85% | Moderate positive momentum (+2.26%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | **BUY** | 63% | Moderate positive momentum (+0.56%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.01%) — no trend to carry forward |
| 9 | **ETH/USD** | Ethereum | **SELL** | 60% | Moderate negative momentum (-0.41%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 66% | Moderate negative momentum (-0.73%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
