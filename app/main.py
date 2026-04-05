from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="MLOps Financial Prediction API",
    description="A simple MLOps API to predict future stock prices based on 2-year historical data using Linear Regression.",
    version="1.0.0"
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MLOps Financial Prediction API. Visit /docs to test the API."}
