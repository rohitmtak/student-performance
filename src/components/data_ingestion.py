#import necessary modules
import os  # import the os module for operating system functionality
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from src.utils import read_sql_data

from sklearn.model_selection import train_test_split
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifacts', 'train.csv')
    test_data_path:str=os.path.join('artifacts', 'test.csv')
    raw_data_path:str=os.path.join('artifacts', 'raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            # read raw data from MySql
            df=pd.read_csv(os.path.join('notebook/data', 'raw.csv'))
            logging.info("Reading completed mysql database")

            # save raw data to a file
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            
            # split data into train and test sets
            train_set,test_set=train_test_split(df,test_size=0.2, random_state=42)
            
            # save train and test sets to a separate files
            train_set.to_csv(self.ingestion_config.train_data_path,index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False, header=True)

            logging.info("Data ingestion is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            logging.info("Exception occured while ingesting data")
            raise CustomException(e,sys)