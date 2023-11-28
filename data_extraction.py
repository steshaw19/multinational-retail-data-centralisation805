import pandas as pd
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

# Instantiate DataExtractor to access its methods
extractor = DataExtractor()

# Read data from the RDS table (example table name: 'legacy_users')
user_data_df = extractor.read_rds_table('legacy_users')