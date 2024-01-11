import os
import sys
import pandas as pd
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging

import warnings
warnings.filterwarnings('ignore')
import pyodbc

@dataclass
class DataIngestionConfig():
    books_data_path: str = os.path.join("artifacts", "books_data.csv")
    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")

class DataIngestion():
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Starting data ingestion")
        try:
            # Replace with your SQL Server details
            server = 'NAGESH\\SQLEXPRESS'
            database = 'ML_Projects_db'
            username = 'sa'
            password = 'nagesh@sharvan'

            # Connect to SQL Server
            connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'
            connection = pyodbc.connect(connection_string)

            # Execute SQL Query
            query = 'SELECT * FROM books_data'
            data = pd.read_sql(query, connection)

            # copy the data from original data
            df = data.copy()

             # Save the raw-data
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False)

            # Drop unnecessary column 'Height'
            df.drop('Height', axis=1, inplace=True)

            # Drop rows with missing values
            df.dropna(inplace=True)

            # Combine relevant text columns into a single 'tags' column
            df['tags'] = df['Author'] + ' ' + df['Genre'] + ' ' + df['SubGenre'] + ' ' + df['Publisher']

            # Convert 'tags' to lowercase
            df['tags'] = df['tags'].apply(lambda x: x.lower())

            # Save the data
            os.makedirs(os.path.dirname(self.ingestion_config.books_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.books_data_path, index=False)


            logging.info("Data ingestion is completed")

            return (
                self.ingestion_config.raw_data_path,
                self.ingestion_config.books_data_path
            )

        except Exception as e:
            logging.error("Exception occurred in data ingestion")
            raise CustomException(e, sys)

if __name__ == '__main__':
    obj = DataIngestion()
    raw_data_path, books_data_path = obj.initiate_data_ingestion()
