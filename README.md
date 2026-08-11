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

> 🕐 **Last updated:** 2026-08-11 14:11 UTC &nbsp;|&nbsp; **Trades today:** 5 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$106,586.51` |
| 💸 Cash Available    | `$-84,259.28` |
| 🧾 Buying Power      | `$125,913.76` |
| 🟢 Total P&L | `+$20,382.26` &nbsp; `(+203.82%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$20,382.26` (+203.82%)
- **Yesterday-to-today P&L:** `+$4.88`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 79% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 97% | DCA buy: quality asset on a deep pullback |
| **MSFT** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **AMZN** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 81% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 63.00 | $307.66 | $306.55 | $19,312.33 | 🔴 $-70.16 | -0.36% |
| **AMZN** | STOCK | 39.00 | $243.03 | $275.31 | $10,737.28 | 🟢 +$1,259.17 | +13.29% |
| **AVGO** | STOCK | 11.00 | $384.11 | $421.20 | $4,633.26 | 🟢 +$408.04 | +9.66% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $64,123.80 | $19,903.70 | 🟢 +$12,559.84 | +171.02% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,884.46 | $1,182.01 | 🟢 +$1,182.01 | 0.00% |
| **GOOGL** | STOCK | 23.00 | $354.15 | $351.38 | $8,081.74 | 🔴 $-63.62 | -0.78% |
| **LLY** | STOCK | 34.00 | $1,161.41 | $1,219.52 | $41,463.51 | 🟢 +$1,975.65 | +5.00% |
| **META** | STOCK | 26.00 | $597.38 | $608.38 | $15,817.88 | 🟢 +$285.99 | +1.84% |
| **MSFT** | STOCK | 24.00 | $391.93 | $501.76 | $12,042.36 | 🟢 +$2,635.99 | +28.02% |
| **NVDA** | STOCK | 161.00 | $214.48 | $219.91 | $35,404.71 | 🟢 +$873.36 | +2.53% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.16 | $1,174.33 | 🟢 +$1,174.33 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $773.73 | $4,642.35 | 🟢 +$169.69 | +3.79% |
| **TSLA** | STOCK | 24.00 | $432.23 | $335.08 | $8,042.04 | 🔴 $-2,331.53 | -22.48% |
| **VTI** | ETF | 22.00 | $367.49 | $382.19 | $8,408.29 | 🟢 +$323.50 | +4.00% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $219.97 | 🟢 +1.11% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $306.38 | 🔴 -0.61% | **BUY** | 79% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $351.63 | 🔴 -1.65% | **BUY** | 97% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $501.88 | 🔴 -0.83% | **BUY** | 83% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $275.43 | 🔴 -0.96% | **BUY** | 84% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $382.24 | 🟢 +0.16% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $421.30 | 🔴 -0.26% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $609.04 | 🟢 +2.37% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,142.77 | 🟢 +0.35% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,221.55 | 🔴 -0.84% | **BUY** | 81% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+1.11%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **SELL** | 69% | Moderate negative momentum (-0.61%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 85% | Moderate negative momentum (-1.65%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 73% | Moderate negative momentum (-0.83%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 74% | Moderate negative momentum (-0.96%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.16%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (-0.26%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+2.37%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.35%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 71% | Moderate negative momentum (-0.84%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
