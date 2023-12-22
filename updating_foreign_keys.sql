-- Add foreign key constraints in orders_table

-- Reference dim_date_times (done)
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_table_date_uuid
FOREIGN KEY (date_uuid)
REFERENCES dim_date_times(date_uuid);


-- Reference dim_card_details
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_table_card_number
FOREIGN KEY (card_number)
REFERENCES dim_card_details(card_number);

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

