import pandas as pd

class MovingAverageStrategy:
    """Simple moving average crossover strategy.

    Signals:
        1 -> long
       -1 -> short
        0 -> flat
    """
    def __init__(self, short_window: int = 20, long_window: int = 50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short = data["Close"].rolling(window=self.short_window, min_periods=1).mean()
        long = data["Close"].rolling(window=self.long_window, min_periods=1).mean()
        signals = pd.Series(0, index=data.index)
        signals[short > long] = 1
        signals[short < long] = -1
        return signals
