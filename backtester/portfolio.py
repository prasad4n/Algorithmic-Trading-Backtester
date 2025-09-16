import pandas as pd
import numpy as np

class Portfolio:
    def __init__(self, data: pd.DataFrame, signals: pd.Series, initial_capital: float = 100000.0, commission: float = 0.0, slippage: float = 0.0):
        self.data = data
        self.signals = signals
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage

    def _position_size(self, price: float, risk_fraction: float = 0.01):
        # simple fixed fractional: risk_fraction of capital per trade (very basic)
        qty = int((self.initial_capital * risk_fraction) // price)
        return max(qty, 0)

    def backtest_portfolio(self) -> pd.DataFrame:
        df = pd.DataFrame(index=self.data.index)
        df["Close"] = self.data["Close"]
        df["signal"] = self.signals

        # Build trade list and position
        position = 0
        cash = self.initial_capital
        holdings = []
        totals = []
        qtys = []
        trade_log = []

        for i, (date, row) in enumerate(df.iterrows()):
            signal = row["signal"]
            price = row["Close"]

            # Determine desired position: long=1, short=-1, flat=0
            desired = signal

            if desired == 1 and position <= 0:
                # enter long
                qty = self._position_size(price)
                if qty > 0:
                    cost = qty * price * (1 + self.slippage)
                    commission = qty * price * self.commission
                    cash -= (cost + commission)
                    position += qty
                    trade_log.append({"date": date, "type": "BUY", "qty": qty, "price": price, "cash": cash})

            elif desired == -1 and position >= 0:
                # enter short (for simplicity implement as selling current holdings)
                qty = self._position_size(price)
                if qty > 0:
                    proceeds = qty * price * (1 - self.slippage)
                    commission = qty * price * self.commission
                    cash += (proceeds - commission)
                    position -= qty
                    trade_log.append({"date": date, "type": "SELL", "qty": qty, "price": price, "cash": cash})

            holdings_val = position * price
            total = cash + holdings_val
            holdings.append(holdings_val)
            totals.append(total)
            qtys.append(position)

        df["position"] = qtys
        df["holdings"] = holdings
        # Build a cash series by assuming cash only changes on trades; reconstruct sequence
        cash_series = [self.initial_capital]
        position2 = 0
        cash2 = self.initial_capital
        for i, (date, row) in enumerate(df.iterrows()):
            signal = row["signal"]
            price = row["Close"]
            if signal == 1 and position2 <= 0:
                qty = self._position_size(price)
                if qty > 0:
                    cost = qty * price * (1 + self.slippage)
                    commission = qty * price * self.commission
                    cash2 -= (cost + commission)
                    position2 += qty
            elif signal == -1 and position2 >= 0:
                qty = self._position_size(price)
                if qty > 0:
                    proceeds = qty * price * (1 - self.slippage)
                    commission = qty * price * self.commission
                    cash2 += (proceeds - commission)
                    position2 -= qty
            cash_series.append(cash2)
        # align lengths
        cash_series = cash_series[1:len(df)+1]
        df["cash"] = cash_series
        df["total"] = df["cash"] + df["holdings"]

        # attach trade log as column for final row for convenience
        df["trade_log"] = [trade_log if i == len(df)-1 else None for i in range(len(df))]

        return df
