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

> 🕐 **Last updated:** 2026-05-13 14:40 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,580.10` |
| 💸 Cash Available    | `$64,245.70` |
| 🧾 Buying Power      | `$12,954.89` |
| 🔴 Total P&L | `$-419.90` &nbsp; `(-4.20%)` |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:----:|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 162.00 | $294.91 | $295.55 | $47,879.10 | 🟢 +$102.89 | +0.22% |
| **AMZN** | STOCK | -56.0000 | $263.79 | $264.87 | $-14,832.44 | 🔴 $-60.30 | +0.41% |
| **META** | STOCK | 50.00 | $599.90 | $603.44 | $30,172.00 | 🟢 +$177.09 | +0.59% |
| **MSFT** | STOCK | -72.0000 | $403.04 | $402.32 | $-28,967.04 | 🟢 +$51.57 | -0.18% |
| **NVDA** | STOCK | 140.00 | $225.45 | $224.46 | $31,423.70 | 🔴 $-139.78 | -0.44% |
| **TSLA** | STOCK | -68.0000 | $438.08 | $446.19 | $-30,340.92 | 🔴 $-551.37 | +1.85% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $295.61 | 🟢 +0.27% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $224.38 | 🟢 +1.63% | **BUY** | 93% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $445.71 | 🟢 +2.83% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $402.33 | 🔴 -1.33% | **SELL** | 87% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $264.95 | 🔴 -0.33% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $603.49 | 🟢 +0.08% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $737.96 | 🔴 -0.03% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $79,773.55 | 🔴 -0.88% | HOLD | — |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,266.15 | 🔴 -0.35% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $91.99 | 🔴 -2.57% | HOLD | — |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
