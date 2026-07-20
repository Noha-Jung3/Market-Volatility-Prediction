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
WHERE dataset = 'validation';

SELECT COUNT(*)
FROM market_data

SELECT COUNT(*)
FROM market_data
WHERE dataset = 'train';

SELECT AVG(vol_10)
FROM market_data
WHERE dataset = 'train';


