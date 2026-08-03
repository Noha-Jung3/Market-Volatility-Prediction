from fastapi import FastAPI
from src.predict import predict_latest


app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Market Volatility Prediction API"
    }


@app.get("/predict")
def predict():
    return predict_latest()
