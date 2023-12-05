import pandas as pd
import tabula
from sqlalchemy import inspect
from database_utils import DatabaseConnector

class DataExtractor:
    def __init__(self):
        # Instantiate DatabaseConnector to access its methods
        self.db_connector = DatabaseConnector()
        # Get credentials
        self.credentials = self.db_connector.read_source_db_creds()
        # Initialize the database engine
        self.source_engine = self.db_connector.init_source_db_engine(self.credentials)

    def read_rds_table(self, table_name):
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, self.source_engine, index_col='index')
            return df
        except Exception as e:
            print(f"Error reading table {table_name}: {e}")
            return None

    def list_db_tables(self):
        try:
            # Use the inspector to get table names
            inspector = inspect(self.source_engine)
            table_names = inspector.get_table_names()
            return table_names
        except Exception as e:
            print(f"Error listing tables: {e}")
            return None
        
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

# Create an instance of the DataExtractor class
extractor = DataExtractor()

# Read data from the RDS table (example table name: 'legacy_users')
user_data_df = extractor.read_rds_table('legacy_users')

# Provide the PDF link as an argument to the retrieve_pdf_data method
pdf_data = extractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
