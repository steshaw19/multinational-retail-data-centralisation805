# Data Handling Project (multinational-retail-data-centralisation805) 

## Table of Contents
- [Description](#description)
- [Installation Instructions](#installation-instructions)
- [Usage Instructions](#usage-instructions)
- [File Structure](#file-structure)
- [License Information](#license-information)

## Description
This project focuses on data extraction, cleaning, and uploading to a database using Python. The data involves user information, PDF data, store details from an API, and product details from CSV files stored in an S3 bucket on AWS. SQL was used to develop a star-based database scheme ensuring correct data types and primary and foreign keys. SQL was then used to query the data and present an analysis for a demo business situation. 

1. `database_utils.py`: Defines a `DatabaseConnector` class for handling database connections, reading credentials, initializing database engines, and uploading data to a PostgreSQL database.

2. `data_extraction.py`: Contains a `DataExtractor` class for reading data from an RDS database, extracting PDF data, making API calls, and downloading data from an S3 bucket.

3. `data_cleaning.py`: Implements a `DataCleaning` class with methods for cleaning user data, PDF data, store data, product data, orders data, and date details data.

4. `querying_the_data.md`: Provides a description of each required analysis, the SQL query used and the returned data summarised in tables and text in Markdown format. This information is organised by task and the original working SQL code file can be found at `querying_the_data.sql`. 

## Installation Instructions
1. Clone the repository: `git clone https://github.com/steshaw19/multinational-retail-data-centralisation805`
2. Install the required Python packages: `pip install -r requirements.txt`
3. Install required SQL packages. This project used pgAdmin 4, SQLTools in VS Code, and SQLTools PostgreSQL/Cockroach Driver in VS Code. Full information on installation can be found in `sql_installation_requirements.sql`

## Usage Instructions
1. **Database Credentials**: Ensure that the credentials for the source and destination databases are correctly specified in the `db_creds.yaml` and `sales_data_creds.yaml` files.

2. **AWS Credentials**: If using the S3 extraction method, provide AWS credentials in the `aws_access.yaml` file.

3. **Execute Scripts**: Execute the scripts based on your requirements. The `data_cleaning.py` script is set up to run as a standalone application, performing data cleaning and uploading for product data. Adjust the commented sections in the script to enable cleaning and uploading for other data types.

4. **Run the Main Script**: Execute the main script (`data_extraction.py`) to demonstrate data extraction from various sources.

5. **Dependencies**: Make sure you have the required Python libraries installed. You can install them using the following or by referring to `requirements.txt`:
   ```bash
   pip install pandas numpy tabula requests pyyaml boto3 sqlalchemy

6. **Security**: Ensure that all credentials and passkeys are saved in .yaml files and not available in the main script. Add these files to a .gitignore file in VS Studio (or similar software) to ensure that no credentials are uploaded to GitHub and made available to individuals who should not have access.

7. **Accessing Docstrings Information**: You can access docstrings directly within Python using the `help` function. For example, to get information about a class or function, open a Python shell and execute: 
   ```python
   help(class_or_function_name)
   ```
## File Structure
- `database_utils.py`: Database connection utility class.
- `data_extraction.py`: Data extraction and API interaction class.
- `data_cleaning.py`: Data cleaning and database upload class.
- `querying_the_data.md`: Analysis of database using SQL.
- `querying_the_data.sql`: Working document of SQL query code.
- `dim_card_details_corrected_data_types.sql`: Edits data types using SQL for card details data table.
- `dim_data_time_corrected_data.sql`: Edits data types using SQL for date and time of orders data table.
- `dim_products_delivery_team.sql` & `products_correct_data_type.sql`: Edits data types using SQL for products data table.
- `dim_store_details_correct_data_types.sql`: Edits data types using SQL for store details data table.
- `dim_users_correct_data_type.sql`: Edits data types using SQL for user details table.
- `orders_table_correct_data_types.sql`: Edits data types and cleans orders data table.
- `requirements.txt`: List of Python dependencies.

## License Information
Feel free to customize the scripts according to your specific data handling needs and adapt the methods for your use case.

Please reach out for any questions or further assistance!
