import numpy as np
import pandas as pd

class Metrics:
    def __init__(self, portfolio: pd.DataFrame):
        self.portfolio = portfolio
        if "total" not in self.portfolio.columns:
            raise ValueError("Portfolio must contain 'total' column for metrics calculation")
        self.returns = self.portfolio["total"].pct_change().dropna()

    def total_return(self):
        start = self.portfolio["total"].iloc[0]
        end = self.portfolio["total"].iloc[-1]
        return (end / start - 1) * 100

    def annualized_return(self):
        compounded = (1 + self.returns).prod()
        periods = len(self.returns)
        if periods == 0:
            return 0.0
        annual = compounded ** (252.0 / periods) - 1
        return annual * 100

    def annualized_volatility(self):
        return self.returns.std() * (252 ** 0.5) * 100

    def sharpe_ratio(self, risk_free_rate: float = 0.0):
        rf = risk_free_rate / 252
        excess = self.returns - rf
        if self.returns.std() == 0:
            return 0.0
        return (excess.mean() / self.returns.std()) * (252 ** 0.5)

    def sortino_ratio(self, target: float = 0.0):
        downside = self.returns[self.returns < target]
        if len(downside) == 0:
            return float('inf')
        expected_return = self.returns.mean()
        downside_std = downside.std()
        return (expected_return - target) / (downside_std + 1e-9) * (252 ** 0.5)

    def max_drawdown(self):
        cum = self.portfolio["total"].cummax()
        dd = (self.portfolio["total"] - cum) / cum
        return dd.min() * 100

    def summary(self):
        return {
            "Total Return (%)": round(self.total_return(), 2),
            "Annualized Return (%)": round(self.annualized_return(), 2),
            "Annualized Volatility (%)": round(self.annualized_volatility(), 2),
            "Sharpe Ratio": round(self.sharpe_ratio(), 3),
            "Sortino Ratio": round(self.sortino_ratio(), 3) if np.isfinite(self.sortino_ratio()) else None,
            "Max Drawdown (%)": round(self.max_drawdown(), 2)
        }
