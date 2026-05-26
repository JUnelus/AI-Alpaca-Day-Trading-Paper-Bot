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

> 🕐 **Last updated:** 2026-05-26 14:42 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,689.56` |
| 💸 Cash Available    | `$46,302.64` |
| 🧾 Buying Power      | `$135,509.28` |
| 🔴 Total P&L | `$-851.15` &nbsp; `(-8.51%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-851.15` (-8.51%)
- **Yesterday-to-today P&L:** `+$496.47`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 76% | Positive momentum detected |
| **NVDA** | BUY | 77% | Positive momentum detected |
| **TSLA** | BUY | 79% | Positive momentum detected |
| **AMZN** | SELL | 72% | Negative momentum detected |
| **SPY** | BUY | 77% | Positive momentum detected |
| **BTC/USD** | SELL | 72% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 40.00 | $307.56 | $311.25 | $12,450.20 | 🟢 +$147.96 | +1.20% |
| **AMZN** | STOCK | 5.0000 | $267.55 | $264.44 | $1,322.20 | 🔴 $-15.54 | -1.16% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,527.19 | $76,700.00 | $1,339.32 | 🔴 $-14.44 | -1.07% |
| **ETH/USD** | CRYPTO | 1.3502 | $2,126.13 | $2,109.00 | $2,847.66 | 🔴 $-23.13 | -0.81% |
| **NVDA** | STOCK | 102.00 | $226.65 | $217.15 | $22,149.30 | 🔴 $-969.37 | -4.19% |
| **SOL/USD** | CRYPTO | 33.33 | $86.75 | $84.58 | $2,819.18 | 🔴 $-72.19 | -2.50% |
| **SPY** | ETF | 4.0000 | $737.94 | $752.00 | $3,008.02 | 🟢 +$56.25 | +1.91% |
| **TSLA** | STOCK | 15.00 | $427.56 | $430.19 | $6,452.79 | 🟢 +$39.32 | +0.61% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $311.26 | 🟢 +0.79% | **BUY** | 76% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $217.15 | 🟢 +0.85% | **BUY** | 77% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $430.03 | 🟢 +0.94% | **BUY** | 79% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $417.73 | 🔴 -0.20% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $264.75 | 🔴 -0.59% | **SELL** | 72% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $607.59 | 🔴 -0.44% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $752.00 | 🟢 +0.85% | **BUY** | 77% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $76,774.62 | 🔴 -0.62% | **SELL** | 72% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,110.68 | 🔴 -0.08% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $84.92 | 🔴 -0.11% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 67% | Moderate positive momentum (+0.79%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 68% | Moderate positive momentum (+0.85%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **BUY** | 69% | Moderate positive momentum (+0.94%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (-0.20%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 63% | Moderate negative momentum (-0.59%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 61% | Moderate negative momentum (-0.44%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | **BUY** | 68% | Moderate positive momentum (+0.85%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 64% | Moderate negative momentum (-0.62%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | HOLD | 50% | Flat session today (-0.08%) — no trend to carry forward |
| 10 | **SOL/USD** | Solana | HOLD | 50% | Flat session today (-0.11%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
