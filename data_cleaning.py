import pandas as pd
import numpy as np
from data_extraction import user_data_df
from database_utils import DatabaseConnector
from data_extraction import DataExtractor

# Instantiate DatabaseConnector to access its methods
db_connector = DatabaseConnector()

# Get credentials
credentials = db_connector.read_db_creds()

# Initialize the database engine
engine = db_connector.init_db_engine(credentials)

# Create an instance of DataExtractor
extractor = DataExtractor()
user_data_df = extractor.read_rds_table('legacy_users')


class DataCleaning:
    def clean_user_data(self, user_data_df):
        try:
            # Replace 'NULL' with NaN
            user_data_df.replace({'NULL': np.nan}, inplace=True)

            # Drop rows with any NULL value in any column
            user_data_df = user_data_df.dropna()

            # Filter rows where the user ID has the desired length
            user_data_df = user_data_df[user_data_df['user_uuid'].str.len() == 36]

            # Drop any names that contain numbers but checks if the name is NULL first
            user_data_df = user_data_df[user_data_df[['first_name', 'last_name']].notnull().all(axis=1) &
                            user_data_df[['first_name', 'last_name']].applymap(lambda x: x.isalpha()).all(axis=1)]

            # Removes email address that are invalid (does not have an @ sign)
            mask = user_data_df['email_address'].str.contains('@', na=False)
            user_data_df = user_data_df[mask]

            # Convert date columns to datetime format
            date_columns = ['date_of_birth', 'join_date']
            user_data_df[date_columns] = user_data_df[date_columns].apply(pd.to_datetime, errors='coerce')

            # Create a boolean mask for rows with numbers in the 'country' column
            no_number_mask_country = ~user_data_df['country'].str.contains(r'\d', na=False)

            # Filter the DataFrame using the boolean mask
            user_data_df = user_data_df[no_number_mask_country]

            # Create a boolean mask for rows with numbers in the 'column' column
            no_number_mask_company = ~user_data_df['company'].str.contains(r'\d', na=False)

            # Filter the DataFrame using the boolean mask
            user_data_df = user_data_df[no_number_mask_company]

            # Create a boolean mask for rows with valid country codes (2 or 3 characters)
            valid_country_code_mask = user_data_df['country_code'].str.len().isin([2, 3])

            # Filter the DataFrame using the boolean mask
            user_data_df = user_data_df[valid_country_code_mask]

            # # Create a boolean mask for rows with phone numbers containing letters (excluding 'ext')
            # valid_phone_mask = ~user_data_df['phone_number'].str.contains(r'[^0-9extEXT()+.-'']', na=False)

            # # Filter the DataFrame using the boolean mask
            # user_data_df = user_data_df[valid_phone_mask]

            return user_data_df
        
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return None

if __name__=='__main__': 
    data_cleaner = DataCleaning()
    cleaned_data = data_cleaner.clean_user_data(user_data_df)
    
    try:
        # Call upload_to_db method from db_connector instance
        db_connector.upload_to_db(cleaned_data, 'dim_users')
    except:
        print("Data cleaning and upload failed.")

    
            # Find duplicates based off unique user id            
            # This indicated that the NULL values were the only duplicates and could be removed.
            # duplicate_rows_subset = user_data_df[user_data_df.duplicated(subset=['user_uuid'])]

                 


