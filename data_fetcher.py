import yfinance as yf

def fetch_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df
