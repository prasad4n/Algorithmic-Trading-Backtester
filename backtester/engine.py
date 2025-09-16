import pandas as pd
from .portfolio import Portfolio
from .risk import RiskManager

class Backtester:
    def __init__(self, data: pd.DataFrame, strategy, initial_capital: float = 100000.0, commission: float = 0.0, slippage: float = 0.0):
        self.data = data.copy()
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.risk_manager = RiskManager()

    def run_backtest(self):
        # Generate raw signals
        signals = self.strategy.generate_signals(self.data)

        # Allow risk manager to adjust signals
        signals = self.risk_manager.apply_risk_controls(self.data, signals)

        portfolio = Portfolio(self.data, signals, initial_capital=self.initial_capital, commission=self.commission, slippage=self.slippage)
        portfolio_results = portfolio.backtest_portfolio()

        return {"portfolio": portfolio_results, "signals": signals}

    def print_summary(self, results):
        from .metrics import Metrics
        metrics = Metrics(results["portfolio"]).summary()
        print("===== Performance Summary =====")
        for k, v in metrics.items():
            print(f"{k}: {v}")

    def get_metrics(self, results):
        from .metrics import Metrics
        return Metrics(results["portfolio"]).summary()
