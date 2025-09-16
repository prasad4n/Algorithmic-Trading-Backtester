import pandas as pd

class RSIStrategy:
    def __init__(self, period: int = 14, overbought: int = 70, oversold: int = 30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    def _rsi(self, series: pd.Series) -> pd.Series:
        delta = series.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ma_up = up.rolling(self.period, min_periods=1).mean()
        ma_down = down.rolling(self.period, min_periods=1).mean()
        rs = ma_up / (ma_down + 1e-9)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        rsi = self._rsi(data["Close"])
        signals = pd.Series(0, index=data.index)
        signals[rsi > self.overbought] = -1
        signals[rsi < self.oversold] = 1
        return signals
