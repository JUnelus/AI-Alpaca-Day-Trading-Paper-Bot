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

> 🕐 **Last updated:** 2026-05-20 02:52 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,158.48` |
| 💸 Cash Available    | `$53,798.93` |
| 🧾 Buying Power      | `$148,845.84` |
| 🔴 Total P&L | `$-1,215.26` &nbsp; `(-12.15%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,215.26` (-12.15%)
- **Yesterday-to-today P&L:** `$-134.60`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | SELL | 75% | Negative momentum detected |
| **MSFT** | SELL | 89% | Negative momentum detected |
| **SPY** | SELL | 73% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 4.0000 | $298.13 | $298.86 | $1,195.44 | 🟢 +$2.90 | +0.24% |
| **BTC/USD** | CRYPTO | 0.0180 | $81,502.71 | $76,540.75 | $1,378.29 | 🔴 $-89.35 | -6.09% |
| **ETH/USD** | CRYPTO | 0.6510 | $2,299.70 | $2,110.41 | $1,373.81 | 🔴 $-123.22 | -8.23% |
| **MSFT** | STOCK | 12.00 | $414.36 | $416.83 | $5,001.96 | 🟢 +$29.61 | +0.60% |
| **NVDA** | STOCK | 152.00 | $226.72 | $220.96 | $33,585.92 | 🔴 $-875.26 | -2.54% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $84.30 | $1,359.47 | 🔴 $-139.10 | -9.28% |
| **SPY** | ETF | 2.0000 | $742.75 | $732.33 | $1,464.66 | 🔴 $-20.84 | -1.40% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $298.97 | 🟢 +0.38% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $220.61 | 🔴 -0.77% | **SELL** | 75% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $404.11 | 🔴 -1.43% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $417.42 | 🔴 -1.44% | **SELL** | 89% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $259.34 | 🔴 -2.08% | HOLD | — |
| 6 | **META** | Meta Platforms Inc. | STOCK | $602.61 | 🔴 -1.41% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $733.73 | 🔴 -0.67% | **SELL** | 73% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $76,581.68 | 🔴 -0.24% | HOLD | — |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,105.05 | 🔴 -0.25% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $83.89 | 🔴 -0.38% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.38%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 66% | Moderate negative momentum (-0.77%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **SELL** | 78% | Moderate negative momentum (-1.43%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 78% | Moderate negative momentum (-1.44%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 85% | Moderate negative momentum (-2.08%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 78% | Moderate negative momentum (-1.41%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | **SELL** | 65% | Moderate negative momentum (-0.67%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.24%) — no trend to carry forward |
| 9 | **ETH/USD** | Ethereum | HOLD | 50% | Flat session today (-0.25%) — no trend to carry forward |
| 10 | **SOL/USD** | Solana | HOLD | 50% | Flat session today (-0.38%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
