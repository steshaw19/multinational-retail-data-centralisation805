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
    TO_CHAR(TO_DATE(month::text, 'MM'), 'Month') AS month,
    COUNT(month) AS total_sales    
FROM
    dim_date_times
GROUP BY
    month
ORDER BY
    total_sales DESC
LIMIT 12;
```
Returns:
| month      | total_sales |
|------------|-------------|
| July       |       10284 |
| January    |       10249 |
| August     |       10225 |
| May        |       10150 |
| October    |       10130 |
| December   |       10119 |
| March      |       10119 |
| June       |        9965 |
| November   |        9867 |
| April      |        9755 |
| September  |        9752 |
| February   |        9508 |

The query took the numerical value given for each month and converted it to the name of the month to improve readability of the table. July was the most successful month for sales. All months were shown on the table due to the small number of rows it would produce.

## Task 4

The company is looking to increase its online sales.
They want to know how many sales are happening online vs offline.
Calculate how many products were sold and the amount of sales made for online and offline purchases.

You should get the following information:



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