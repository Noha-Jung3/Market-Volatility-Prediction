from pathlib import Path

import pandas as pd
from joblib import load

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


def predict_latest():
    """Predict volatility for the latest available market data."""

    model = load_model()

    latest = get_latest_features()

    X = latest.drop(columns=["Date"])

    prediction = model.predict(X)[0]

    return {
        "date": latest["Date"].iloc[0],
        "prediction": float(prediction)
    }