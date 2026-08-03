from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Market Volatility Prediction API"
    }

