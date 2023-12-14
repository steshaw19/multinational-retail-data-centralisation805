# Data Analysis

## Task 1
The Operations team would like to know which countries we currently operate in and which country now has the most stores. Perform a query on the database to get the information, it should return the following information:

| country  | total_no_stores |
|----------|-----------------|
| GB       |             265 |
| DE       |             141 |
| US       |              34 |


```sql
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
```
Returns:
| country_code | total_no_stores |
|--------------|-----------------|
| GB           |             264 |
| DE           |             139 |
| US           |              33 |

From the available data, the three most popular store locations are Great Britain (GB), Germany (DE), and the United States (US).

## Task 2
The business stakeholders would like to know which locations currently have the most stores.

They would like to close some stores before opening more in other locations.

Find out which locations have the most stores currently. The query should return the following:
| locality         | total_no_stores |
|------------------|-----------------|
| Chapletown       |              14 |
| Belper           |              13 |
| Bushley          |              12 |
| Exeter           |              11 |
| High Wycombe     |              10 |
| Arbroath         |              10 |
| Rutherglen       |              10 |

```sql
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
```
Returns:
| locality       | total_no_stores |
|----------------|-----------------|
| Chapletown     |              14 |
| Belper         |              13 |
| Bushey         |              12 |
| Exeter         |              11 |
| Arbroath       |              10 |
| High Wycombe   |              10 |
| Rutherglen     |              10 |

This table shows the locations that have the most stores. No data has been lost from the cleaning process for any of these data.

## Task 3
Query the database to find out which months have produced the most sales. The query should return the following information:

| total_sales | month |
|-------------|-------|
|   673295.68 |     8 |
|   668041.45 |     1 |
|   657335.84 |    10 |
|   650321.43 |     5 |
|   645741.70 |     7 |
|   645463.00 |     3 |

```sql
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
```
Returns:
| month      | total_sales (£) |
|------------|------------------|
| August     | 614084.65        |
| January    | 611275.22        |
| October    | 605163.53        |
| July       | 591645.17        |
| May        | 591025.28        |
| March      | 585323.38        |
| December   | 579222.23        |
| June       | 578768.49        |
| September  | 575246.48        |
| November   | 574986.19        |
| April      | 570757.81        |
| February   | 564681.76        |


The query took the numerical value given for each month and converted it to the name of the month to improve readability of the table. August was the most successful month for sales based on the number of products sold. All months were shown on the table due to the small number of rows it would produce.

## Task 4

The company is looking to increase its online sales.
They want to know how many sales are happening online vs offline.
Calculate how many products were sold and the amount of sales made for online and offline purchases.

You should get the following information:
| numbers_of_sales | product_quantity_count | location |
|------------------|------------------------|----------|
| 26957            | 107739                 | Web      |
| 93166            | 374047                 | Offline  |

```sql
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
```

Returns:
| numbers_of_sales  | product_quantity_count | location_type  |
|-------------------|------------------------|----------------|
| 24689             | 98529                  | Web            |
| 85103             | 341425                 | Offline        |

The analysis shows that offline sales are more than 3 times higher than web sales. This query joined `dim_sales_table` and `orders_table` through the store code to retrieve the amount of products sold. It then combined mall, kiosk etc... into offline sales leaving the web sales. The `CASE` method was moved into the `SELECT` method for this query to work.

## Task 5
The sales team wants to know which of the different store types has generated the most revenue so they know where to focus. Find out the total and percentage of sales coming from each of the different store types. The query should return:

| store_type  | total_sales | percentage_total(%) |
|-------------|-------------|---------------------|
| Local       | 3440896.52  | 44.87               |
| Web portal  | 1726547.05  | 22.44               |
| Super Store | 1224293.65  | 15.63               |
| Mall Kiosk  | 698791.61   | 8.96                |
| Outlet      | 631804.81   | 8.10                |

```sql
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
```
Returns:
| store_type   | total_sales  | percentage_total(%)  |
|--------------|--------------|----------------------|
| Local        | 3132748.77   | 44.49                |
| Web Portal   | 1581269.40   | 22.45                |
| Super Store  | 1112431.64   | 15.80                |
| Mall Kiosk   | 636332.97    | 9.04                 |
| Outlet       | 579397.41    | 8.23                 |

This query joined `dim_products`, `order_table`, and `dim_store_details` in order to answer the question. I struggled to round the data to 2 decimal places using `ROUND`, but made it work with the `CAST` function. This is something I may need to work on.

## Task 6

