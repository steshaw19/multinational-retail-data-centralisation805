-- View the data to familiarise
SELECT * FROM dim_users;

-- Change data type of first_name and last_name to VARCHAR(255)
ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255);

ALTER TABLE dim_users
    ALTER COLUMN last_name TYPE VARCHAR(255);

-- Change data type of date_of_birth from TEXT to DATE
ALTER TABLE dim_users
    ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE;

-- Change data type of country_code from TEXT to VARCHAR(?)
ALTER TABLE dim_users
    ALTER COLUMN country_code TYPE VARCHAR(3);

-- Change data type of user_uuid from TEXT to UUID
ALTER TABLE dim_users
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID;

-- Change data type of join_date from TEXT to DATE
ALTER TABLE dim_users
    ALTER COLUMN join_date TYPE DATE USING join_date::DATE;