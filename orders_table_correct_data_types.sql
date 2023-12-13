SELECT * FROM orders_table;

-- Change data type of date_uuid from TEXT to UUID
ALTER TABLE orders_table
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;

-- Change data type of user_uuid from TEXT to UUID
ALTER TABLE orders_table
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID;

-- Change data type of card_number from TEXT to VARCHAR(?)
ALTER TABLE orders_table
    ALTER COLUMN card_number TYPE VARCHAR(19);
    
-- Change data type of store_code from TEXT to VARCHAR(?)
ALTER TABLE orders_table
    ALTER COLUMN store_code TYPE VARCHAR(12);

-- Change data type of product_code from TEXT to VARCHAR(?)
ALTER TABLE orders_table
    ALTER COLUMN product_code TYPE VARCHAR(11);

-- Change data type of product_quantity from BIGINT to SMALLINT
ALTER TABLE orders_table
    ALTER COLUMN product_quantity TYPE SMALLINT;
