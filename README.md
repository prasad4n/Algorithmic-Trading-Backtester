# Algorithmic Trading Backtester

A modular Python backtesting engine for testing and evaluating algorithmic trading strategies. This repo demonstrates features and architecture suitable for a developer with ~3 years of experience: multiple strategies, risk hooks, realistic portfolio modeling, visualization and PDF report generation.

## Features

- Multiple strategies (Moving Average, RSI, Bollinger Bands)
- Combined strategies (voting)
- Risk manager hooks (stop-loss/take-profit placeholders)
- Portfolio simulation with commission & slippage
- Performance metrics (Total/Annualized return, Volatility, Sharpe, Sortino, Max Drawdown)
- Trade markers & equity curve plots
- PDF report generation

## Installation

```bash
git clone <your-repo-url>
cd algo-backtester
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## Usage

Run a backtest using the bundled sample data:

```bash
python main.py
```

Run a backtest for a ticker using Yahoo data:

```bash
python main.py --ticker AAPL --start 2020-01-01 --end 2023-01-01
```

## Extending the project (suggested improvements)

- Per-trade tracking (entry price, exited price, P&L per trade)
- Transaction-level logging persisted to CSV/DB
- Unit tests for performance metrics & edge cases
- CI integration (GitHub Actions) and Dockerfile for reproducible env
- Add parameter grid-search and walk-forward optimization
- Add Anomaly detection for data quality
- Add live trading adapter (CCXT / broker SDK) with careful safety checks

