import pandas as pd

class BollingerBandsStrategy:
    def __init__(self, window: int = 20, n_std: float = 2.0):
        self.window = window
        self.n_std = n_std

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        rolling_mean = data["Close"].rolling(self.window, min_periods=1).mean()
        rolling_std = data["Close"].rolling(self.window, min_periods=1).std().fillna(0)
        upper_band = rolling_mean + (rolling_std * self.n_std)
        lower_band = rolling_mean - (rolling_std * self.n_std)

        signals = pd.Series(0, index=data.index)
        # Mean reversion: buy when price crosses below lower band; sell when above upper band
        signals[data["Close"] < lower_band] = 1
        signals[data["Close"] > upper_band] = -1
        return signals
