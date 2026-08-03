from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres:VolatileMarket@localhost:5432/market_volatility"
)

engine = create_engine(DATABASE_URL)