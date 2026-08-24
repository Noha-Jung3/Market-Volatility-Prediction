from pathlib import Path

import pandas as pd
from joblib import load
from sqlalchemy import text

from src.ingest import update_raw_market_data
from src.features import update_engineered_features
from src.database import engine


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "catboost_volatility_model.pkl"
)


def load_model():
    """Load trained CatBoost model."""
    return load(MODEL_PATH)


def get_latest_features():
    """Retrieve the most recent engineered features."""

    query = """
    SELECT *
    FROM engineered_features
    ORDER BY "Date" DESC
    LIMIT 1
    """

    return pd.read_sql(query, engine)

def save_prediction(date, prediction):
    #save latest model prediction to PostgreSQL
    query = """
    INSERT INTO Predictions (
        Prediction_date,
        predicted_vol_10,
        model_name
    )
    VALUES (
        :prediction_date,
        :predicted_vol_10,
        :model_name
    )

    ON CONFLICT (Prediction Date)
    DO NOTHING
    """

    with engine.begin() as connection:
        connection.execute(
            text(query),
            {
                "prediction_date": date,
                "predicted_vol_10": prediction,
                "model_name": "CatBoost"
            }
        )

def predict_latest():
    """Predict volatility for the latest available market data."""

    model = load_model()

    latest = get_latest_features()

    X = latest.drop(columns=["Date"])

    prediction = float(model.predict(X)[0])

    prediction_date = latest["Date"].iloc[0]

    save_prediction(
        prediction_date,
        prediction
    )

    return {
        "date": str(prediction_date),
        "prediction": prediction
    }

def update_and_predict():
    ingestion_result = update_raw_market_data()
    if ingestion_result["rows_added"] > 0:
        feature_result = update_engineered_features()
    else:
        feature_result = {
            "status": "skipped",
            "reason": "No new market data",
            "rows_processed": 0
        }
    prediction = predict_latest()
    return {
    "ingestion": ingestion_result,
    "features": feature_result,
    "prediction": prediction
    }

