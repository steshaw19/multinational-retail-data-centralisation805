# Data Handling Project (multinational-retail-data-centralisation805) 

## Table of Contents
- [Description](#description)
- [Installation Instructions](#installation-instructions)
- [Usage Instructions](#usage-instructions)
- [File Structure](#file-structure)
- [License Information](#license-information)

## Description
This project focuses on data extraction, cleaning, and uploading to a database using Python. The data involves user information, PDF data, store details from an API, and product details from CSV files stored in an S3 bucket on AWS.

1. `database_utils.py`: Defines a `DatabaseConnector` class for handling database connections, reading credentials, initializing database engines, and uploading data to a PostgreSQL database.

2. `data_extraction.py`: Contains a `DataExtractor` class for reading data from an RDS database, extracting PDF data, making API calls, and downloading data from an S3 bucket.

3. `data_cleaning.py`: Implements a `DataCleaning` class with methods for cleaning user data, PDF data, store data, product data, orders data, and date details data.

## Installation Instructions
1. Clone the repository: `git clone <repository_url>`
2. Install the required Python packages: `pip install -r requirements.txt`

## Usage Instructions
1. **Database Credentials**: Ensure that the credentials for the source and destination databases are correctly specified in the `db_creds.yaml` and `sales_data_creds.yaml` files.

2. **AWS Credentials**: If using the S3 extraction method, provide AWS credentials in the `aws_access.yaml` file.

3. **Execute Scripts**: Execute the scripts based on your requirements. The `data_cleaning.py` script is set up to run as a standalone application, performing data cleaning and uploading for product data. Adjust the commented sections in the script to enable cleaning and uploading for other data types.

4. **Run the Main Script**: Execute the main script (`data_extraction.py`) to demonstrate data extraction from various sources.

5. **Dependencies**: Make sure you have the required Python libraries installed. You can install them using the following or by referring to `requirements.txt`:
   ```bash
   pip install pandas numpy re tabula requests yaml boto3 sqlalchemy

6. **Security**: Ensure that all credentials and passkeys are saved in .yaml files and not available in the main script. Add these files to a .gitignore file in your VS Studio to ensure that no credentials are uploaded to GitHub and made available to individuals who should not have access.

## File Structure
- `database_utils.py`: Database connection utility class.
- `data_extraction.py`: Data extraction and API interaction class.
- `data_cleaning.py`: Data cleaning and database upload class.
- `requirements.txt`: List of Python dependencies.

## License Information
Feel free to customize the scripts according to your specific data handling needs and adapt the methods for your use case.

Please reach out for any questions or further assistance!
