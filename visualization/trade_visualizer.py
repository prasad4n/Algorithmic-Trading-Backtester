import matplotlib.pyplot as plt

def plot_trades(price_data, signals):
    """Plots price and overlays buy/sell markers using signals series (1 buy, -1 sell)."""
    plt.figure(figsize=(12, 6))
    plt.plot(price_data.index, price_data["Close"], label="Close Price")

    buys = signals[signals == 1].index
    sells = signals[signals == -1].index

    if len(buys) > 0:
        plt.scatter(buys, price_data.loc[buys, "Close"], marker="^", s=80, label="Buy")
    if len(sells) > 0:
        plt.scatter(sells, price_data.loc[sells, "Close"], marker="v", s=80, label="Sell")

    plt.title("Price with Trade Markers")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
