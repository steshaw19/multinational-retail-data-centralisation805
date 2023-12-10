# Data Handling Project (multinational-retail-data-centralisation805) 

## Overview
This project focuses on data extraction, cleaning, and uploading to a database using Python. The data involves user information, PDF data, store details from an API, and product details from CSV files stored in an S3 bucket on AWS.

## Files

### `data_cleaning.py`
This script contains a `DataCleaning` class with methods to clean user data, PDF data, store data, and product data. It also includes methods to convert product weights to kilograms and upload cleaned data to a PostgreSQL database. The script is executed as a standalone application, performing data cleaning and uploading for product data.

### `data_extraction.py`
This file defines a `DataExtractor` class responsible for extracting data from a PostgreSQL database, PDFs, APIs, and S3. It includes methods to read tables from an RDS, retrieve PDF data using the tabula library, list the number of stores from an API, and retrieve store details from the same API. Additionally, there's a method to extract product details from an S3 bucket. The script also includes an example of using the `DataExtractor` class to retrieve user data from an RDS table, PDF data from a link, and store data from an API.

### `database_utils.py`
This script contains a `DatabaseConnector` class with methods to read database credentials from YAML files, initialize database engines, and upload data to a PostgreSQL database. The script also includes an example of using the `DatabaseConnector` class to initialize source and destination database engines.

## Usage
1. **Database Credentials**: Ensure that the credentials for the source and destination databases are correctly specified in the `db_creds.yaml` and `sales_data_creds.yaml` files.

2. **AWS Credentials**: If using the S3 extraction method, provide AWS credentials in the `aws_access.yaml` file.

3. **Execute Scripts**: Execute the scripts based on your requirements. The `data_cleaning.py` script is set up to run as a standalone application, performing data cleaning and uploading for product data. Adjust the commented sections in the script to enable cleaning and uploading for other data types.

4. **Run the Main Script**: Execute the main script (`data_extraction.py`) to demonstrate data extraction from various sources.

5. **Dependencies**: Make sure you have the required Python libraries installed. You can install them using the following:
   ```bash
   pip install pandas numpy re tabula requests yaml boto3 sqlalchemy

Feel free to customize the scripts according to your specific data handling needs and adapt the methods for your use case.

Please reach out for any questions or further assistance!
