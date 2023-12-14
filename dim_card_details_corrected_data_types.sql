SELECT * FROM dim_card_details;

-- Update data types in dim_card_details table with VARCHAR lengths
ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(19), 
    ALTER COLUMN expiry_date TYPE VARCHAR(5),
    ALTER COLUMN date_payment_confirmed TYPE DATE;
