import numpy as np

def calc_volatility(df):
    return df['Close'].pct_change().rolling(20).std()

def max_drawdown(df):
    cummax = df['Close'].cummax()
    drawdown = (df['Close'] - cummax) / cummax
    return drawdown.min()

def sharpe_ratio(df, rf=0.02):
    returns = df['Close'].pct_change().dropna()
    excess_returns = returns - rf/252
    return excess_returns.mean() / excess_returns.std()
