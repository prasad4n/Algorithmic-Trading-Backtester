import argparse
from utils.data_loader import load_csv, load_yahoo
from backtester.engine import Backtester
from strategies.moving_average import MovingAverageStrategy
from strategies.rsi import RSIStrategy
from strategies.bollinger_bands import BollingerBandsStrategy
from visualization.plots import plot_equity_curve
from visualization.trade_visualizer import plot_trades
from reports.report_generator import ReportGenerator

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", type=str, default=None, help="Ticker to download via yfinance")
    p.add_argument("--csv", type=str, default=None, help="Path to CSV file with historical OHLCV data")
    p.add_argument("--start", type=str, default="2020-01-01")
    p.add_argument("--end", type=str, default="2023-01-01")
    p.add_argument("--initial-capital", type=float, default=100000)
    return p.parse_args()

def main():
    args = parse_args()

    if args.csv:
        data = load_csv(args.csv)
    elif args.ticker:
        data = load_yahoo(args.ticker, start=args.start, end=args.end)
    else:
        # sample data
        data = load_csv("data/sample_data.csv")

    # Choose strategy (combine or swap as needed)
    ma = MovingAverageStrategy(short_window=20, long_window=50)
    rsi = RSIStrategy(period=14, overbought=70, oversold=30)
    bb = BollingerBandsStrategy(window=20, n_std=2)

    # can combine signals: simple example - require both MA and RSI signals
    class CombinedStrategy:
        def __init__(self, strategies):
            self.strategies = strategies

        def generate_signals(self, data):
            import pandas as pd
            signals = pd.Series(0, index=data.index)
            for strat in self.strategies:
                signals = signals + strat.generate_signals(data)
            # majority voting: buy when sum > 0, sell when sum < 0
            signals[signals > 0] = 1
            signals[signals < 0] = -1
            return signals

    combined = CombinedStrategy([ma, rsi, bb])

    # Backtester
    bt = Backtester(data, combined, initial_capital=args.initial_capital, commission=0.001, slippage=0.001)
    results = bt.run_backtest()

    bt.print_summary(results)

    # Plots
    plot_equity_curve(results["portfolio"])
    plot_trades(data, results["signals"])  # marks buys/sells

    # Generate PDF report
    metrics = bt.get_metrics(results)
    rg = ReportGenerator(metrics, output_file="reports/backtest_report.pdf")
    rg.generate()

if __name__ == "__main__":
    main()
