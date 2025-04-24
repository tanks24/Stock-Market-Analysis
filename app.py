import streamlit as st
from data_fetcher import fetch_data
from risk_analyzer import calc_volatility, sharpe_ratio, max_drawdown
from portfolio_simulator import simulate_portfolio
from rebalance import mean_variance_optimizer
from predictor import forecast_prices
import plotly.graph_objects as go
from datetime import date
import pandas as pd

st.set_page_config(layout="wide")
st.title("Intelligent Portfolio Tracker & Risk Analyzer")

tickers = st.multiselect("Enter Stock Tickers", ['AAPL', 'TSLA', 'MSFT', 'AMZN'], default=['AAPL', 'TSLA'])
start = st.date_input("Start Date", value=date(2022,1,1))
end = st.date_input("End Date", value=date.today())

# Portfolio Inputs
portfolio = {}
for ticker in tickers:
    amt = st.number_input(f"Amount invested in {ticker} ($)", min_value=0.0, value=1000.0)
    portfolio[ticker] = amt

data_dict = {ticker: fetch_data(ticker, start, end) for ticker in tickers}

# Plot portfolio
st.header("Portfolio Simulation")
daily_vals = simulate_portfolio(portfolio, data_dict)
st.line_chart(daily_vals)

# Risk Analysis
st.header("Risk Analysis Per Stock")
for ticker in tickers:
    df = data_dict[ticker]
    vol = calc_volatility(df).iloc[-1]  # Get the last value in the Series
    sharpe = sharpe_ratio(df)  # Assuming this is already a scalar value
    drawdown = max_drawdown(df)  # Assuming this is already a scalar value
    
    # Ensure that the values are scalar before formatting them for display
    vol_value = vol.values[0] if isinstance(vol, pd.Series) else vol
    sharpe_value = sharpe.values[0] if isinstance(sharpe, pd.Series) else sharpe
    drawdown_value = drawdown.values[0] if isinstance(drawdown, pd.Series) else drawdown
    
    st.markdown(f"**{ticker}** - Volatility: {vol_value:.2%}, Sharpe Ratio: {sharpe_value:.2f}, Max Drawdown: {drawdown_value:.2%}")


# Optimization
st.header("Suggested Rebalancing")
opt_weights = mean_variance_optimizer(data_dict)
st.write(dict(zip(tickers, opt_weights)))

# Forecasting
st.header("Forecasted Prices")
selected = st.selectbox("Select ticker to forecast", tickers)
forecast = forecast_prices(data_dict[selected].reset_index())
fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))
fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], name='Upper', line=dict(dash='dot')))
fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], name='Lower', line=dict(dash='dot')))
st.plotly_chart(fig)

