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

> 🕐 **Last updated:** 2026-05-15 21:36 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$100,122.24` |
| 💸 Cash Available    | `$46,520.44` |
| 🧾 Buying Power      | `$139,869.42` |
| 🔴 Total P&L | `$-407.03` &nbsp; `(-4.07%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-407.03` (-4.07%)
- **Yesterday-to-today P&L:** `$-2,094.38`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 74% | Positive momentum detected |
| **NVDA** | SELL | 100% | Negative momentum detected |
| **MSFT** | BUY | 100% | Positive momentum detected |
| **SPY** | SELL | 84% | Negative momentum detected |
| **BTC/USD** | SELL | 100% | Negative momentum detected |
| **ETH/USD** | SELL | 100% | Negative momentum detected |
| **SOL/USD** | SELL | 100% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 5.0000 | $299.77 | $299.78 | $1,498.90 | 🟢 +$0.05 | +0.00% |
| **BTC/USD** | CRYPTO | 0.0180 | $80,844.19 | $79,133.80 | $1,424.98 | 🔴 $-30.80 | -2.12% |
| **ETH/USD** | CRYPTO | 0.6510 | $2,299.70 | $2,221.36 | $1,446.04 | 🔴 $-51.00 | -3.41% |
| **MSFT** | STOCK | 9.0000 | $412.86 | $420.32 | $3,782.88 | 🟢 +$67.14 | +1.81% |
| **NVDA** | STOCK | 176.00 | $226.59 | $224.90 | $39,582.40 | 🔴 $-297.30 | -0.75% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $89.39 | $1,441.60 | 🔴 $-56.97 | -3.80% |
| **SPY** | ETF | 6.0000 | $743.86 | $737.50 | $4,425.00 | 🔴 $-38.15 | -0.85% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $300.23 | 🟢 +0.68% | **BUY** | 74% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $225.32 | 🔴 -4.42% | **SELL** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $422.24 | 🔴 -4.75% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $421.92 | 🟢 +3.05% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $264.14 | 🔴 -1.15% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $614.23 | 🔴 -0.68% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $739.17 | 🔴 -1.20% | **SELL** | 84% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $79,068.80 | 🔴 -2.48% | **SELL** | 100% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,219.65 | 🔴 -2.75% | **SELL** | 100% |
| 10 | **SOL/USD** | Solana | CRYPTO | $89.13 | 🔴 -3.27% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 65% | Moderate positive momentum (+0.68%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 77% | Extreme loss today (-4.42%) — mean reversion pullback likely |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 78% | Extreme loss today (-4.75%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 70% | Extreme gain today (+3.05%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 73% | Moderate negative momentum (-1.15%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 65% | Moderate negative momentum (-0.68%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | **SELL** | 74% | Moderate negative momentum (-1.20%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.48%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **BUY** | 69% | Extreme loss today (-2.75%) — mean reversion pullback likely |
| 10 | **SOL/USD** | Solana | **BUY** | 71% | Extreme loss today (-3.27%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
