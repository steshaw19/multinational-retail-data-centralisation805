import pandas as pd
import numpy as np
import re
from database_utils import DatabaseConnector
from data_extraction import DataExtractor, all_store_data, date_details_data, pdf_data, products_data, orders_data_df, user_data_df

class DataCleaning:
    """
    A class for cleaning various types of data.

    Attributes:
    - db_connector: An instance of the DatabaseConnector class.

    Methods:
    - clean_user_data(user_data_df: DataFrame): Clean user data.
    - clean_pdf_data(pdf_data: DataFrame): Clean PDF data.
    - clean_store_data(all_store_data: DataFrame): Clean store data.
    - convert_product_weights(products_data: DataFrame): Convert product weights to kilograms.
    - clean_products_data(products_data: DataFrame): Clean product data.
    - clean_orders_data(orders_data: DataFrame): Clean orders data.
    - clean_date_details_data(date_details_data): Clean date details data.
    """
    def __init__(self):
        self.db_connector = DatabaseConnector()
        self.destination_credentials = self.db_connector.read_destination_db_creds()
        self.destination_engine = self.db_connector.init_destination_db_engine(self.destination_credentials)
        self.extractor = DataExtractor()

    # Method for cleaning user data. Commented out code can be added as needed.
    def clean_user_data(self, user_data_df):
        try:
            if user_data_df is not None:
                user_data_df["country_code"] = user_data_df["country_code"].str.replace("GGB", "GB") # Fixes typo in country_code
                keep_values = ["GB", "DE", "US"] # Values to keep
                user_data_df = user_data_df[user_data_df["country_code"].isin(keep_values)] # Removes rows with incorrect information
                return user_data_df
        
        except Exception as e:
            print(f"Error cleaning user data: {e}")
            return None
        
    # Method for cleaning card details from PDF data. This is done in three parts. 1) removes ? from card_number 2) removes "NULL" values 3) removes non-numeric card_numbers
    def clean_pdf_data(self, pdf_data):
        try:
            if pdf_data is not None:
                pdf_data['card_number'] = pdf_data['card_number'].str.replace(r'\?', '', regex=True) # Drops '?' card numbers
                non_numeric_mask = ~pd.to_numeric(pdf_data['card_number'], errors='coerce').notna()
                pdf_data = pdf_data.loc[~non_numeric_mask] # Drops non-numeric values using mask from card numbers
                return pdf_data
        except Exception as e:
            print(f"Error cleaning card details data: {e}")
            return None
        
    # Method for cleaning store details data. Commented out code can be added as needed.    
    def clean_store_data(self, all_store_data):
        try:
            keep_values = ["GB", "DE", "US"] # Groups variables to keep
            all_store_data = all_store_data[all_store_data['country_code'].isin(keep_values)] # Drops rows which do not match criteria
            all_store_data["continent"] = all_store_data["continent"].str.replace("eeEurope", "Europe") # Corrects typos
            all_store_data["continent"] = all_store_data["continent"].str.replace("eeAmerica", "America") # Corrects typos
            return all_store_data
        except Exception as e:
            print(f"Error cleaning store details data: {e}")
            return None
        
    # Method for converting product weight data before cleaning products_data table.
    def convert_product_weights(self, products_data):
        def convert_to_kg(weight_str):
            try:
                if isinstance(weight_str, str): # Check if the value is a string
                    value, unit = re.match(r'(\d+\.?\d*)\s*([a-zA-Z]+)', weight_str).groups() # Extract numeric value and unit
                    if unit.lower() == 'g': # Convert units to kg
                        return float(value) / 1000
                    elif unit.lower() == 'ml':
                        return float(value) / 1000
                    else:
                        return float(value)
            except (AttributeError, ValueError):
                return None
            
        products_data['weight_kg'] = products_data['weight'].apply(convert_to_kg) # Apply conversion function to the 'weight' column
        products_data = products_data.drop(columns=['weight']) # Drop the original 'weight' column
        return products_data
    
    # Method for cleaning products data. First, drops all duplicate values. Then drops NaN values. Finally drops rows with non-numeric values based on EAN column.
    def clean_products_data(self, products_data):
        try:
            products_data = products_data.drop_duplicates() # Drops duplicated rows
            products_data = products_data.dropna() # Drops any null values
            non_numeric_mask = ~products_data['EAN'].str.isnumeric() # Checks for non-numeric characters in EAN
            products_data = products_data.drop(products_data[non_numeric_mask].index) # Drops non-numeric characters
            return products_data
        except Exception as e:
            print(f"Error cleaning products data: {e}")
            return None
        
    # Method for cleaning order data.    
    def clean_orders_data(self, orders_data):
        try:
            if orders_data is not None:
                columns_to_drop = ['first_name', 'last_name', '1'] # Groups columns to drop into variable
                orders_data = orders_data.drop(columns=columns_to_drop, errors='ignore') # Drops unneeded columns
                orders_data = orders_data.rename(columns={'level_0': 'index'}) # Renames index column
                orders_data = orders_data.set_index('index') # Sets index
                return orders_data
        except Exception as e:
            print(f"Error cleaning orders data: {e}")
            return None
        
    # Method to clean date details data (time when orders have been placed in the various stores)
    def clean_date_details_data(self, date_details_data):
        try:
            date_details_data_df = pd.DataFrame(date_details_data) # Converts json to dataframe
            date_details_data_df.reset_index(drop=True, inplace=True) # Set the index to default (integer index)
            keep_values = ['Morning', 'Evening', "Midday", "Late_Hours"] # Groups values to keep into a single variable
            date_details_data_df = date_details_data_df[date_details_data_df['time_period'].isin(keep_values)] # Drops rows with incorrect data
            return date_details_data_df
        except Exception as e:
            print(f"Error cleaning date details data: {e}")
            return None

