import pandas as pd
import numpy as np
import re
from database_utils import DatabaseConnector
from data_extraction import DataExtractor, all_store_data, date_details_data, pdf_data, products_data  

# Instantiate DatabaseConnector to access its methods
db_connector = DatabaseConnector()

# Get credentials
destination_credentials = db_connector.read_destination_db_creds()

# Initialize the database engine
destination_engine = db_connector.init_destination_db_engine(destination_credentials)

# Create an instance of DataExtractor
extractor = DataExtractor()

# Read data from the RDS table (example table name: 'legacy_users')
user_data_df = extractor.read_rds_table('legacy_users')

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
    def clean_user_data(self, user_data_df):
        try:
            if user_data_df is not None:
                # Replace 'NULL' with NaN
                user_data_df.replace({'NULL': np.nan}, inplace=True)

                # Drop rows with any NULL value in any column
                user_data_df = user_data_df.dropna()

                # Filter rows where the user ID has the desired length
                user_data_df = user_data_df[user_data_df['user_uuid'].str.len() == 36]

                 # Drop any names that contain numbers but check if the name is NULL first
                name_columns = ['first_name', 'last_name']
                user_data_df = user_data_df[user_data_df[name_columns].notnull().all(axis=1) &
                            user_data_df[name_columns].applymap(lambda x: bool(re.match(r'^[a-zA-Z\'-]+$', str(x))))]

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

                # Create a boolean mask for rows with numbers in the 'company' column
                no_number_mask_company = ~user_data_df['company'].str.contains(r'\d', na=False)

                # Filter the DataFrame using the boolean mask
                user_data_df = user_data_df[no_number_mask_company]

                # Create a boolean mask for rows with valid country codes (2 or 3 characters)
                valid_country_code_mask = user_data_df['country_code'].str.len().isin([2, 3])

                # Filter the DataFrame using the boolean mask
                user_data_df = user_data_df[valid_country_code_mask]

                # Create a boolean mask for rows with phone numbers containing letters (excluding 'ext')
                # valid_phone_mask = ~user_data_df['phone_number'].str.contains(r'[^0-9extEXT()+.-'']', na=False)

                # Filter the DataFrame using the boolean mask
                # user_data_df = user_data_df[valid_phone_mask]

            return user_data_df
        
        except Exception as e:
            print(f"Error cleaning user data: {e}")
            return None
    
    def clean_pdf_data(self, pdf_data):
        try:
            if pdf_data is not None:
                # Replace 'NULL' with NaN
                pdf_data.replace({'NULL': np.nan}, inplace=True)

                # Drop rows with any NULL value in any column
                pdf_data = pdf_data.dropna()

                # Convert 'card_number' to numeric, and drop rows where conversion is not possible
                pdf_data.loc[:, 'card_number'] = pd.to_numeric(pdf_data['card_number'], errors='coerce').round().astype('Int64')
                pdf_data = pdf_data.dropna(subset=['card_number'])

                # Include only 'card_number' values with a length between 8 and 19 (length taken from online research)
                pdf_data = pdf_data[pdf_data['card_number'].astype(str).apply(len).between(8, 19)]

                # Makes data_payment_confirmed date time values (excluding expiry date as this has a specific format)
                date_columns = ['date_payment_confirmed']
                pdf_data[date_columns] = pdf_data[date_columns].apply(pd.to_datetime, errors='coerce')
                
                return pdf_data
                
        except Exception as e:
            print(f"Error cleaning card details data: {e}")
            return None
        
    def clean_store_data(self, all_store_data):
        try:
            # Replace 'NULL' (case insensitive) with NaN
            all_store_data.replace({'NULL': np.nan, 'null': np.nan, 'NULL ': np.nan, ' NULL': np.nan}, inplace=True)

            # Drop the 'lat' column as all data is none.
            all_store_data = all_store_data.drop('lat', axis=1)

            # Convert 'staff_numbers' column to numeric, coerce non-numeric values to NaN
            all_store_data['staff_numbers'] = pd.to_numeric(all_store_data['staff_numbers'], errors='coerce')

            # Convert 'opening_date' column to datetime
            all_store_data['opening_date'] = pd.to_datetime(all_store_data['opening_date'], errors='coerce')
            
            # Specify columns where NaN values should be kept
            columns_to_keep_nan = ['latitude']

            # Create a boolean mask for rows with valid country codes (2 or 3 characters)
            valid_country_code_mask = all_store_data['country_code'].str.len().isin([2, 3])

            # Filter the DataFrame using the boolean mask
            all_store_data = all_store_data[valid_country_code_mask]

            # Create a boolean mask for rows with numbers in the 'continent' column
            no_number_mask_continent = ~all_store_data['continent'].str.contains(r'\d', na=False)

            # Filter the DataFrame using the boolean mask
            all_store_data = all_store_data[no_number_mask_continent]

            # Drop rows with NaN values from all columns except 'latitude'
            # Keep rows where 'store_type' is 'web portal' or has at least two non-NaN values
            all_store_data = all_store_data[(all_store_data['store_type'] == 'web portal') | (all_store_data.notna().sum(axis=1) >= 2)]
            all_store_data = all_store_data.dropna(subset=all_store_data.columns.difference(columns_to_keep_nan))
        
            return all_store_data
                
        except Exception as e:
            print(f"Error cleaning store details data: {e}")
            return None
    
    def convert_product_weights(self, products_data):
        def convert_to_kg(weight_str):
            try:
                # Check if the value is a string
                if isinstance(weight_str, str):
                    # Extract numeric value and unit
                    value, unit = re.match(r'(\d+\.?\d*)\s*([a-zA-Z]+)', weight_str).groups()
                    # Convert units to kg
                    if unit.lower() == 'g':
                        return float(value) / 1000
                    elif unit.lower() == 'ml':
                        return float(value) / 1000
                    else:
                        return float(value)
            except (AttributeError, ValueError):
                # Handle cases where the regex match or conversion fails
                return None

        # Apply conversion function to the 'weight' column
        products_data['weight_kg'] = products_data['weight'].apply(convert_to_kg)

        # Drop the original 'weight' column
        products_data = products_data.drop(columns=['weight'])

        return products_data
    
    def clean_products_data(self, products_data):
        try:
            # Replace 'NULL' (case insensitive) with NaN
            products_data.replace({'NULL': np.nan, 'null': np.nan, 'NULL ': np.nan, ' NULL': np.nan}, inplace=True)

            # Define a regular expression pattern for a valid UUID
            uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'

            # Filter out rows with invalid UUIDs
            products_data = products_data[products_data['uuid'].str.match(uuid_pattern, na=False)]

            # Convert date_added to datetime
            products_data.loc[:, 'date_added'] = pd.to_datetime(products_data['date_added'], errors='coerce')

            # Drop Nan values in any column
            products_data = products_data.dropna()

            return products_data
        
        except Exception as e:
            print(f"Error cleaning products data: {e}")
            return None
        
    def clean_orders_data(self, orders_data):
        try:
            if orders_data is not None:
                # Drop unwanted columns if they exist
                columns_to_drop = ['first_name', 'last_name', '1']
                orders_data = orders_data.drop(columns=columns_to_drop, errors='ignore')

                # Sets index
                orders_data = orders_data.rename(columns={'level_0': 'index'})
                orders_data = orders_data.set_index('index')

                # Define a regular expression pattern for a valid UUID
                # orders_data = orders_data.rename(columns={'uuid': 'date_uuid'})
                # uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
                # uuid_columns = ['date_uuid', 'user_uuid']

                # Drop rows where the length of 'user_uuid' or 'uuid' is not equal to 36
                orders_data = orders_data[orders_data['user_uuid'].str.len() == 36]
                orders_data = orders_data[orders_data['date_uuid'].str.len() == 36]

                # Filter out rows with invalid UUIDs and renames the 'date_uuid' column to uuid like in other tables.
                # orders_data = orders_data[orders_data[uuid_columns].str.match(uuid_pattern, na=False)]

                # Drop Nan values in any column
                orders_data = orders_data.dropna()

                return orders_data
        except Exception as e:
            print(f"Error cleaning orders data: {e}")
            return None
        
    # Function to clean date details data
    def clean_date_details_data(self, date_details_data):
        try:
            # Convert JSON to DataFrame
            date_details_data_df = pd.DataFrame(date_details_data)

            # Set the index to default (integer index)
            date_details_data_df.reset_index(drop=True, inplace=True)

            # Convert the 'timestamp' column to datetime type
            date_details_data_df['timestamp'] = pd.to_datetime(date_details_data_df['timestamp'], errors='coerce')

            # Remove rows with null values
            date_details_data_df = date_details_data_df.dropna()

            return date_details_data_df
    
        except Exception as e:
            print(f"Error cleaning date details data: {e}")
            return None

