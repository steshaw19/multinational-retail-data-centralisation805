SELECT longitude FROM dim_store_details
WHERE longitude = 'NULL';

-- Ensure only numeric values in the "longitude" column
UPDATE dim_store_details
SET longitude = NULL
WHERE NOT longitude ~ '^-[0-9]*\.?[0-9]*$';

-- Ensure only numeric values in the "latitude" column
UPDATE dim_store_details
SET latitude = NULL
WHERE NOT latitude ~ '^-[0-9]*\.?[0-9]*$';

-- Alter data types
ALTER TABLE dim_store_details
    ALTER COLUMN longitude TYPE FLOAT,
    ALTER COLUMN locality TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(12),
    ALTER COLUMN staff_numbers TYPE SMALLINT,
    ALTER COLUMN opening_date TYPE DATE,
    ALTER COLUMN store_type TYPE VARCHAR(255),
    ALTER COLUMN latitude TYPE FLOAT,
    ALTER COLUMN country_code TYPE VARCHAR(3),
    ALTER COLUMN continent TYPE VARCHAR(255);

-- Update 'location' column values where null to 'N/A'
UPDATE dim_store_details
    SET latitude = 'N/A'
    WHERE latitude IS NULL;