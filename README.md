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

> 🕐 **Last updated:** 2026-05-14 03:13 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric              |                        Value |
|:--------------------|-----------------------------:|
| 🏦 Starting Balance |                 `$10,000.00` |
| 💵 Current Equity   |                `$100,794.36` |
| 💸 Cash Available   |                 `$62,766.97` |
| 🧾 Buying Power     |                    `$818.07` |
| 🟢 Total P&L        | `+$818.86` &nbsp; `(+8.19%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$818.86` (+8.19%)
- **Yesterday-to-today P&L:** `+$286.49`
- **Executed today (with AI reasoning):**

| Symbol   | Action | Confidence | AI Reasoning               |
|:---------|:------:|-----------:|:---------------------------|
| **AAPL** |  BUY   |        88% | Positive momentum detected |
| **NVDA** |  BUY   |       100% | Positive momentum detected |

### 📈 Open Positions

| Symbol   | Type           |      Qty | Avg Cost |   Price |   Mkt Value | Unrealized P&L |  P&L % |
|:---------|:---------------|---------:|---------:|--------:|------------:|---------------:|-------:|
| **AAPL** | STOCK          |   162.00 |  $294.91 | $298.71 |  $48,391.02 |    🟢 +$614.81 | +1.29% |
| **AMZN** | STOCK 📉 SHORT | -56.0000 |  $263.79 | $270.39 | $-15,141.84 |    🔴 $-369.70 | +2.50% |
| **META** | STOCK          |    50.00 |  $599.90 | $615.55 |  $30,777.50 |    🟢 +$782.59 | +2.61% |
| **MSFT** | STOCK 📉 SHORT | -75.0000 |  $403.01 | $403.90 | $-30,292.50 |     🔴 $-66.99 | +0.22% |
| **NVDA** | STOCK          |   146.00 |  $225.41 | $228.31 |  $33,333.26 |    🟢 +$422.90 | +1.29% |
| **TSLA** | STOCK 📉 SHORT | -65.0000 |  $438.08 | $446.77 | $-29,040.05 |    🔴 $-564.74 | +1.98% |

### 🎯 Watchlist — 10 Symbols

|  # | Symbol      | Name                |  Type  | Last Price | Day Change | Signal  | Confidence |
|---:|:------------|:--------------------|:------:|-----------:|-----------:|:-------:|:----------:|
|  1 | **AAPL**    | Apple Inc.          | STOCK  |    $298.87 |  🟢 +1.38% | **BUY** |    88%     |
|  2 | **NVDA**    | NVIDIA Corp.        | STOCK  |    $225.83 |  🟢 +2.29% | **BUY** |    100%    |
|  3 | **TSLA**    | Tesla Inc.          | STOCK  |    $445.27 |  🟢 +2.73% | **BUY** |    100%    |
|  4 | **MSFT**    | Microsoft Corp.     | STOCK  |    $405.21 |  🔴 -0.63% |  HOLD   |     —      |
|  5 | **AMZN**    | Amazon.com Inc.     | STOCK  |    $270.13 |  🟢 +1.62% | **BUY** |    92%     |
|  6 | **META**    | Meta Platforms Inc. | STOCK  |    $616.63 |  🟢 +2.26% | **BUY** |    100%    |
|  7 | **SPY**     | SPDR S&P 500 ETF    |  ETF   |    $742.31 |  🟢 +0.56% | **BUY** |    71%     |
|  8 | **BTC/USD** | Bitcoin             | CRYPTO | $79,257.30 |  🔴 -0.04% |  HOLD   |     —      |
|  9 | **ETH/USD** | Ethereum            | CRYPTO |  $2,247.82 |  🔴 -0.43% |  HOLD   |     —      |
| 10 | **SOL/USD** | Solana              | CRYPTO |     $90.44 |  🔴 -0.74% |  HOLD   |     —      |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
