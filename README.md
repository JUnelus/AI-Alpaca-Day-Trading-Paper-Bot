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

> The active 10 symbols are refreshed automatically once per ISO week from a larger universe,
> ranked by market value (market cap for stocks/crypto, total assets fallback for ETFs).

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
| Watchlist refresh          | Weekly top-10 by market value             |
| Entry style                | DCA on dips for quality assets            |
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

> 🕐 **Last updated:** 2026-07-15 21:33 UTC &nbsp;|&nbsp; **Trades today:** 1 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$101,698.09` |
| 💸 Cash Available    | `$-55,474.69` |
| 🧾 Buying Power      | `$159,343.12` |
| 🟢 Total P&L | `+$17,617.48` &nbsp; `(+176.17%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$17,617.48` (+176.17%)
- **Yesterday-to-today P&L:** `+$2,067.53`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 53.00 | $305.86 | $327.50 | $17,357.50 | 🟢 +$1,147.13 | +7.08% |
| **AMZN** | STOCK | 40.00 | $239.44 | $255.00 | $10,200.00 | 🟢 +$622.20 | +6.50% |
| **AVGO** | STOCK | 9.0000 | $380.33 | $393.12 | $3,538.10 | 🟢 +$115.09 | +3.36% |
| **BTC/USD** | CRYPTO | 0.2453 | $12,850.06 | $64,884.40 | $15,913.43 | 🟢 +$12,761.85 | +404.93% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,921.79 | $1,205.43 | 🟢 +$1,205.43 | 0.00% |
| **GOOGL** | STOCK | 24.00 | $353.63 | $370.20 | $8,884.80 | 🟢 +$397.71 | +4.69% |
| **LLY** | STOCK | 24.00 | $1,161.99 | $1,155.00 | $27,720.00 | 🔴 $-167.87 | -0.60% |
| **META** | STOCK | 17.00 | $585.08 | $679.58 | $11,552.86 | 🟢 +$1,606.49 | +16.15% |
| **MSFT** | STOCK | 29.00 | $391.00 | $396.15 | $11,488.35 | 🟢 +$149.46 | +1.32% |
| **NVDA** | STOCK | 133.00 | $216.63 | $211.79 | $28,168.07 | 🔴 $-644.21 | -2.24% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $77.20 | $1,190.28 | 🟢 +$1,190.28 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $754.61 | $4,527.66 | 🟢 +$55.00 | +1.23% |
| **TSLA** | STOCK | 24.00 | $432.23 | $394.60 | $9,470.40 | 🔴 $-903.17 | -8.71% |
| **VTI** | ETF | 16.00 | $367.11 | $372.24 | $5,955.90 | 🟢 +$82.09 | +1.40% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $212.50 | 🟢 +0.33% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $327.50 | 🟢 +4.01% | **SELL** | 100% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $370.92 | 🟢 +3.17% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $395.63 | 🟢 +2.78% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $254.96 | 🟢 +3.02% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $372.42 | 🟢 +0.34% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $394.28 | 🟢 +1.33% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $681.31 | 🟢 +3.07% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,822.89 | 🔴 -0.26% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,156.63 | 🟢 +0.35% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (+0.33%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **SELL** | 75% | Extreme gain today (+4.01%) — mean reversion pullback likely |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 71% | Extreme gain today (+3.17%) — mean reversion pullback likely |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 69% | Extreme gain today (+2.78%) — mean reversion pullback likely |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 70% | Extreme gain today (+3.02%) — mean reversion pullback likely |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.34%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.33%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 70% | Extreme gain today (+3.07%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.26%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.35%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
