from fastapi import FastAPI
from src.predict import update_and_predict

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Market Volatility Prediction API"
    }


@app.get("/predict")
def predict():
    return update_and_predict()