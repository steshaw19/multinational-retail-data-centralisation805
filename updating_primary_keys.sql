-- Shows all the column names in each table.
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public';

-- Code to check column names 
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'orders_table';

ALTER TABLE dim_date_times
ADD PRIMARY KEY (date_uuid);

ALTER TABLE dim_card_details
ADD PRIMARY KEY (card_number);

ALTER TABLE dim_products
ADD PRIMARY KEY (product_code);

ALTER TABLE dim_store_details
ADD PRIMARY KEY (store_code);

ALTER TABLE dim_users
ADD PRIMARY KEY (user_uuid);



