# import necessary modules
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_ingestion import DataIngestionConfig
from src.components.data_transformation import DataTransformationConfig, DataTransformation
from src.components.model_trainer import ModelTrainerConfig, ModelTrainer

import sys # import the sys module for system-specific parameters and functions

if __name__=="__main__":
    logging.info("Execution started")
    
    try:
        data_ingestion = DataIngestion()
        # initiate data ingestion process and get paths for training and test data
        train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
        
        data_transformation = DataTransformation()
        # initiate data transformation process
        train_arr, test_arr, preprocessor_obj_file_path = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
        
        # model training
        model_trainer = ModelTrainer()
        print(model_trainer.initiate_model_trainer(train_arr, test_arr))  
                
    except Exception as e:
        logging.info("Custom Exception")
        raise CustomException(e,sys)