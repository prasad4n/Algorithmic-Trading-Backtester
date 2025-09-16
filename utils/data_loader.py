import pandas as pd
import yfinance as yf

def load_csv(path: str) -> pd.DataFrame:
    # Try to detect 'Date' header, otherwise assume first column is date
    sample = pd.read_csv(path, nrows=1)
    if 'Date' in sample.columns:
        df = pd.read_csv(path, parse_dates=['Date'])
        df.set_index('Date', inplace=True)
    else:
        df = pd.read_csv(path, parse_dates=[0])
        df.set_index(df.columns[0], inplace=True)
        df.index.name = 'Date'
    df = df.sort_index()
    return df

def load_yahoo(ticker: str, start: str = '2020-01-01', end: str = '2023-01-01') -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end)
    # Normalize column names to: Open, High, Low, Close, Volume
    if 'Adj Close' in df.columns and 'Close' not in df.columns:
        df['Close'] = df['Adj Close']
    return df[['Open','High','Low','Close','Volume']]
