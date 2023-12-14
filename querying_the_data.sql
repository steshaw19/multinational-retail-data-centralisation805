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

