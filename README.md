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

> 🕐 **Last updated:** 2026-05-29 21:52 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$98,059.75` |
| 💸 Cash Available    | `$36,349.15` |
| 🧾 Buying Power      | `$129,261.27` |
| 🔴 Total P&L | `$-1,146.15` &nbsp; `(-11.46%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-1,146.15` (-11.46%)
- **Yesterday-to-today P&L:** `$-362.34`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | SELL | 89% | Negative momentum detected |
| **TSLA** | SELL | 89% | Negative momentum detected |
| **MSFT** | BUY | 100% | Positive momentum detected |
| **AMZN** | SELL | 85% | Negative momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 52.00 | $308.65 | $311.25 | $16,185.00 | 🟢 +$135.28 | +0.84% |
| **AMZN** | STOCK | 5.0000 | $271.92 | $270.55 | $1,352.75 | 🔴 $-6.86 | -0.50% |
| **BTC/USD** | CRYPTO | 0.0175 | $77,505.88 | $73,370.41 | $1,281.18 | 🔴 $-72.21 | -5.34% |
| **ETH/USD** | CRYPTO | 0.6272 | $2,122.30 | $2,008.34 | $1,259.71 | 🔴 $-71.48 | -5.37% |
| **MSFT** | STOCK | 9.0000 | $435.56 | $449.36 | $4,044.21 | 🟢 +$124.17 | +3.17% |
| **NVDA** | STOCK | 97.00 | $225.99 | $212.50 | $20,612.34 | 🔴 $-1,309.10 | -5.97% |
| **SOL/USD** | CRYPTO | 15.42 | $86.15 | $81.63 | $1,258.62 | 🔴 $-69.76 | -5.25% |
| **SPY** | ETF | 7.0000 | $744.36 | $755.44 | $5,288.08 | 🟢 +$77.58 | +1.49% |
| **TSLA** | STOCK | 24.00 | $432.60 | $434.53 | $10,428.72 | 🟢 +$46.23 | +0.45% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $312.06 | 🔴 -0.14% | HOLD | — |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $211.14 | 🔴 -1.45% | **SELL** | 89% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $435.79 | 🔴 -1.43% | **SELL** | 89% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $450.24 | 🟢 +5.45% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $270.64 | 🔴 -1.23% | **SELL** | 85% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $632.51 | 🔴 -0.44% | HOLD | — |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $756.48 | 🟢 +0.25% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $73,357.75 | 🔴 -0.21% | HOLD | — |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,008.15 | 🟢 +0.06% | HOLD | — |
| 10 | **SOL/USD** | Solana | CRYPTO | $81.81 | 🔴 -0.27% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.14%) — no trend to carry forward |
| 2 | **NVDA** | NVIDIA Corp. | **SELL** | 78% | Moderate negative momentum (-1.45%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **SELL** | 78% | Moderate negative momentum (-1.43%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 78% | Extreme gain today (+5.45%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 74% | Moderate negative momentum (-1.23%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **SELL** | 61% | Moderate negative momentum (-0.44%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | HOLD | 50% | Flat session today (+0.25%) — no trend to carry forward |
| 8 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.21%) — no trend to carry forward |
| 9 | **ETH/USD** | Ethereum | HOLD | 50% | Flat session today (+0.06%) — no trend to carry forward |
| 10 | **SOL/USD** | Solana | HOLD | 50% | Flat session today (-0.27%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
