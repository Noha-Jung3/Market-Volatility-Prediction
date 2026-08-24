from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title = "Market Volatility Prediction API",
    description= "API for predicting 10-day future market volatility",
    version = "1.0.0"
)

app.include_router(router)
     