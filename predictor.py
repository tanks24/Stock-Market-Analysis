from prophet import Prophet
import pandas as pd

def forecast_prices(df):
    model_df = df.reset_index()[['Date', 'Close']]
    model_df.columns = ['ds', 'y']
    model = Prophet()
    model.fit(model_df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
