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

> 🕐 **Last updated:** 2026-08-19 13:59 UTC &nbsp;|&nbsp; **Trades today:** 4 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$106,353.76` |
| 💸 Cash Available    | `$-109,726.91` |
| 🧾 Buying Power      | `$95,281.57` |
| 🟢 Total P&L | `+$20,152.62` &nbsp; `(+201.53%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$20,152.62` (+201.53%)
- **Yesterday-to-today P&L:** `+$2,910.54`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 74% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 78% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **LLY** | SELL | 100% | Take-profit trim after overextended rally |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $316.18 | $21,183.72 | 🟢 +$584.39 | +2.84% |
| **AMZN** | STOCK | 51.00 | $248.09 | $260.28 | $13,274.28 | 🟢 +$621.68 | +4.91% |
| **AVGO** | STOCK | 16.00 | $387.70 | $361.91 | $5,790.56 | 🔴 $-412.58 | -6.65% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $64,925.26 | $20,152.47 | 🟢 +$12,808.61 | +174.41% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,930.28 | $1,210.75 | 🟢 +$1,210.75 | 0.00% |
| **GOOGL** | STOCK | 28.00 | $352.53 | $342.38 | $9,586.64 | 🔴 $-284.14 | -2.88% |
| **LLY** | STOCK | 41.00 | $1,168.10 | $1,290.20 | $52,898.20 | 🟢 +$5,006.02 | +10.45% |
| **META** | STOCK | 33.00 | $591.43 | $545.48 | $18,000.84 | 🔴 $-1,516.35 | -7.77% |
| **MSFT** | STOCK | 30.00 | $412.13 | $482.28 | $14,468.40 | 🟢 +$2,104.62 | +17.02% |
| **NVDA** | STOCK | 165.00 | $214.64 | $218.56 | $36,061.57 | 🟢 +$645.51 | +1.82% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $78.51 | $1,210.53 | 🟢 +$1,210.53 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $770.08 | $4,620.50 | 🟢 +$147.84 | +3.31% |
| **TSLA** | STOCK | 24.00 | $432.23 | $338.00 | $8,111.88 | 🔴 $-2,261.69 | -21.80% |
| **VTI** | ETF | 25.00 | $369.04 | $380.54 | $9,513.38 | 🟢 +$287.44 | +3.12% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $218.88 | 🔴 -0.39% | **BUY** | 74% |
| 2 | **AAPL** | Apple Inc. | STOCK | $316.09 | 🟢 +1.95% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $342.08 | 🔴 -0.62% | **BUY** | 78% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $482.17 | 🟢 +0.11% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $260.20 | 🟢 +0.29% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $380.61 | 🟢 +0.41% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $362.25 | 🔴 -4.67% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $546.23 | 🟢 +0.47% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $65,000.41 | 🟢 +0.49% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,289.26 | 🟢 +5.18% | **SELL** | 100% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | HOLD | 50% | Flat session today (-0.39%) — no trend to carry forward |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.95%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 69% | Moderate negative momentum (-0.62%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.11%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | HOLD | 50% | Flat session today (+0.29%) — no trend to carry forward |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.41%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 78% | Extreme loss today (-4.67%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | **BUY** | 48% | Moderate positive momentum (+0.47%) — continuation expected |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+0.49%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 78% | Extreme gain today (+5.18%) — mean reversion pullback likely |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
