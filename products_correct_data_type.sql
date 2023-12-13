SELECT new_ean FROM dim_products;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_products';

-- Rename 'removed' column to 'still_available'
ALTER TABLE dim_products
    RENAME COLUMN removed TO still_available;

-- Change data type of 'product_price' from TEXT to FLOAT. Would not cast automatically, so used this work-around.
ALTER TABLE dim_products
ADD COLUMN new_product_price FLOAT;

UPDATE dim_products
SET new_product_price = NULLIF(product_price, '')::FLOAT;

-- Drop the old column
ALTER TABLE dim_products
DROP COLUMN product_price;

-- Rename the new column to the original name
ALTER TABLE dim_products
RENAME COLUMN new_product_price TO product_price;

-- Change data type of 'weight' from TEXT to FLOAT
ALTER TABLE dim_products
    ALTER COLUMN weight_kg TYPE DOUBLE PRECISION;

-- Change data type of 'EAN' from TEXT to VARCHAR(). EAN in double quotations to preserve the capitalisation
ALTER TABLE dim_products
    ALTER COLUMN "EAN" TYPE VARCHAR(48);

-- Change data type of 'product_code' from TEXT to VARCHAR(?)
ALTER TABLE dim_products
ALTER COLUMN product_code TYPE VARCHAR(12);

-- Change data type of 'date_added' from TEXT to DATE
ALTER TABLE dim_products
    ALTER COLUMN date_added TYPE DATE;

-- Change data type of 'uuid' from TEXT to UUID
ALTER TABLE dim_products
    ALTER COLUMN uuid TYPE UUID USING NULLIF(uuid, '')::UUID;

-- Change data type of 'still_available' from TEXT to BOOLEAN. Spelling error in 'still_available' in dataset.
ALTER TABLE dim_products
    ALTER COLUMN still_available
    TYPE BOOLEAN 
    USING 
        (CASE 
            WHEN still_available = 'Still_avaliable' -- This spelling error needs to be watched out for.
            THEN TRUE 
            ELSE FALSE 
        END);

-- Change data type of 'weight_class' from TEXT to VARCHAR(?)
ALTER TABLE dim_products
    ALTER COLUMN weight_class TYPE VARCHAR(20);