def simulate_portfolio(holdings, data_dict):
    daily_vals = None
    for ticker, amt in holdings.items():
        df = data_dict[ticker]
        shares = amt / df['Close'].iloc[0]
        df['Value'] = shares * df['Close']
        daily_vals = df['Value'] if daily_vals is None else daily_vals.add(df['Value'], fill_value=0)
    return daily_vals