if __name__=='__main__': 
    data_cleaner = DataCleaning()
    extractor = DataExtractor()
    db_connector = DatabaseConnector()

    # Calling methods to clean extracted data.
    cleaned_user_data = data_cleaner.clean_user_data(user_data_df)
    cleaned_pdf_data = data_cleaner.clean_pdf_data(pdf_data)
    cleaned_store_data = data_cleaner.clean_store_data(all_store_data)
    converted_products_data = data_cleaner.convert_product_weights(products_data) # Convert product weights
    cleaned_product_data = data_cleaner.clean_products_data(converted_products_data) # Then clean the dataframe with the converted weight column
    cleaned_orders_data = data_cleaner.clean_orders_data(orders_data_df)
    cleaned_date_details_data = data_cleaner.clean_date_details_data(date_details_data)

    # Sends cleaned data to database.    
    try:
       # Call upload_to_db method from db_connector instance
       if cleaned_user_data is not None:
           db_connector.upload_to_db(cleaned_user_data, 'dim_users')
    except:
       print("Data cleaning and upload failed for User Data.")

    try:
        # Call upload_to_db method from db_connector instance
        if cleaned_pdf_data is not None:
            db_connector = DatabaseConnector()
            db_connector.upload_to_db(cleaned_pdf_data, 'dim_card_details')
    except:
        print("Data cleaning and upload failed for card details PDF.")
    
    try:
        # Call upload_to_db method from db_connector instance
        if cleaned_store_data is not None:
            db_connector.upload_to_db(cleaned_store_data, 'dim_store_details')
    except:
        print("Data cleaning and upload failed for API Store Data.")

    try:
        # Call upload_to_db method from db_connector instance
        if cleaned_product_data is not None:
            db_connector.upload_to_db(cleaned_product_data, 'dim_products')
    except:
        print("Data cleaning and upload failed for product data.")

    try:
        if cleaned_orders_data is not None:
            db_connector = DatabaseConnector()
            db_connector.upload_to_db(cleaned_orders_data, 'orders_table')
    except Exception as e:
        print(f"Data cleaning and upload failed for orders data: {e}")

    try:
        if cleaned_date_details_data is not None:
            db_connector = DatabaseConnector()
            db_connector.upload_to_db(cleaned_date_details_data, 'dim_date_times')
    except Exception as e:
        print(f"Data cleaning and upload failed for date_details data: {e}")