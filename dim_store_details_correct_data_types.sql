SELECT * FROM dim_store_details;


-- Set data types
ALTER TABLE dim_store_details
    ALTER COLUMN locality TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(12),
    ALTER COLUMN store_type TYPE VARCHAR(255),
    ALTER COLUMN staff_numbers TYPE INT,
    ALTER COLUMN country_code TYPE VARCHAR(3),
    ALTER COLUMN continent TYPE VARCHAR(255);