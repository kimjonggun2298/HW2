# MLOps Financial Prediction API

A lightweight MLOps API server using FastAPI that fetches the last 2 years of stock data via `yfinance` and trains a simple `LinearRegression` model dynamically to predict short-term future trends.

## Setup Instructions

1. **Install Requirements:**
   Make sure you are in a virtual environment, then install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API Server:**
   Start the FastAPI development server using `uvicorn`:
   ```bash
   cd app
   python -m uvicorn main:app --reload
   ```
   Or from the root directory:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

3. **Access the API:**
   - Swagger UI Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
   - You can test the endpoints interactively from the documentation page. Example inputs include `AAPL` (Apple), `005930.KS` (Samsung Electronics), etc.
