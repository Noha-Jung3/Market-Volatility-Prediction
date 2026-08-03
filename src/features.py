import numpy as np
import pandas as pd
from src.database import engine

def engineer_features(df):
    """
    Generate engineered features from raw OHLCV market data.

    ~Parameters~
    ----------
    df : pandas.DataFrame
        Raw market data containing Date, Open, High, Low, Close and Volume.

    ~Returns~
    -------
    pandas.DataFrame
        Market data with engineered features ready for prediction.
    """

    df = df.copy()

    # Ensure correct order
    df = df.sort_values("Date")

    # Convert columns to numeric
    cols = ["Open", "High", "Low", "Close", "Volume"]

    df[cols] = df[cols].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Log return
    df["log_return"] = np.log(
        df["Close"] / df["Close"].shift(1)
    )

    # Rolling returns
    df["return_5d"] = df["log_return"].rolling(5).sum()
    df["return_10d"] = df["log_return"].rolling(10).sum()
    df["return_20d"] = df["log_return"].rolling(20).sum()

    # Rolling volatility
    df["vol_5"] = df["log_return"].rolling(5).std()
    df["vol_10"] = df["log_return"].rolling(10).std()
    df["vol_20"] = df["log_return"].rolling(20).std()

    # Price ranges
    df["hl_range"] = (
        df["High"] - df["Low"]
    ) / df["Close"]

    df["oc_range"] = (
        df["Close"] - df["Open"]
    ) / df["Open"]

    # Volume features
    df["vol_change"] = df["Volume"].pct_change()

    df["vol_ratio"] = (
        df["Volume"] /
        df["Volume"].rolling(20).mean()
    )

    # Remove rows without enough history
    df = df.dropna().reset_index(drop=True)

    return df    

def update_engineered_features():
    raw = pd.read_sql(
        """
        SELECT *
        FROM raw_market_data
        ORDER BY "Date"
        """,
        engine
    )

    features = engineer_features(raw)

    features.to_sql(
        "engineered_features",
        engine,
        if_exists="replace",
        index = False
    )

    return {
    "status": "success",
    "rows_processed": len(features),
    "latest_date": str(features["Date"].max())}

