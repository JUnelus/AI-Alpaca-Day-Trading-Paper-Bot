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

> 🕐 **Last updated:** 2026-05-20 14:42 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,686.63` |
| 💸 Cash Available    | `$58,034.15` |
| 🧾 Buying Power      | `$147,178.29` |
| 🔴 Total P&L | `$-596.57` &nbsp; `(-5.97%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-596.57` (-5.97%)
- **Yesterday-to-today P&L:** `+$484.09`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 98% | Positive momentum detected |
| **TSLA** | BUY | 86% | Positive momentum detected |
| **MSFT** | SELL | 75% | Negative momentum detected |
| **AMZN** | BUY | 83% | Positive momentum detected |
| **SPY** | BUY | 71% | Positive momentum detected |
| **BTC/USD** | BUY | 73% | Positive momentum detected |
| **ETH/USD** | BUY | 78% | Positive momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 4.0000 | $298.13 | $299.26 | $1,197.06 | 🟢 +$4.52 | +0.38% |
| **BTC/USD** | CRYPTO | 0.0374 | $79,328.23 | $77,213.80 | $2,884.61 | 🔴 $-78.99 | -2.67% |
| **ETH/USD** | CRYPTO | 1.3536 | $2,211.78 | $2,129.27 | $2,882.20 | 🔴 $-111.69 | -3.73% |
| **MSFT** | STOCK | 3.0000 | $414.36 | $414.22 | $1,242.66 | 🔴 $-0.43 | -0.03% |
| **NVDA** | STOCK | 134.00 | $226.82 | $224.66 | $30,104.44 | 🔴 $-289.61 | -0.95% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $85.47 | $1,378.37 | 🔴 $-120.20 | -8.02% |
| **SPY** | ETF | 1.0000 | $737.83 | $737.81 | $737.81 | 🔴 $-0.02 | -0.00% |
| **TSLA** | STOCK | 3.0000 | $409.01 | $408.96 | $1,226.88 | 🔴 $-0.15 | -0.01% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $299.20 | 🟢 +0.08% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $224.84 | 🟢 +1.92% | **BUY** | 98% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $409.36 | 🟢 +1.30% | **BUY** | 86% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $414.22 | 🔴 -0.77% | **SELL** | 75% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $262.26 | 🟢 +1.13% | **BUY** | 83% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $600.54 | 🔴 -0.34% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $737.83 | 🟢 +0.56% | **BUY** | 71% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $77,278.57 | 🟢 +0.67% | **BUY** | 73% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,129.36 | 🟢 +0.90% | **BUY** | 78% |
| 10 | **SOL/USD** | Solana | CRYPTO | $85.39 | 🟢 +1.40% | **BUY** | 88% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.08%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 85% | Moderate positive momentum (+1.92%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 76% | Moderate positive momentum (+1.30%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 66% | Moderate negative momentum (-0.77%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 73% | Moderate positive momentum (+1.13%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.34%) — no trend to carry forward |
| 7 | **SPY** | SPDR S&P 500 ETF | **BUY** | 63% | Moderate positive momentum (+0.56%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 65% | Moderate positive momentum (+0.67%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **BUY** | 69% | Moderate positive momentum (+0.90%) — continuation expected |
| 10 | **SOL/USD** | Solana | **BUY** | 77% | Moderate positive momentum (+1.40%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
