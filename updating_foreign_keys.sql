-- Add foreign key constraints in orders_table

-- Reference dim_date_times (done)
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_table_date_uuid
FOREIGN KEY (date_uuid)
REFERENCES dim_date_times(date_uuid);


-- Reference dim_card_details (DONE)
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_table_card_number
FOREIGN KEY (card_number)
REFERENCES dim_card_details(card_number);

SELECT *
FROM orders_table
WHERE card_number LIKE '%0000%';

-- Reference dim_products (done)
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_table_product_code
FOREIGN KEY (product_code)
REFERENCES dim_products(product_code);

-- Reference dim_store_details (done)
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_table_store_code
FOREIGN KEY (store_code)
REFERENCES dim_store_details(store_code);

-- Reference dim_users (done)
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_table_user_uuid
FOREIGN KEY (user_uuid)
REFERENCES dim_users(user_uuid);

SELECT *
FROM orders_table
SET card_number = SUBSTRING(card_number, 1, LENGTH(card_number) - 4) AS new_card_number
WHERE new_card_number NOT IN (SELECT card_number FROM dim_card_details); -- AROUND 1000 DATA DELETED FROM DIM_STORE_DETAILS

-- Update card_number in orders_table
UPDATE orders_table
SET card_number = SUBSTRING(card_number, 1, LENGTH(card_number) - 4)
WHERE card_number NOT IN (SELECT card_number FROM dim_card_details);

-- Delete records from dim_card_details
DELETE FROM dim_card_details
WHERE card_number IN (SELECT new_card_number FROM orders_table);

SELECT *
FROM orders_table
WHERE user_uuid NOT IN (SELECT user_uuid FROM dim_users);

SELECT store_code
FROM dim_store_details
WHERE store_code LIKE 'DA-ACC520AE';

DELETE FROM orders_table
WHERE card_number NOT IN (SELECT card_number FROM dim_card_details);


-- checking which values exist in both tables
SELECT dim_card_details.card_number
FROM dim_card_details
INNER JOIN orders_table ON dim_card_details.card_number = orders_table.card_number;

-- checking which values don't match between the two tables
SELECT dim_card_details.*
FROM dim_card_details
LEFT JOIN orders_table ON dim_card_details.card_number = orders_table.card_number
WHERE orders_table.card_number IS NULL;

SELECT *
FROM orders_table
WHERE LENGTH(card_number) = 15;

-- delete values that don't match
DELETE FROM orders_table
LEFT JOIN dim_card_details ON orders_table.card_number = dim_card_details.card_number
WHERE dim_card_details.card_number IS NULL;
