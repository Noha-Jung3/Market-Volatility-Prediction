CREATE TABLE market_data (
	date DATE,
	open FLOAT,
	high FLOAT,
	low FLOAT,
	close FLOAT,
	volume BIGINT
);

INSERT INTO market_data
VALUES (
    '2026-01-01',
    680,
    690,
    675,
    685,
    100000000
);


SELECT *
FROM market_data
LIMIT 5;
