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

def generate_guideline(df: pd.DataFrame, model: LinearRegression) -> str:
    """
    Analyzes historical data (4 years) and generates a text insight.
    """
    slope = model.coef_[0]
    std_dev = df['Close'].pct_change().std() * np.sqrt(252) # Annualized volatility
    
    yearly_growth = slope * 365 # Approximate yearly growth in pure price
    first_price = df['Close'].iloc[0]
    percent_growth_yearly = (yearly_growth / first_price) * 100

    volatility_assessment = "안정적"
    if std_dev > 0.4:
        volatility_assessment = "매우 불안정(고변동성)"
    elif std_dev > 0.25:
        volatility_assessment = "다소 변동성 있음"
        
    trend_assessment = "견고한 성장"
    if percent_growth_yearly < 0:
         trend_assessment = "하락 추세"
    elif percent_growth_yearly < 5:
         trend_assessment = "저성장 단기 횡보"

    guideline = (
        f"📊 [4년(약 {len(df)}거래일) 데이터 기반 분석 결과]\n"
        f"이 기업은 지난 기간 동안 연간 추세선 기준 약 {percent_growth_yearly:.2f}%의 {trend_assessment}을(를) 보이고 있습니다. "
        f"연간 내재 변동성은 약 {std_dev*100:.1f}% 수준으로 '{volatility_assessment}'인 종목으로 평가됩니다. "
    )
    if slope > 0 and std_dev < 0.3:
        guideline += "포트폴리오의 안정적인 기초 자산으로 편입하기에 적합해 보입니다."
    elif slope > 0 and std_dev >= 0.3:
        guideline += "장기 우상향의 잠재력은 있으나, 단기적인 가격 등락에 유의하여 분할 매수하는 것을 권장합니다."
    elif slope <= 0:
        guideline += "장기적 하락 또는 정체 구간에 있으므로 새로운 성장 동력이나 실적 턴어라운드를 확인한 후 접근하는 것이 좋습니다."
        
    return guideline
