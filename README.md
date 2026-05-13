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

> 🕐 **Last updated:** 2026-05-13 21:45 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$100,507.87` |
| 💸 Cash Available    | `$62,766.97` |
| 🧾 Buying Power      | `$7,498.95` |
| 🟢 Total P&L | `+$532.37` &nbsp; `(+5.32%)` |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:----:|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 162.00 | $294.91 | $298.58 | $48,370.07 | 🟢 +$593.86 | +1.24% |
| **AMZN** | STOCK | -56.0000 | $263.79 | $270.07 | $-15,123.92 | 🔴 $-351.78 | +2.38% |
| **META** | STOCK | 50.00 | $599.90 | $615.35 | $30,767.50 | 🟢 +$772.59 | +2.58% |
| **MSFT** | STOCK | -75.0000 | $403.01 | $404.56 | $-30,342.01 | 🔴 $-116.50 | +0.39% |
| **NVDA** | STOCK | 146.00 | $225.41 | $226.58 | $33,081.35 | 🟢 +$170.99 | +0.52% |
| **TSLA** | STOCK | -65.0000 | $438.08 | $446.34 | $-29,012.10 | 🔴 $-536.79 | +1.89% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $298.87 | 🟢 +1.38% | **BUY** | 88% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $225.83 | 🟢 +2.29% | **BUY** | 100% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $445.27 | 🟢 +2.73% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $405.21 | 🔴 -0.63% | **SELL** | 73% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $270.13 | 🟢 +1.62% | **BUY** | 92% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $616.63 | 🟢 +2.26% | **BUY** | 100% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $742.31 | 🟢 +0.56% | **BUY** | 71% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $79,440.68 | 🔴 -1.29% | HOLD | — |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,255.84 | 🔴 -0.81% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $90.99 | 🔴 -3.64% | HOLD | — |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
