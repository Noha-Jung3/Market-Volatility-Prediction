from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import update_and_predict

app = FastAPI(
    title = "Market Volatility Prediction API",
    description= "API for predicting 10-day future market volatility",
    version = "1.0.0"
)

#creating "contract":

class IngestionResult(BaseModel):
    status: str
    rows_added: int
    latest_date: str

class FeatureResult(BaseModel):
    status: str
    rows_processed: int | None = None
    latest_date: str | None = None
    reason: str | None = None

class PredictionResult(BaseModel):
    date: str 
    prediction: float
#prediction response must contain a date which is a string and prediction which is a number (float)
    
class PredictResponse(BaseModel):
    ingestion: IngestionResult
    features: FeatureResult
    prediction: PredictionResult
# /predict must return an object containing these three sections each with the appropriate structure.

#we explicitly define what the API promises to return
    

@app.get("/")
def home():
    return {
        "message": "Market Volatility Prediction API"
    }


@app.get("/predict")
def predict():
    return update_and_predict()