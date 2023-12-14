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
SELECT
    TO_CHAR(TO_DATE(month::text, 'MM'), 'Month') AS month,
    COUNT(month) AS total_sales    
FROM
    dim_date_times
GROUP BY
    month
ORDER BY
    total_sales DESC
LIMIT 12;

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

SELECT * FROM dim_date_times;

-- Task 9
WITH sale_time_difference AS (
  SELECT
    EXTRACT(YEAR FROM actual_time_taken) AS year,
    actual_time_taken - LEAD(actual_time_taken) OVER (ORDER BY actual_time_taken) AS time_diff
  FROM
    your_sales_table -- Replace with the actual name of your sales table
)
SELECT
  year,
  AVG(EXTRACT(EPOCH FROM time_diff)::INTERVAL) AS average_time_taken
FROM
  SalesCTE
WHERE
  time_diff IS NOT NULL
GROUP BY
  year
ORDER BY
  year;