from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import router as api_router
from pathlib import Path
import os

app = FastAPI(
    title="MLOps Financial Prediction API",
    description="A simple MLOps API to predict future stock prices based on 2-year historical data using Linear Regression.",
    version="1.0.0"
)

app.include_router(api_router)

# Mount /static directory for frontend assets
static_dir = Path(__file__).parent / "static"
if not static_dir.exists():
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    index_file = static_dir / "index.html"
    if not index_file.exists():
        return {"message": "Welcome to the MLOps API. Frontend is building..."}
    return FileResponse(index_file)
