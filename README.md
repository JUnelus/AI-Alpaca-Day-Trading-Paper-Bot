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

> 🕐 **Last updated:** 2026-08-07 21:25 UTC &nbsp;|&nbsp; **Trades today:** 2 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$106,022.34` |
| 💸 Cash Available    | `$-79,724.30` |
| 🧾 Buying Power      | `$133,361.32` |
| 🟢 Total P&L | `+$19,815.54` &nbsp; `(+198.16%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `+$19,815.54` (+198.16%)
- **Yesterday-to-today P&L:** `+$987.19`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **GOOGL** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **LLY** | BUY | 76% | DCA buy: quality asset on a mild dip |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 61.00 | $307.66 | $313.04 | $19,095.44 | 🟢 +$328.24 | +1.75% |
| **AMZN** | STOCK | 39.00 | $243.03 | $274.33 | $10,698.87 | 🟢 +$1,220.76 | +12.88% |
| **AVGO** | STOCK | 10.00 | $380.24 | $425.46 | $4,254.60 | 🟢 +$452.18 | +11.89% |
| **BTC/USD** | CRYPTO | 0.2941 | $21,410.95 | $64,891.97 | $19,087.05 | 🟢 +$12,789.32 | +203.08% |
| **ETH/USD** | STOCK | 0.6272 | $0.00 | $1,915.90 | $1,201.73 | 🟢 +$1,201.73 | 0.00% |
| **GOOGL** | STOCK | 22.00 | $354.12 | $354.60 | $7,801.20 | 🟢 +$10.67 | +0.14% |
| **LLY** | STOCK | 33.00 | $1,160.01 | $1,184.00 | $39,072.00 | 🟢 +$791.51 | +2.07% |
| **META** | STOCK | 26.00 | $597.38 | $592.35 | $15,401.20 | 🔴 $-130.69 | -0.84% |
| **MSFT** | STOCK | 24.00 | $391.93 | $500.00 | $12,000.00 | 🟢 +$2,593.63 | +27.57% |
| **NVDA** | STOCK | 157.00 | $214.30 | $223.37 | $35,069.09 | 🟢 +$1,423.75 | +4.23% |
| **SOL/USD** | STOCK | 15.42 | $0.00 | $73.50 | $1,133.29 | 🟢 +$1,133.29 | 0.00% |
| **SPY** | STOCK | 6.0000 | $745.44 | $772.99 | $4,637.94 | 🟢 +$165.28 | +3.70% |
| **TSLA** | STOCK | 24.00 | $432.23 | $328.76 | $7,890.24 | 🔴 $-2,483.33 | -23.94% |
| **VTI** | ETF | 22.00 | $367.49 | $382.00 | $8,404.00 | 🟢 +$319.21 | +3.95% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $223.96 | 🟢 +2.27% | HOLD | — |
| 2 | **AAPL** | Apple Inc. | STOCK | $313.33 | 🟢 +0.29% | HOLD | — |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $354.30 | 🔴 -0.96% | **BUY** | 84% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $499.99 | 🟢 +0.03% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $274.48 | 🟢 +0.82% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $381.78 | 🟢 +0.71% | HOLD | — |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $427.76 | 🟢 +1.71% | HOLD | — |
| 8 | **META** | Meta Platforms Inc. | STOCK | $592.10 | 🟢 +0.37% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $64,941.00 | 🟢 +1.06% | HOLD | — |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,185.71 | 🔴 -0.52% | **BUY** | 76% |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 48% | Moderate positive momentum (+2.27%) — continuation expected |
| 2 | **AAPL** | Apple Inc. | HOLD | 50% | Flat session today (+0.29%) — no trend to carry forward |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 74% | Moderate negative momentum (-0.96%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | HOLD | 50% | Flat session today (+0.03%) — no trend to carry forward |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.82%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **BUY** | 48% | Moderate positive momentum (+0.71%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 48% | Moderate positive momentum (+1.71%) — continuation expected |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (+0.37%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **BUY** | 48% | Moderate positive momentum (+1.06%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **SELL** | 66% | Moderate negative momentum (-0.52%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
