import yfinance as yf
import pandas as pd

def fetch_historical_data(ticker: str, period: str = "2y") -> pd.DataFrame:
    """
    Fetches historical stock prices using yfinance.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    
    if hist.empty:
        return pd.DataFrame()
        
    # We will use the closing price
    df = hist[['Close']].copy()
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    
    # Ensure Date column is tz-naive or standard format
    if 'Date' in df.columns:
         if pd.api.types.is_datetime64_any_dtype(df['Date']):
             if df['Date'].dt.tz is not None:
                 df['Date'] = df['Date'].dt.tz_localize(None)
    
    return df
