-- Update data types in dim_date_times table

ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(2),
    ALTER COLUMN year TYPE VARCHAR(4),
    ALTER COLUMN day TYPE VARCHAR(2),
    ALTER COLUMN time_period TYPE VARCHAR(20),
    ALTER COLUMN date_uuid TYPE UUID USING NULLIF(date_uuid, '')::UUID;

-- Code to check column types
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_date_times';