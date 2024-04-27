# import necessary modules
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_ingestion import DataIngestionConfig
from src.components.data_transformation import DataTransformationConfig, DataTransformation

import sys # import the sys module for system-specific parameters and functions


if __name__=="__main__":
    logging.info("The execution has started")
    
    try:
        data_ingestion = DataIngestion()
        # initiate data ingestion process and get paths for training and test data
        train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
        
        data_transformation=DataTransformation()
         # initiate data transformation process
        data_transformation.initiate_data_transformation(train_data_path, test_data_path)
        
    except Exception as e:
        logging.info("Custom Exception")
        raise CustomException(e, sys)
