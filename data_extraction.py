import boto3
import json
import pandas as pd
import requests
import tabula
from tabula.io import read_pdf
import time
import yaml
from database_utils import DatabaseConnector
from io import BytesIO
from sqlalchemy import inspect


class DataExtractor:
    """
    A class for data extraction from various sources.

    Attributes:
    - db_connector: An instance of the DatabaseConnector class.
    - credentials: Database credentials.
    - source_engine: SQLAlchemy engine for the source database.

    Methods:
    - read_rds_table(table_name: str): Read data from an RDS database table.
    - list_db_tables(): List all tables in the source database.
    - retrieve_pdf_data(pdf_link: str): Retrieve tables from a PDF document.
    - list_number_of_stores(number_of_stores_endpoint: str, headers: dict): List the number of stores via an API.
    - retrieve_stores_data(store_endpoint_pattern: str, headers: dict, total_stores: int): Retrieve store data via an API.
    - extract_from_s3(s3_address: str, aws_credentials_path: str = 'aws_access.yaml'): Extract data from an S3 bucket.
    - download_s3_data(s3_url: str): Download JSON data from S3.
    """
    def __init__(self):
        # Instantiate DatabaseConnector to access its methods
        self.db_connector = DatabaseConnector()
        # Get credentials
        self.credentials = self.db_connector.read_source_db_creds()
        # Initialize the database engine
        self.source_engine = self.db_connector.init_source_db_engine(self.credentials)

    # Reads source database table to retrieve column names.
    def read_rds_table(self, table_name):
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, self.source_engine, index_col='index')
            return df
        except Exception as e:
            print(f"Error reading table {table_name}: {e}")
            return None
        
    # Lists tables in source database.
    def list_db_tables(self):
        try:
            # Use the inspector to get table names
            inspector = inspect(self.source_engine)
            table_names = inspector.get_table_names()
            return table_names
        except Exception as e:
            print(f"Error listing tables: {e}")
            return None
    
    # Extracts card details from a PDF file.
    def retrieve_pdf_data(self, pdf_link):
        # Use tabula to extract tables from the PDF
        try:
            pdf_df = tabula.read_pdf(pdf_link, pages='all', multiple_tables=True)
            
            # Concatenate all tables into a single DataFrame
            pdf_df = pd.concat(pdf_df, ignore_index=True)
            
            return pdf_df
        except Exception as e:
            print(f"Error extracting data from PDF: {e}")
            return None
    
    # Gets the number of stores from API
    def list_number_of_stores(self, number_of_stores_endpoint, headers):
        try:
            response = requests.get(number_of_stores_endpoint, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error listing number of stores: {e}")
            return None
    
    # Extracts all store data from API for the number of stores retrieved from previous method
    def retrieve_stores_data(self, store_endpoint_pattern, headers, total_stores):
        all_stores_data = []

        for store_number in range(0, total_stores):
            store_endpoint = f"{store_endpoint_pattern}/{store_number}"
            try:
                response = requests.get(store_endpoint, headers=headers)
                response.raise_for_status()
                store_data = response.json()
                all_stores_data.append(store_data)
            except requests.exceptions.RequestException as e:
                print(f"Error retrieving data for store {store_number}: {e}")
                return None
        all_stores_df = pd.DataFrame(all_stores_data)
        all_stores_df = all_stores_df.set_index('index')
        return all_stores_df
    
    # Extracts product data from AWS S3 Bucket
    def extract_from_s3(s3_address, aws_credentials_path='aws_access.yaml'):
        # Read AWS credentials from YAML file
        with open(aws_credentials_path, 'r') as file:
            aws_credentials = yaml.safe_load(file)

        # Extract credentials from the YAML file
        aws_access_key_id = aws_credentials['aws_access_key_id']
        aws_secret_access_key = aws_credentials['aws_secret_access_key']

        # Extract bucket and key from S3 address
        bucket_name, key = s3_address.split('s3://')[1].split('/', 1)

        # Create an S3 client
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # Download the file from S3
        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read()

        # Convert the content to a DataFrame
        product_details_data = pd.read_csv(BytesIO(content))
        product_details_data = product_details_data.set_index(product_details_data.columns[0])
        return product_details_data
    
    # Extracts JSON date_time table data from S3 Bucket
    def download_s3_data(self, s3_url):
        response = requests.get(s3_url)
        date_data = json.loads(response.text)
        return date_data

extractor = DataExtractor() # Create an instance of the DataExtractor class

# Read data from the RDS table (example table name: 'legacy_users')
user_data_df = extractor.read_rds_table('legacy_users')
orders_data_df = extractor.read_rds_table('orders_table')

# Provide the PDF link as an argument to the retrieve_pdf_data method for card details
pdf_data = extractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')

# API details and calls method to retrieve store details from API
number_of_stores_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores/" # Retrieves number of stores available
store_endpoint_pattern = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details" # Retrieves details for individual store
headers = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"} # Headers to access API
number_of_stores = extractor.list_number_of_stores(number_of_stores_endpoint, headers) # Calls method to retrieve store count
total_stores = number_of_stores.get('number_stores', 0) # Assigns variable for store count
all_store_data = extractor.retrieve_stores_data(store_endpoint_pattern, headers, total_stores) # Calls method to retrieve all store data

# AWS credentials for downloaded products data from AWS S3 Bucket
aws_credentials_path = 'aws_access.yaml'
s3_address = 's3://data-handling-public/products.csv'
products_data = DataExtractor.extract_from_s3(s3_address, aws_credentials_path)

# Link and method to retrieve date_time details from S3 bucket
s3_url = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
date_details_data = extractor.download_s3_data(s3_url)