if __name__=='__main__': 
    data_cleaner = DataCleaning()
    extractor = DataExtractor()
    # cleaned_user_data = data_cleaner.clean_user_data(user_data_df)
    # cleaned_pdf_data = data_cleaner.clean_pdf_data(pdf_data)
    # cleaned_store_data = data_cleaner.clean_store_data(all_store_data)
    
    # Convert product weights
    converted_products_data = data_cleaner.convert_product_weights(products_data)
    # Then clean the dataframe with the converted weight column
    cleaned_product_data = data_cleaner.clean_products_data(converted_products_data)
    
    
    # try:
    #    # Call upload_to_db method from db_connector instance
    #    if cleaned_user_data is not None:
    #        db_connector.upload_to_db(cleaned_user_data, 'dim_users')
    # except:
    #    print("Data cleaning and upload failed for User Data.")

    # try:
    #     # Call upload_to_db method from db_connector instance
    #     if cleaned_pdf_data is not None:
    #         db_connector.upload_to_db(cleaned_pdf_data, 'dim_card_details')
    # except:
    #     print("Data cleaning and upload failed for PDF.")
    
    # try:
    #     # Call upload_to_db method from db_connector instance
    #     if cleaned_store_data is not None:
    #         db_connector.upload_to_db(cleaned_store_data, 'dim_store_details')
    # except:
    #     print("Data cleaning and upload failed for API Store Data.")

    try:
        # Call upload_to_db method from db_connector instance
        if cleaned_product_data is not None:
            db_connector.upload_to_db(cleaned_product_data, 'dim_products')
    except:
        print("Data cleaning and upload failed for product data.")

    # # Retrieves the names of all the tables in the database 
    # all_tables = extractor.list_db_tables()
    # print("All Tables in the Database:")
    # print(all_tables)

    # # Extract orders data
    # orders_table_name = 'orders_table'
    # orders_data = extractor.read_rds_table(orders_table_name)
    # print(orders_data)

    # # Clean orders data
    # cleaned_orders_data = data_cleaner.clean_orders_data(orders_data)
    # print(cleaned_orders_data)

    # try:
    #     if cleaned_orders_data is not None:
    #         db_connector = DatabaseConnector()
    #         db_connector.upload_to_db(cleaned_orders_data, 'orders_table')
    # except Exception as e:
    #     print(f"Data cleaning and upload failed for orders data: {e}")

    # # Clean date_details order data
    # cleaned_date_details_data = data_cleaner.clean_date_details_data(date_details_data)
    # print(cleaned_date_details_data)

    # try:
    #     if cleaned_date_details_data is not None:
    #         db_connector = DatabaseConnector()
    #         db_connector.upload_to_db(cleaned_date_details_data, 'dim_date_times')
    # except Exception as e:
    #     print(f"Data cleaning and upload failed for date_details data: {e}")