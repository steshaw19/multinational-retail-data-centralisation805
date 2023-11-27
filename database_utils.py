import yaml
from sqlalchemy import create_engine

class DatabaseConnector:
    def read_db_creds(self, file_path='db_creds.yaml'):
        with open(file_path, 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials
    
    ## Now create a method init_db_engine which will read the credentials from the 
    ## return of read_db_creds and initialise and return an sqlalchemy database engine.
    
    def init_db_engine(self, credentials=None):
        if credentials is None:
            credentials = self.read_db_creds()
        db_url = f"postgresql+psycopg2://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}"
        engine = create_engine(db_url, isolation_level="READ COMMITTED")
        self.engine = engine  # Save of the engine as an instance variable for later use
        return engine
    
    def upload_to_db(self, df, table_name, if_exists='replace'):
        try:
            from data_cleaning import DataCleaning  # Move inside method to stop circular dependency between this file and data_cleaning.py
            df_cleaned = DataCleaning().clean_user_data(df)
            df_cleaned.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            print(f"Data uploaded to {table_name} successfully.")
        except Exception as e:
            print(f"Error uploading data to {table_name}: {e}")   
    
if __name__ == '__main__':
    db_connector = DatabaseConnector()
    credentials = db_connector.read_db_creds()

    try:
        # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
        engine = db_connector.init_db_engine(credentials)
        print(f"Connection to the {credentials['RDS_HOST']} for user {credentials['RDS_USER']} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)