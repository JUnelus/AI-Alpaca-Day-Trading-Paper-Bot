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

> 🕐 **Last updated:** 2026-05-20 21:53 UTC &nbsp;|&nbsp; **Trades today:** 7 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$99,353.04` |
| 💸 Cash Available    | `$54,374.76` |
| 🧾 Buying Power      | `$137,209.89` |
| 🔴 Total P&L | `$-927.37` &nbsp; `(-9.27%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-927.37` (-9.27%)
- **Yesterday-to-today P&L:** `+$153.29`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 82% | Positive momentum detected |
| **NVDA** | BUY | 86% | Positive momentum detected |
| **TSLA** | BUY | 100% | Positive momentum detected |
| **MSFT** | BUY | 77% | Positive momentum detected |
| **AMZN** | BUY | 100% | Positive momentum detected |
| **SPY** | BUY | 80% | Positive momentum detected |
| **BTC/USD** | BUY | 79% | Positive momentum detected |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 4.0000 | $298.13 | $301.51 | $1,206.04 | 🟢 +$13.50 | +1.13% |
| **AMZN** | STOCK | 5.0000 | $262.29 | $265.08 | $1,325.40 | 🟢 +$13.97 | +1.07% |
| **BTC/USD** | CRYPTO | 0.0567 | $78,721.64 | $77,550.40 | $4,397.90 | 🔴 $-66.42 | -1.49% |
| **ETH/USD** | CRYPTO | 1.3536 | $2,211.78 | $2,131.30 | $2,884.94 | 🔴 $-108.94 | -3.64% |
| **NVDA** | STOCK | 140.00 | $226.73 | $221.78 | $31,049.20 | 🔴 $-692.99 | -2.18% |
| **SOL/USD** | CRYPTO | 16.13 | $92.93 | $85.98 | $1,386.56 | 🔴 $-112.01 | -7.47% |
| **SPY** | ETF | 2.0000 | $737.84 | $739.95 | $1,479.90 | 🟢 +$4.22 | +0.29% |
| **TSLA** | STOCK | 3.0000 | $409.01 | $416.11 | $1,248.33 | 🟢 +$21.30 | +1.74% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **AAPL** | Apple Inc. | STOCK | $302.25 | 🟢 +1.10% | **BUY** | 82% |
| 2 | **NVDA** | NVIDIA Corp. | STOCK | $223.47 | 🟢 +1.30% | **BUY** | 86% |
| 3 | **TSLA** | Tesla Inc. | STOCK | $417.26 | 🟢 +3.25% | **BUY** | 100% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $421.06 | 🟢 +0.87% | **BUY** | 77% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $265.01 | 🟢 +2.19% | **BUY** | 100% |
| 6 | **META** | Meta Platforms Inc. | STOCK | $605.06 | 🟢 +0.41% | **BUY** | 68% |
| 7 | **SPY** | SPDR S&P 500 ETF | ETF | $741.25 | 🟢 +1.02% | **BUY** | 80% |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $77,491.45 | 🟢 +0.95% | **BUY** | 79% |
| 9 | **ETH/USD** | Ethereum | CRYPTO | $2,129.41 | 🟢 +0.91% | **BUY** | 78% |
| 10 | **SOL/USD** | Solana | CRYPTO | $86.03 | 🟢 +2.16% | **BUY** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **AAPL** | Apple Inc. | **BUY** | 72% | Moderate positive momentum (+1.10%) — continuation expected |
| 2 | **NVDA** | NVIDIA Corp. | **BUY** | 76% | Moderate positive momentum (+1.30%) — continuation expected |
| 3 | **TSLA** | Tesla Inc. | **SELL** | 71% | Extreme gain today (+3.25%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 68% | Moderate positive momentum (+0.87%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 85% | Moderate positive momentum (+2.19%) — continuation expected |
| 6 | **META** | Meta Platforms Inc. | **BUY** | 60% | Moderate positive momentum (+0.41%) — continuation expected |
| 7 | **SPY** | SPDR S&P 500 ETF | **BUY** | 71% | Moderate positive momentum (+1.02%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **BUY** | 70% | Moderate positive momentum (+0.95%) — continuation expected |
| 9 | **ETH/USD** | Ethereum | **BUY** | 69% | Moderate positive momentum (+0.91%) — continuation expected |
| 10 | **SOL/USD** | Solana | **BUY** | 85% | Moderate positive momentum (+2.16%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
