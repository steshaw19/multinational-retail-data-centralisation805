SELECT * FROM dim_store_details;

--Task 1
SELECT
    country_code,
    COUNT(country_code) AS total_no_stores
FROM
    dim_store_details
GROUP BY
    country_code
ORDER BY
    total_no_stores DESC
LIMIT 3;

--Task 2
SELECT
    locality,
    COUNT(locality) AS total_no_stores
FROM
    dim_store_details
GROUP BY
    locality
ORDER BY
    total_no_stores DESC
LIMIT 7;

--Task 3
SELECT * FROM orders_table;
SELECT * FROM dim_date_times;
SELECT
    TO_CHAR(TO_DATE(dim_date_times.month::text, 'MM'), 'Month') AS month,
    ROUND(SUM(orders_table.product_quantity * dim_products.product_price)::numeric, 2) AS "total_sales (£)"
FROM
    orders_table
JOIN
    dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY
    month
ORDER BY
    "total_sales (£)" DESC
LIMIT 12;

-- Task 4
SELECT * FROM dim_store_details;

SELECT DISTINCT store_type
FROM dim_store_details;

SELECT
    COUNT(orders_table.store_code) AS numbers_of_sales,
    SUM(orders_table.product_quantity) AS product_quantity_count,
    CASE
        WHEN dim_store_details.store_type = 'Web Portal' THEN 'Web'
        ELSE 'Offline'
    END AS location_type
FROM
    orders_table
JOIN
    dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY
    location_type
ORDER BY product_quantity_count ASC;

-- Task 5
SELECT
    dim_store_details.store_type,
    CAST(SUM(orders_table.product_quantity * dim_products.product_price) AS NUMERIC(10, 2)) AS total_sales,
    CAST((SUM(orders_table.product_quantity * dim_products.product_price) / 
    SUM(SUM(orders_table.product_quantity * dim_products.product_price)) OVER ()) * 100 AS NUMERIC(10, 2)) AS "percentage_total(%)"
FROM
    dim_store_details
JOIN
    orders_table ON dim_store_details.store_code = orders_table.store_code
JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY
    dim_store_details.store_type
ORDER BY
    total_sales DESC;

-- Task 6
SELECT
    ROUND(SUM(orders_table.product_quantity * dim_products.product_price)::numeric, 2) AS "total_sales(£)",
    dim_date_times.year,
    dim_date_times.month
FROM
    orders_table
JOIN
    dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY
    dim_date_times.year,
    dim_date_times.month
ORDER BY
    "total_sales(£)" DESC
LIMIT 10;



-- Task 7
SELECT
    SUM(staff_numbers) AS total_staff_numbers,
    country_code
FROM
    dim_store_details
GROUP BY
    country_code
ORDER BY
    total_staff_numbers DESC;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_store_details';

SELECT DISTINCT staff_numbers
FROM dim_store_details
LIMIT 102;

ALTER TABLE dim_store_details
ALTER COLUMN staff_numbers TYPE NUMERIC
USING NULLIF(staff_numbers, '')::NUMERIC;

SELECT DISTINCT staff_numbers
FROM dim_store_details
WHERE staff_numbers !~ E'^\\d+$';

SELECT *
FROM dim_store_details
WHERE staff_numbers IS NULL;

UPDATE dim_store_details
SET
    staff_numbers = REPLACE(staff_numbers, '30e', '30');

UPDATE dim_store_details
SET
    staff_numbers = REPLACE(staff_numbers, '3n9', '39');

UPDATE dim_store_details
SET
    staff_numbers = REPLACE(staff_numbers, 'A97', '97');

UPDATE dim_store_details
SET
    staff_numbers = REPLACE(staff_numbers, '80R', '80');

UPDATE dim_store_details
SET
    staff_numbers = REPLACE(staff_numbers, 'J78', '78');
    
-- Task 8
SELECT
    ROUND(SUM(orders_table.product_quantity * dim_products.product_price)::numeric, 2) AS "total_sales (£)",
    dim_store_details.store_type,
    dim_store_details.country_code
FROM
    orders_table
JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
JOIN
    dim_store_details ON orders_table.store_code = dim_store_details.store_code
WHERE
    dim_store_details.country_code = 'DE'
GROUP BY
    dim_store_details.store_type, dim_store_details.country_code
ORDER BY
    "total_sales (£)" ASC;



-- Task 9

WITH date_times_cte AS (
    SELECT
        year,
        year || '-' || LPAD(month::TEXT, 2, '0') || '-' || LPAD(day::TEXT, 2, '0') || ' ' || timestamp AS complete_time
    FROM
        dim_date_times
)

SELECT
    year,
    AVG(time_difference) AS average_time_difference_per_year
FROM (
    SELECT
        year,
        complete_time::timestamp,
        LEAD(complete_time::timestamp) OVER (ORDER BY complete_time::timestamp) AS next_complete_time,
        LEAD(complete_time::timestamp) OVER (ORDER BY complete_time::timestamp) - complete_time::timestamp AS time_difference
    FROM date_times_cte
) AS subquery
GROUP BY year
ORDER BY average_time_difference_per_year DESC
LIMIT 5;

