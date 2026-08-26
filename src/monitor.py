import pandas as pd
import numpy as np

from sqlalchemy import text

from src.database import engine

def get_pending_predictions():
    #retrieve predictions that have not yet been evaluated
    query = """
    SELECT * 
    FROM Predictions
    WHERE Prediction_date <= (
        SELECT MAX ("Date") - INTERVAL '10 Days'
        FROM raw_market_data
    )
    AND Prediction_date NOT IN (
        SELECT prediction_date
        FROM prediction_performance
    )
    ORDER BY Prediction_date
    """
    #"Give me predictions for which enough market data should now exist, but which we haven't evaluated yet"
    predictions = pd.read_sql(query, engine)

    predictions["prediction_date"] = pd.to_datetime(
        predictions["prediction_date"]
    )

    return predictions

def get_market_data():
    #retrieve historical market data
    query = """
    SELECT "Date", "Close"
    FROM raw_market_data
    ORDER BY "Date"
    """
    market_data = pd.read_sql(query, engine)

    market_data["Date"] = pd.to_datetime(
        market_data["Date"]
    )

    return market_data
    # we only need "date" and "close to calculate the actual volatility"

def calculate_actual_volatility(market_data):
    #standard deviation over 10 days 
    df = market_data.copy()

    df["log_return"] = np.log(df["Close"]/df["Close"].shift(1))

    df["future_vol_10"] = (df["log_return"].rolling(10).std().shift(-10))

    return df


def evaluate_predictions():
    """Evaluate all predictions for which actual outcomes are available."""

    predictions = get_pending_predictions()

    if predictions.empty:
        return {
            "status": "up_to_date",
            "evaluated": 0
        }

    market_data = get_market_data()

    market_data = calculate_actual_volatility(market_data)

    results = predictions.merge(
        market_data[["Date", "future_vol_10"]],
        left_on="prediction_date",
        right_on="Date",
        how="left"
    )

    results = results.dropna(
        subset=["future_vol_10"]
    )

    if results.empty:
        return {
            "status": "no_outcomes_available",
            "evaluated": 0
        }

    results["error"] = (
        results["predicted_vol_10"]
        - results["future_vol_10"]
    )

    results["absolute_error"] = (
        results["error"].abs()
    )

    results["squared_error"] = (
        results["error"] ** 2
    )

    for _, row in results.iterrows():

        query = """
        INSERT INTO prediction_performance (
            prediction_date,
            predicted_vol_10,
            actual_vol_10,
            error,
            absolute_error,
            squared_error,
            model_name
        )
        VALUES (
            :prediction_date,
            :predicted_vol_10,
            :actual_vol_10,
            :error,
            :absolute_error,
            :squared_error,
            :model_name
        )
        """

        with engine.begin() as connection:
            connection.execute(
                text(query),
                {
                    "prediction_date": row["prediction_date"],
                    "predicted_vol_10": row["predicted_vol_10"],
                    "actual_vol_10": row["future_vol_10"],
                    "error": row["error"],
                    "absolute_error": row["absolute_error"],
                    "squared_error": row["squared_error"],
                    "model_name": row["model_name"]
                }
            )

    return {
        "status": "success",
        "evaluated": len(results)
    }

def run_monitoring():
    #Run prediction monitoring process.
    evaluation_result = evaluate_predictions()

    return {
        "evaluation": evaluation_result
    }