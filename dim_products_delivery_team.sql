SELECT * FROM dim_products;

-- Remove the '£' character from 'product_price'
UPDATE dim_products
    SET product_price = REPLACE(product_price, '£', '');
    
-- Add a new column 'weight_class'
ALTER TABLE dim_products
    ADD COLUMN weight_class VARCHAR(50);

-- Update 'weight_class' based on 'weight' range
UPDATE dim_products
    SET weight_class =
        CASE
            WHEN weight_kg < 2 THEN 'Light'
            WHEN weight_kg >= 2 AND weight < 40 THEN 'Mid_Sized'
            WHEN weight_kg >= 40 AND weight < 140 THEN 'Heavy'
            WHEN weight_kg >= 140 THEN 'Truck_Required'
            ELSE NULL
        END;