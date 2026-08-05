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

> 🕐 **Last updated:** 2026-08-05 14:32 UTC &nbsp;|&nbsp; **Trades today:** 3 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$104,346.01` |
| 💸 Cash Available    | `$-77,646.54` |
| 🧾 Buying Power      | `$135,521.50` |
| 🟢 Total P&L | `+$18,209.80` &nbsp; `(+182.10%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$18,209.80` (+182.10%)
- **Yesterday-to-today P&L:** `+$1,612.02`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AAPL** | BUY | 83% | DCA buy: quality asset on a mild dip |
| **MSFT** | BUY | 77% | DCA buy: quality asset on a mild dip |
| **LLY** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 60.00 | $307.67 | $306.90 | $18,414.00 | 🔴 $-46.27 | -0.25% |
| **AMZN** | STOCK | 38.00 | $242.21 | $276.93 | $10,523.34 | 🟢 +$1,319.18 | +14.33% |
| **AVGO** | STOCK | 10.00 | $379.03 | $421.10 | $4,211.00 | 🟢 +$420.68 | +11.10% |
| **BTC/USD** | CRYPTO | 0.2778 | $18,884.84 | $64,247.06 | $17,846.34 | 🟢 +$12,600.57 | +240.20% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,878.75 | $1,178.43 | 🟢 +$1,178.43 | 0.00% |
| **GOOGL** | STOCK | 18.00 | $352.96 | $381.55 | $6,867.90 | 🟢 +$514.63 | +8.10% |
| **LLY** | STOCK | 35.00 | $1,159.21 | $1,161.45 | $40,650.93 | 🟢 +$78.62 | +0.19% |
| **META** | STOCK | 26.00 | $597.38 | $591.56 | $15,380.56 | 🔴 $-151.33 | -0.97% |
| **MSFT** | STOCK | 22.00 | $382.96 | $490.92 | $10,800.23 | 🟢 +$2,375.08 | +28.19% |
| **NVDA** | STOCK | 157.00 | $214.30 | $219.97 | $34,535.29 | 🟢 +$889.95 | +2.65% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.84 | $1,138.52 | 🟢 +$1,138.52 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $774.60 | $4,647.57 | 🟢 +$174.91 | +3.91% |
| **TSLA** | STOCK | 24.00 | $432.23 | $323.77 | $7,770.48 | 🔴 $-2,603.09 | -25.09% |
| **VTI** | ETF | 21.00 | $366.90 | $382.13 | $8,024.84 | 🟢 +$319.94 | +4.15% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $219.81 | 🟢 +3.71% | HOLD | — |
| 2 | **GOOGL** | Alphabet Inc. | STOCK | $381.02 | 🟢 +0.89% | HOLD | — |
| 3 | **AAPL** | Apple Inc. | STOCK | $306.67 | 🔴 -0.88% | **BUY** | 83% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $490.50 | 🔴 -0.47% | **BUY** | 77% |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $276.82 | 🔴 -0.22% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $382.04 | 🟢 +0.32% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $420.69 | 🟢 +0.61% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $591.49 | 🟢 +0.60% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,260.35 | 🟢 +0.31% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,162.01 | 🟢 +4.15% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **SELL** | 74% | Extreme gain today (+3.71%) — mean reversion pullback likely |
| 2 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.89%) — continuation expected |
| 3 | **AAPL** | Apple Inc. | **SELL** | 73% | Moderate negative momentum (-0.88%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **SELL** | 67% | Moderate negative momentum (-0.47%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (-0.22%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | HOLD | 50% | Flat session today (+0.32%) — no trend to carry forward |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+0.61%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.60%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (+0.31%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 76% | Extreme gain today (+4.15%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
