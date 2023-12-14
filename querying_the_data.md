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
