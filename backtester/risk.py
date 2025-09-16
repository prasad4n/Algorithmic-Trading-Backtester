import pandas as pd

class RiskManager:
    def __init__(self, max_drawdown: float = 0.2, stop_loss: float = 0.05, take_profit: float = 0.1):
        # Parameters are fractions (0.2 -> 20%)
        self.max_drawdown = max_drawdown
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def apply_risk_controls(self, data: pd.DataFrame, signals: pd.Series) -> pd.Series:
        """Basic risk controls example: cancels signals if stop-loss / take-profit would have been hit
        This is a placeholder for more sophisticated position-level monitoring.
        """
        adjusted = signals.copy()
        # No changes for now — returns signals unchanged. Keep hooks for extension.
        return adjusted
