import matplotlib.pyplot as plt

def plot_equity_curve(portfolio_df):
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_df.index, portfolio_df["total"], label="Equity Curve")
    plt.title("Backtest Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
