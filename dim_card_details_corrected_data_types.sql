SELECT date_payment_confirmed FROM dim_card_details
WHERE length(date_payment_confirmed) < 10;

-- Update data types in dim_card_details table with VARCHAR lengths
ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(19), 
    ALTER COLUMN expiry_date TYPE VARCHAR(5);
    ALTER COLUMN date_payment_confirmed TYPE DATE


