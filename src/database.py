from sqlalchemy import create_engine, text

DATABASE_URL = (
    "postgresql://postgres:VolatileMarket@localhost:5432/market_volatility"
)

engine = create_engine(DATABASE_URL)

def create_predictions_table():
    #create predictions table if it doesn't already exist

    query = """
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY, 
        prediction_date TIMESTAMP NOT NULL,
        predicted_volatility DOUBLE PRECISION NOT NULL,
        model_version VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    # "id SERIAL PRIMARY KEY" gives every prediction a unique ID. PRIMARY KEY means no two rows can have the same ID.
    # "prediction_date TIMESTAMP NOT NULL" stores market date associated with the prediction, NOT NULL means every prediction must have a date.
    # "predicted volatility" stores catboost output 
    # "model_version" not super necessary at the moment, but if we were to use a new model or retrain the one we have, we would know which model genereated which results.
    # "created_at" PostgreSQL automatically records when the prediction was inserted.
    with engine.begin() as connection:
        connection.execute(text(query))