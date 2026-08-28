from fastapi import FastAPI

from api.routes import router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "Market Volatility Prediction API",
    description= "API for predicting 10-day future market volatility",
    version = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#(For frontend) FastAPI's CORS middleware tells browser that API permits requests from different origins 

app.include_router(router)
     