import pandas as pd
import yfinance as yf

from src.database import engine


def update_raw_market_data():
    query = """
    SELECT MAX ("Date")
    FROM raw_market_data        
    """

    latest_date = pd.read_sql(
        query, engine
    ).iloc[0,0]

    new_data = yf.download("SPY", start = latest_date.strftime("%Y-%m-%d"),
    auto_adjust=True)

    new_data = new_data.reset_index()

    new_data = new_data[new_data["Date"] > latest_date]

    new_data.columns = [col[0] for col in new_data.columns]

    new_data = new_data[["Date", "Open", "High", "Low", "Close", "Volume"]]

    new_data = new_data.dropna(subset=["Open", "High", "Low", "Close", "Volume"])

    if new_data.empty:
        return {"status": "up_to_date", "rows_added": 0, "latest_date": str(latest_date)}

    newest_date = str(new_data["Date"].max())

    new_data.to_sql(
    "raw_market_data",
    engine,
    if_exists="append",
    index=False)

    return {
    "status": "success",
    "rows_added": len(new_data),
    "latest_date": newest_date}