import yaml
from sqlalchemy import create_engine

class DatabaseConnector:
    def __init__(self):
        # Initialize both source and destination engines in the constructor
        self.source_engine = self.init_source_db_engine()
        self.destination_engine = self.init_destination_db_engine()
        
    def read_source_db_creds(self, file_path='db_creds.yaml'):
        with open(file_path, 'r') as file:
            source_credentials = yaml.safe_load(file)
        return source_credentials
    
    def read_destination_db_creds(self, file_path='sales_data_creds.yaml'):
        with open(file_path, 'r') as file:
            destination_credentials = yaml.safe_load(file)
        return destination_credentials
    
    def init_source_db_engine(self, credentials=None):
        if credentials is None:
            credentials = self.read_source_db_creds()
        db_url = f"postgresql+psycopg2://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}"
        self.source_engine = create_engine(db_url)
        return self.source_engine
    
    def init_destination_db_engine(self, credentials=None):
        if credentials is None:
            credentials = self.read_destination_db_creds()
        db_url = f"postgresql+psycopg2://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}"
        self.destination_engine = create_engine(db_url)
        return self.destination_engine
    
    def upload_to_db(self, df, table_name, if_exists='replace'):
        try:
            df.to_sql(table_name, self.destination_engine, if_exists=if_exists, index=False)
            print(f"Data uploaded to {table_name} successfully.")
        except Exception as e:
            print(f"Error uploading data to {table_name}: {e}")
    
if __name__ == '__main__':
    db_connector = DatabaseConnector()
    source_credentials = db_connector.read_source_db_creds()
    destination_credentials = db_connector.read_destination_db_creds()

    try:
        source_engine = db_connector.init_source_db_engine(source_credentials)
        print(f"Connection to the {source_credentials['RDS_HOST']} for user {source_credentials['RDS_USER']} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

    try:
        destination_engine = db_connector.init_destination_db_engine(destination_credentials)
        print(f"Connection to the {destination_credentials['RDS_HOST']} for user {destination_credentials['RDS_USER']} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)