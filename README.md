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

> 🕐 **Last updated:** 2026-08-17 13:57 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$103,769.30` |
| 💸 Cash Available    | `$-101,165.92` |
| 🧾 Buying Power      | `$99,387.26` |
| 🟢 Total P&L | `+$17,565.09` &nbsp; `(+175.65%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$17,565.09` (+175.65%)
- **Yesterday-to-today P&L:** `$-368.21`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 73% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **META** | BUY | 95% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $305.58 | $20,473.86 | 🔴 $-125.47 | -0.61% |
| **AMZN** | STOCK | 45.00 | $246.48 | $262.19 | $11,798.77 | 🟢 +$707.26 | +6.38% |
| **AVGO** | STOCK | 14.00 | $389.31 | $393.52 | $5,509.35 | 🟢 +$59.07 | +1.08% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $63,536.00 | $19,721.25 | 🟢 +$12,377.39 | +168.54% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,904.45 | $1,194.55 | 🟢 +$1,194.55 | 0.00% |
| **GOOGL** | STOCK | 25.00 | $353.71 | $344.69 | $8,617.25 | 🔴 $-225.39 | -2.55% |
| **LLY** | STOCK | 41.00 | $1,168.10 | $1,179.74 | $48,369.54 | 🟢 +$477.37 | +1.00% |
| **META** | STOCK | 29.00 | $596.19 | $580.46 | $16,833.34 | 🔴 $-456.16 | -2.64% |
| **MSFT** | STOCK | 28.00 | $407.09 | $485.78 | $13,601.84 | 🟢 +$2,203.39 | +19.33% |
| **NVDA** | STOCK | 161.00 | $214.48 | $226.15 | $36,410.13 | 🟢 +$1,878.79 | +5.44% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $75.79 | $1,168.61 | 🟢 +$1,168.61 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $775.46 | $4,652.76 | 🟢 +$180.10 | +4.03% |
| **TSLA** | STOCK | 24.00 | $432.23 | $339.59 | $8,150.26 | 🔴 $-2,223.31 | -21.43% |
| **VTI** | ETF | 22.00 | $367.49 | $383.35 | $8,433.70 | 🟢 +$348.91 | +4.32% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $226.20 | 🟢 +0.46% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $305.70 | 🔴 -0.08% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $344.79 | 🔴 -0.32% | **BUY** | 73% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $485.80 | 🔴 -1.94% | **BUY** | 100% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $262.31 | 🔴 -0.13% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $383.35 | 🔴 -0.13% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $393.90 | 🟢 +0.23% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $580.50 | 🔴 -1.59% | **BUY** | 95% |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,551.83 | 🟢 +1.11% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,180.50 | 🟢 +0.03% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+0.46%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (-0.08%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | HOLD | 50% | Flat session today (-0.32%) — no trend to carry forward |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 85% | Moderate negative momentum (-1.94%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.13%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (-0.13%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | HOLD | 50% | Flat session today (+0.23%) — no trend to carry forward |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 84% | Moderate negative momentum (-1.59%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.11%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | HOLD | 50% | Flat session today (+0.03%) — no trend to carry forward |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
