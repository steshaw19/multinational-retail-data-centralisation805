SELECT * FROM dim_store_details;

-- Merge latitude columns
UPDATE dim_store_details
SET latitude = COALESCE(CAST(latitude AS FLOAT), CAST(latitude AS FLOAT));

-- Set data types
ALTER TABLE dim_store_details
ALTER COLUMN locality TYPE VARCHAR(255),
ALTER COLUMN store_code TYPE VARCHAR(12),
ALTER COLUMN staff_numbers TYPE SMALLINT,
ALTER COLUMN opening_date TYPE DATE,
ALTER COLUMN store_type TYPE VARCHAR(255),
ALTER COLUMN country_code TYPE VARCHAR(3),
ALTER COLUMN continent TYPE VARCHAR(255);