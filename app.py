from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_ingestion import DataIngestionConfig
import sys


if __name__=="__main__":
    logging.info("Execution started")
    
    try:
        data_ingestion = DataIngestion()
        data_ingestion.initiate_data_ingestion()
        
        
    except Exception as e:
        logging.info("Custom Exception")
        raise CustomException(e,sys)
