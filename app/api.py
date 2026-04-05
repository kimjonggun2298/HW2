from fastapi import APIRouter, HTTPException, Query
from app.data_service import fetch_historical_data
from app.ml_model import train_model, predict_future

router = APIRouter()

@router.get("/predict")
def predict_stock(
    ticker: str = Query(..., description="The stock ticker symbol (e.g., AAPL, NVDA, 005930.KS)"),
    predict_days: int = Query(30, description="Number of days to predict into the future")
):
    try:
        # 1. Fetch data (last 2 years approx 730 days)
        df = fetch_historical_data(ticker, period="2y")
        
        if df.empty or len(df) < 30:
            raise HTTPException(status_code=400, detail="Not enough historical data found for the ticker.")
            
        # 2. Train a lightweight model
        model, last_date, last_price = train_model(df)
        
        # 3. Predict the future
        future_prices = predict_future(model, last_date, predict_days)
        
        return {
            "ticker": ticker,
            "last_closing_date": last_date.strftime("%Y-%m-%d"),
            "last_closing_price": float(last_price),
            "future_prediction": future_prices,
            "model_used": "LinearRegression (Trend Analysis)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
