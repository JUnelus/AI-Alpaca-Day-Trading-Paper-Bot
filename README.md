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

> 🕐 **Last updated:** 2026-08-13 21:29 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$105,995.68` |
| 💸 Cash Available    | `$-95,695.28` |
| 🧾 Buying Power      | `$112,198.33` |
| 🟢 Total P&L | `+$19,791.45` &nbsp; `(+197.91%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$19,791.45` (+197.91%)
- **Yesterday-to-today P&L:** `+$985.22`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **AMZN** | BUY | 81% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 82% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 67.00 | $307.45 | $304.89 | $20,427.95 | 🔴 $-171.38 | -0.83% |
| **AMZN** | STOCK | 43.00 | $245.63 | $265.30 | $11,407.90 | 🟢 +$845.96 | +8.01% |
| **AVGO** | STOCK | 12.00 | $387.61 | $419.22 | $5,030.67 | 🟢 +$379.33 | +8.16% |
| **BTC/USD** | CRYPTO | 0.3104 | $23,659.74 | $63,418.00 | $19,684.63 | 🟢 +$12,340.76 | +168.04% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,885.00 | $1,182.35 | 🟢 +$1,182.35 | 0.00% |
| **GOOGL** | STOCK | 25.00 | $353.71 | $346.43 | $8,660.83 | 🔴 $-181.81 | -2.06% |
| **LLY** | STOCK | 38.00 | $1,166.69 | $1,210.78 | $46,009.46 | 🟢 +$1,675.39 | +3.78% |
| **META** | STOCK | 28.00 | $596.63 | $593.07 | $16,605.96 | 🔴 $-99.55 | -0.60% |
| **MSFT** | STOCK | 28.00 | $407.09 | $496.05 | $13,889.34 | 🟢 +$2,490.89 | +21.85% |
| **NVDA** | STOCK | 161.00 | $214.48 | $225.42 | $36,293.25 | 🟢 +$1,761.90 | +5.10% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $76.32 | $1,176.82 | 🟢 +$1,176.82 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $778.02 | $4,668.12 | 🟢 +$195.46 | +4.37% |
| **TSLA** | STOCK | 24.00 | $432.23 | $341.50 | $8,196.00 | 🔴 $-2,177.57 | -20.99% |
| **VTI** | ETF | 22.00 | $367.49 | $384.44 | $8,457.68 | 🟢 +$372.89 | +4.61% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $225.30 | 🟢 +0.54% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $305.26 | 🟢 +1.00% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $346.36 | 🟢 +0.82% | HOLD | — |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $496.88 | 🟢 +0.90% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $265.13 | 🔴 -0.80% | **BUY** | 81% |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $384.30 | 🟢 +0.65% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $417.82 | 🟢 +0.43% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $594.97 | 🟢 +2.78% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $63,363.53 | 🔴 -0.08% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,209.00 | 🔴 -0.92% | **BUY** | 82% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+0.54%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | **BUY** | 48% | Moderate positive momentum (+1.00%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **BUY** | 48% | Moderate positive momentum (+0.82%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+0.90%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **SELL** | 71% | Moderate negative momentum (-0.80%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.65%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+0.43%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | **SELL** | 69% | Extreme gain today (+2.78%) — mean reversion pullback likely |
| 9 | **BTC/USD** | Bitcoin | HOLD | 50% | Flat session today (-0.08%) — no trend to carry forward |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 72% | Moderate negative momentum (-0.92%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
