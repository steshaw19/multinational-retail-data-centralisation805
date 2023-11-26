from sqlalchemy import inspect
from database_utils import DatabaseConnector

class DataExtractor:
    def list_db_tables(self):
        try:
            # Instantiate DatabaseConnector to access its methods
            db_connector = DatabaseConnector()

            # Get credentials
            credentials = db_connector.read_db_creds()

            # Initialize the database engine
            engine = db_connector.init_db_engine(credentials)

            # Use the inspector to get table names
            inspector = inspect(engine)
            table_names = inspector.get_table_names()

            return table_names
        except Exception as e:
            print(f"Error listing tables: {e}")
            return None

# Create an instance of DataExtractor
extractor = DataExtractor()

# Call the list_db_tables method
tables = extractor.list_db_tables()
print(tables)