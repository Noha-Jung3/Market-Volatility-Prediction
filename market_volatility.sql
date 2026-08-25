
CREATE TABLE market_data (
	date DATE,
	open FLOAT,
	high FLOAT,
	low FLOAT,
	close FLOAT,
	volume BIGINT
)

SELECT COUNT(*)
FROM raw_market_data;

SELECT *
FROM engineered_features
WHERE
    log_return IS NULL OR
    return_20d IS NULL OR
    vol_20 IS NULL;

SELECT MAX("Date")
FROM engineered_features;

    SELECT *
    FROM engineered_features
    ORDER BY "Date" DESC
    LIMIT 1

CREATE TABLE Predictions(
	Prediction_date DATE PRIMARY KEY,
	
    predicted_vol_10 DOUBLE PRECISION,

    model_name TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

SELECT MAX("Date")
FROM engineered_features;

SELECT *
FROM predictions 

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'predictions'
ORDER BY ordinal_position;

SELECT *
FROM predictions
ORDER BY created_at DESC;

