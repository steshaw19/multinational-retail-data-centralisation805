import pandas as pd
from sqlalchemy import inspect
from database_utils import DatabaseConnector

# Instantiate DatabaseConnector to access its methods
db_connector = DatabaseConnector()

# Get credentials
credentials = db_connector.read_db_creds()

# Initialize the database engine
engine = db_connector.init_db_engine(credentials)

class DataExtractor:
    def read_rds_table(self, db_connector, engine, table_name):
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, engine, index_col='index')
            return df
        except Exception as e:
            print(f"Error reading table {table_name}: {e}")
            return None

    def list_db_tables(self, engine):
        try:
            # Use the inspector to get table names
            inspector = inspect(engine)
            table_names = inspector.get_table_names()

            return table_names
        except Exception as e:
            print(f"Error listing tables: {e}")
            return None

if __name__== '__main__':
    # Create an instance of DataExtractor
    extractor = DataExtractor()

    # Call the list_db_tables method
    tables = extractor.list_db_tables(engine)
    print(f"TABLES: {tables}")

    user_data_df = extractor.read_rds_table(db_connector, engine, 'legacy_users')
    print("User Data DataFrame:")
    print(user_data_df)