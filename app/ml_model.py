import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

def train_model(df: pd.DataFrame):
    """
    Trains a simple Linear Regression model on historical stock prices to capture the trend.
    """
    # Create an ordinal date feature for simple trend regression
    df['date_ordinal'] = pd.to_datetime(df['Date']).apply(lambda date: date.toordinal())
    
    X = df[['date_ordinal']].values
    y = df['Close'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    last_date = df['Date'].iloc[-1]
    last_price = df['Close'].iloc[-1]
    
    return model, last_date, last_price

def predict_future(model: LinearRegression, last_date: pd.Timestamp, days_to_predict: int) -> list:
    """
    Predicts prices for the given number of days into the future.
    """
    future_dates = [last_date + timedelta(days=i) for i in range(1, days_to_predict + 1)]
    future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
    
    predictions = model.predict(future_ordinals)
    
    result = []
    for date, price in zip(future_dates, predictions):
        result.append({
            "date": date.strftime("%Y-%m-%d"),
            "predicted_price": round(float(price), 2)
        })
        
    return result
