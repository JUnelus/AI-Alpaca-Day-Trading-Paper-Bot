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

> 🕐 **Last updated:** 2026-06-23 21:48 UTC &nbsp;|&nbsp; **Trades today:** 6 &nbsp;|&nbsp; 🧪 Paper trading only — not financial advice

---

### 💰 Account Summary

| Metric | Value |
|:-------|------:|
| 🏦 Starting Balance  | `$10,000.00` |
| 💵 Current Equity    | `$91,955.11` |
| 💸 Cash Available    | `$-15,202.16` |
| 🧾 Buying Power      | `$199,301.40` |
| 🔴 Total P&L | `$-7,073.90` &nbsp; `(-70.74%)` |

### 📝 Daily Trade Summary

- **Startup-to-date Total P&L:** `$-7,073.90` (-70.74%)
- **Yesterday-to-today P&L:** `$-1,648.09`
- **Executed today (with AI reasoning):**

| Symbol | Action | Confidence | AI Reasoning |
|:-------|:------:|-----------:|:-------------|
| **NVDA** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **AAPL** | BUY | 84% | DCA buy: quality asset on a mild dip |
| **GOOGL** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **VTI** | BUY | 85% | DCA buy: quality asset on a mild dip |
| **AVGO** | BUY | 100% | DCA buy: quality asset on a deep pullback |
| **BTC/USD** | BUY | 99% | DCA buy: quality asset on a deep pullback |

### 📈 Open Positions

| Symbol | Type | Qty | Avg Cost | Price | Mkt Value | Unrealized P&L | P&L % |
|:-------|:-----|----:|---------:|------:|----------:|---------------:|------:|
| **AAPL** | STOCK | 54.00 | $308.45 | $294.80 | $15,919.20 | 🔴 $-736.98 | -4.42% |
| **AMZN** | STOCK | 28.00 | $241.88 | $233.97 | $6,551.16 | 🔴 $-221.59 | -3.27% |
| **AVGO** | STOCK | 4.0000 | $387.11 | $382.05 | $1,528.20 | 🔴 $-20.24 | -1.31% |
| **BTC/USD** | CRYPTO | 0.1421 | $65,508.71 | $62,527.47 | $8,886.20 | 🔴 $-423.68 | -4.55% |
| **ETH/USD** | STOCK | 0.6272 | $2,122.30 | $1,664.49 | $1,044.04 | 🔴 $-287.15 | -21.57% |
| **GOOGL** | STOCK | 12.00 | $358.03 | $350.00 | $4,200.00 | 🔴 $-96.33 | -2.24% |
| **LLY** | STOCK | 12.00 | $1,126.41 | $1,106.05 | $13,272.60 | 🔴 $-244.32 | -1.81% |
| **META** | STOCK | 14.00 | $584.75 | $562.56 | $7,875.84 | 🔴 $-310.68 | -3.80% |
| **MSFT** | STOCK | 22.00 | $411.30 | $373.38 | $8,214.30 | 🔴 $-834.39 | -9.22% |
| **NVDA** | STOCK | 110.00 | $222.30 | $200.88 | $22,096.80 | 🔴 $-2,356.60 | -9.64% |
| **SOL/USD** | STOCK | 15.42 | $86.15 | $69.28 | $1,068.21 | 🔴 $-260.17 | -19.59% |
| **SPY** | STOCK | 6.0000 | $745.44 | $734.76 | $4,408.56 | 🔴 $-64.10 | -1.43% |
| **TSLA** | STOCK | 24.00 | $432.23 | $382.39 | $9,177.36 | 🔴 $-1,196.21 | -11.53% |
| **VTI** | ETF | 8.0000 | $367.03 | $364.35 | $2,914.80 | 🔴 $-21.45 | -0.73% |

### 🎯 Watchlist — 10 Symbols

| # | Symbol | Name | Type | Last Price | Day Change | Signal | Confidence |
|--:|:-------|:-----|:----:|-----------:|-----------:|:------:|:----------:|
| 1 | **NVDA** | NVIDIA Corp. | STOCK | $200.04 | 🔴 -4.13% | **BUY** | 100% |
| 2 | **AAPL** | Apple Inc. | STOCK | $294.30 | 🔴 -0.91% | **BUY** | 84% |
| 3 | **GOOGL** | Alphabet Inc. | STOCK | $346.13 | 🔴 -1.02% | **BUY** | 85% |
| 4 | **MSFT** | Microsoft Corp. | STOCK | $373.94 | 🟢 +1.80% | HOLD | — |
| 5 | **AMZN** | Amazon.com Inc. | STOCK | $234.11 | 🟢 +0.57% | HOLD | — |
| 6 | **VTI** | Vanguard Total Stock Market ETF | ETF | $363.70 | 🔴 -1.39% | **BUY** | 85% |
| 7 | **AVGO** | Broadcom Inc. | STOCK | $380.15 | 🔴 -3.06% | **BUY** | 100% |
| 8 | **META** | Meta Platforms Inc. | STOCK | $562.20 | 🔴 -0.29% | HOLD | — |
| 9 | **BTC/USD** | Bitcoin | CRYPTO | $62,573.89 | 🔴 -2.13% | **BUY** | 99% |
| 10 | **LLY** | Eli Lilly and Co. | STOCK | $1,107.08 | 🟢 +0.45% | HOLD | — |

---

### 🔮 Tomorrow's Predictions

> _Momentum-based forecast only — not financial advice. Moderate moves predict continuation; extreme moves (>2.5%) suggest mean reversion._

| # | Symbol | Name | Predicted Action | Confidence | Basis |
|--:|:-------|:-----|:----------------:|-----------:|:------|
| 1 | **NVDA** | NVIDIA Corp. | **BUY** | 76% | Extreme loss today (-4.13%) — mean reversion pullback likely |
| 2 | **AAPL** | Apple Inc. | **SELL** | 74% | Moderate negative momentum (-0.91%) — continuation expected |
| 3 | **GOOGL** | Alphabet Inc. | **SELL** | 75% | Moderate negative momentum (-1.02%) — continuation expected |
| 4 | **MSFT** | Microsoft Corp. | **BUY** | 48% | Moderate positive momentum (+1.80%) — continuation expected |
| 5 | **AMZN** | Amazon.com Inc. | **BUY** | 48% | Moderate positive momentum (+0.57%) — continuation expected |
| 6 | **VTI** | Vanguard Total Stock Market ETF | **SELL** | 75% | Moderate negative momentum (-1.39%) — continuation expected |
| 7 | **AVGO** | Broadcom Inc. | **BUY** | 70% | Extreme loss today (-3.06%) — mean reversion pullback likely |
| 8 | **META** | Meta Platforms Inc. | HOLD | 50% | Flat session today (-0.29%) — no trend to carry forward |
| 9 | **BTC/USD** | Bitcoin | **SELL** | 85% | Moderate negative momentum (-2.13%) — continuation expected |
| 10 | **LLY** | Eli Lilly and Co. | **BUY** | 48% | Moderate positive momentum (+0.45%) — continuation expected |

---

_Dashboard auto-updated by [GitHub Actions](.github/workflows/daily_trade.yml) · Runs Mon–Fri at 9:45 AM ET & 4:15 PM ET_

<!-- PORTFOLIO_DASHBOARD_END -->
