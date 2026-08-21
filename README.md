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

> 🕐 **Last updated:** 2026-08-21 14:00 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$108,364.47` |
| 💸 Cash Available    | `$-111,072.41` |
| 🧾 Buying Power      | `$100,517.87` |
| 🟢 Total P&L | `+$20,340.69` &nbsp; `(+203.41%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$20,340.69` (+203.41%)
- **Yesterday-to-today P&L:** `+$1,142.55`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 76% | DCA buy: quality asset on a mild dip |
| **BTC/USD** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 68.00 | $307.50 | $307.32 | $20,898.10 | 🔴 $-12.02 | -0.06% |
| **AMZN** | STOCK | 54.00 | $248.79 | $259.10 | $13,991.13 | 🟢 +$556.62 | +4.14% |
| **AVGO** | STOCK | 18.00 | $385.06 | $366.88 | $6,603.84 | 🔴 $-327.29 | -4.72% |
| **BTC/USD** | CRYPTO | 0.2489 | $17,584.56 | $77,244.40 | $19,225.74 | 🟢 +$14,849.03 | +339.27% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $2,401.31 | $1,506.20 | 🟢 +$1,506.20 | 0.00% |
| **GOOGL** | STOCK | 31.00 | $351.54 | $341.88 | $10,598.28 | 🔴 $-299.31 | -2.75% |
| **LLY** | STOCK | 41.00 | $1,174.30 | $1,251.60 | $51,315.60 | 🟢 +$3,169.19 | +6.58% |
| **META** | STOCK | 33.00 | $591.43 | $549.77 | $18,142.41 | 🔴 $-1,374.78 | -7.04% |
| **MSFT** | STOCK | 32.00 | $416.49 | $482.17 | $15,429.28 | 🟢 +$2,101.65 | +15.77% |
| **NVDA** | STOCK | 171.00 | $214.77 | $216.52 | $37,024.92 | 🟢 +$299.01 | +0.81% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $91.08 | $1,404.37 | 🟢 +$1,404.37 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $764.61 | $4,587.66 | 🟢 +$115.00 | +2.57% |
| **TSLA** | STOCK | 24.00 | $432.23 | $354.61 | $8,510.64 | 🔴 $-1,862.93 | -17.96% |
| **VTI** | ETF | 27.00 | $369.73 | $377.73 | $10,198.71 | 🟢 +$215.96 | +2.16% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $216.49 | 🔴 -0.17% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $307.38 | 🔴 -1.26% | **BUY** | 85% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $341.64 | 🟢 +0.29% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $481.90 | 🟢 +0.16% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $258.88 | 🔴 -0.47% | **BUY** | 76% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $377.71 | 🟢 +0.30% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $366.56 | 🟢 +0.69% | HOLD | — |
| 8 | **BTC/USD** | Bitcoin | CRYPTO | $77,240.08 | 🟢 +5.79% | **SELL** | 100% |
| 9 | **META** | Meta Platforms Inc. | STOCK | $550.17 | 🟢 +0.80% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,251.02 | 🟢 +0.53% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.17%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **SELL** | 75% | Moderate negative momentum (-1.26%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (+0.29%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.16%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 66% | Moderate negative momentum (-0.47%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.30%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+0.69%) — continuation expected |
| 8 | **BTC/USD** | Bitcoin | **SELL** | 78% | Extreme gain today (+5.79%) — mean reversion pullback likely |
| 9 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.80%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.53%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
