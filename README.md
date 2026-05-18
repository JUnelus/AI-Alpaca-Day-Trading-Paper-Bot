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

> 🕐 **Last updated:** 2026-05-18 14:46 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,360.56` |
| 💸 Cash Available    | `$46,918.28` |
| 🧾 Buying Power      | `$140,843.67` |
| 🔴 Total P&L | `$-1,185.55` &nbsp; `(-11.86%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,185.55` (-11.86%)
- **Yesterday-to-today P&L:** `$-778.53`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | SELL | 76% | Negative momentum detected |
| **NVDA** | SELL | 95% | Negative momentum detected |
| **AMZN** | BUY | 89% | Positive momentum detected |
| **BTC/USD** | SELL | 87% | Negative momentum detected |
| **ETH/USD** | SELL | 81% | Negative momentum detected |
| **SOL/USD** | SELL | 89% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 9.0000 | $299.04 | $297.80 | $2,680.20 | 🔴 $-11.19 | -0.42% |
| **BTC/USD** | CRYPTO | 0.0180 | $81,502.71 | $76,290.10 | $1,373.77 | 🔴 $-93.86 | -6.40% |
| **ETH/USD** | CRYPTO | 0.6510 | $2,299.70 | $2,106.55 | $1,371.30 | 🔴 $-125.73 | -8.40% |
| **MSFT** | STOCK | 12.00 | $414.36 | $421.05 | $5,052.60 | 🟢 +$80.25 | +1.61% |
| **NVDA** | STOCK | 170.00 | $226.63 | $221.54 | $37,661.80 | 🔴 $-865.18 | -2.25% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $83.79 | $1,351.30 | 🔴 $-147.28 | -9.83% |
| **SPY** | ETF | 4.0000 | $743.49 | $737.85 | $2,951.40 | 🔴 $-22.55 | -0.76% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $297.82 | 🔴 -0.80% | **SELL** | 76% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $221.42 | 🔴 -1.73% | **SELL** | 95% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $411.13 | 🔴 -2.63% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $421.93 | 🟢 +0.00% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $267.96 | 🟢 +1.45% | **BUY** | 89% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $609.71 | 🔴 -0.74% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $737.67 | 🔴 -0.20% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $76,356.34 | 🔴 -1.35% | **SELL** | 87% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,108.40 | 🔴 -1.03% | **SELL** | 81% |
| 10 | **SOL/USD** | Solana | CRYPTO | $83.91 | 🔴 -1.45% | **SELL** | 89% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **SELL** | 67% | Moderate negative momentum (-0.80%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 83% | Moderate negative momentum (-1.73%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 68% | Extreme loss today (-2.63%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.00%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 78% | Moderate positive momentum (+1.45%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 66% | Moderate negative momentum (-0.74%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (-0.20%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 77% | Moderate negative momentum (-1.35%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **SELL** | 71% | Moderate negative momentum (-1.03%) — continuation expected |
| 10 | **SOL/USD** | Solana | **SELL** | 78% | Moderate negative momentum (-1.45%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
