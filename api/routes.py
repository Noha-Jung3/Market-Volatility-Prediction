from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.predict import update_and_predict


router = APIRouter()


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
# /predict must return an object containing these three sections each with the routerropriate structure.

#we explicitly define what the API promises to return
    

@router.get("/")
def home():
    return {
        "message": "Market Volatility Prediction API"
    }
# health endpoint so we know if something has gone wrong if it stops responding
@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "market-volatility-api"
    }


@router.get("/predict")
def predict():
    #error handling 
    try:
        return update_and_predict()
    #"try executing the prediction pipeline. function should run as normal if everything is in order"   
    except Exception as e:
    #Catch error if something goes wrong
        raise HTTPException(status_code=500, detail=f"Prediction pipline failed: {str(e)}")
        #tells FastAPI "return an HTTP 500 response and tell client what went wrong"


#why do this? We're introducing separation of concerns.