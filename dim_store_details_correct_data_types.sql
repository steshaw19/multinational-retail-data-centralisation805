SELECT * FROM dim_store_details;

SELECT staff_numbers
FROM dim_store_details
WHERE LENGTH(staff_numbers) > 2;

DELETE FROM dim_store_details
WHERE LENGTH(country_code) > 2;

-- Merge latitude columns
UPDATE dim_store_details
SET latitude = COALESCE(CAST(latitude AS FLOAT), CAST(lat AS FLOAT));

-- Set data types
ALTER TABLE dim_store_details
ALTER COLUMN locality TYPE VARCHAR(255),
ALTER COLUMN store_code TYPE VARCHAR(12),
ALTER COLUMN opening_date TYPE DATE,
ALTER COLUMN store_type TYPE VARCHAR(255),
ALTER COLUMN country_code TYPE VARCHAR(3),
ALTER COLUMN continent TYPE VARCHAR(255);