The company stakeholders want assurances that the company has been doing well recently. Find which months in which years have had the most sales historically. The query should return the following information:

| total_sales | year | month |
|-------------|------|-------|
| 27936.77    | 1994 | 3     |
| 27356.14    | 2019 | 1     |
| 27091.67    | 2009 | 8     |
| 26679.98    | 1997 | 11    |
| 26310.97    | 2018 | 12    |
| 26277.72    | 2019 | 8     |
| 26236.67    | 2017 | 9     |
| 25798.12    | 2010 | 5     |
| 25648.29    | 1996 | 8     |
| 25614.54    | 2000 | 1     |

```sql
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
```
Returns:
| total_sales(£) | year | month |
|----------------|------|-------|
| 25649.16       | 2019 | 1     |
| 25568.32       | 1994 | 3     |
| 25173.64       | 2009 | 8     |
| 24549.25       | 1997 | 11    |
| 24235.50       | 2010 | 5     |
| 24150.96       | 1998 | 12    |
| 24109.91       | 2017 | 9     |
| 23556.99       | 2000 | 1     |
| 23525.48       | 2012 | 8     |
| 23484.53       | 2019 | 8     |

This highlights August (8) as a month that has been successful for sales in various years with January (1) popping up twice.

## Task 7
The operations team would like to know the overall staff numbers in each location around the world. Perform a query to determine the staff numbers in each of the countries the company sells in.
The query should return the values:

| total_staff_numbers | country_code |
|---------------------|--------------|
|               13307 |           GB |
|                6123 |           DE |
|                1384 |           US |

```sql
SELECT
    SUM(staff_numbers) AS total_staff_numbers,
    country_code
FROM
    dim_store_details
GROUP BY
    country_code
ORDER BY
    total_staff_numbers DESC;
```
Returns:
| total_staff_numbers | country_code |
|---------------------|--------------|
| 13132               | GB           |
| 6054                | DE           |
| 1304                | US           |

## Task 8
The sales team is looking to expand their territory in Germany. Determine which type of store is generating the most sales in Germany.

The query will return:
| total_sales (£)  | store_type  | country_code |
|------------------|-------------|--------------|
| 198373.57        | Outlet      | DE           |
| 247634.20        | Mall Kiosk  | DE           |
| 384625.03        | Super Store | DE           |
| 1109909.59       | Local       | DE           |

```sql
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
    "total_sales (£)" DESC;
```
Returns:
| total_sales (£) | store_type   | country_code |
|-----------------|--------------|--------------|
| 1011813.78      | Local        | DE           |
| 345698.50       | Super Store  | DE           |
| 224414.43       | Mall Kiosk   | DE           |
| 181926.15       | Outlet       | DE           |

This query was similiar to previous queries, however, a `WHERE` function was used to only gather 'DE' rows. Local stores are massing the most total sales currently, although it would be interesting to see the percentage of sales based on their number compared to other store types.

## Task 9
Sales would like the get an accurate metric for how quickly the company is making sales.

Determine the average time taken between each sale grouped by year, the query should return the following information:

| year | actual_time_taken                                       |
|------|---------------------------------------------------------|
| 2013 | "hours": 2, "minutes": 17, "seconds": 12, "milliseconds":... |
| 1993 | "hours": 2, "minutes": 15, "seconds": 35, "milliseconds":... |
| 2002 | "hours": 2, "minutes": 13, "seconds": 50, "milliseconds":... |
| 2022 | "hours": 2, "minutes": 13, "seconds": 6,  "milliseconds":... |
| 2008 | "hours": 2, "minutes": 13, "seconds": 2,  "milliseconds":... |


```sql
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
```
Returns:

| year | average_time_difference_per_year                                   |
|------|---------------------------------------------------------------------|
| 2013 | {"hours":2,"minutes":17,"seconds":15,"milliseconds":655.442}     |
| 1993 | {"hours":2,"minutes":15,"seconds":40,"milliseconds":129.515}    |
| 2002 | {"hours":2,"minutes":13,"seconds":49,"milliseconds":478.228}    |
| 2008 | {"hours":2,"minutes":13,"seconds":3,"milliseconds":532.442}     |
| 2022 | {"hours":2,"minutes":13,"seconds":2,"milliseconds":3.698}       |

This query began by combining the time data (month, day, year, timestamp) into one column. It then used the `LEAD` function to create a new column with the next timestamp alongside the previous one. With this, a time difference could be found between values. The query then created an average_time_difference column and grouped the data by year and ordered by the average_time_difference. The data were limited to 5 values as was the case with the example.