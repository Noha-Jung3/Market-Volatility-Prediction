
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
-- "what did the model predict?"

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

CREATE TABLE prediction_performance (
    prediction_date DATE PRIMARY KEY,

    predicted_vol_10 DOUBLE PRECISION,

    actual_vol_10 DOUBLE PRECISION,

    error DOUBLE PRECISION,

    absolute_error DOUBLE PRECISION,

    squared_error DOUBLE PRECISION,

    model_name TEXT,

    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- "How well did the model perform?"
-- all three errors? -> error lets us know if prediction was over predicted or under predicted
-- absolute_error lets us know about the magnitude of the error, and squared_error is useful for calculating MSE or RMSE

SELECT *
FROM prediction_performance

SELECT *
FROM prediction_performance
ORDER BY prediction_date DESC;

SELECT
    prediction_date,
    predicted_vol_10,
    actual_vol_10
FROM prediction_performance
WHERE prediction_date = '2026-07-28';