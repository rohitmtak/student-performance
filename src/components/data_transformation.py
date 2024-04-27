# import necassary modules
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.utils import save_object
from src.exception import CustomException
from src.logger import logging
import os

@dataclass
class DataTransformationConfig:
    # define default file path for preprocessor object and create pickle file
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        # initialize with default configuration
        self.data_transformation_config = DataTransformationConfig()

    # method to create and return data transformer object
    def get_data_transformer_object(self):
        try:
            # define numerical and categorical columns
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            # define pipeline for numerical features
            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy='median')),
                ("scaler", StandardScaler())
            ])

            # define pipeline for categorical features
            cat_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy='most_frequent')),
                ("one_hot_encoder", OneHotEncoder()),
                ("scaler", StandardScaler(with_mean=False))
            ])

            # log column information
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # create ColumnTransformer to apply different preprocessing steps to different columns
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipline", cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor

        except Exception as e:
            # raise custom exception if an error occurs
            raise CustomException(e, sys)

    # method to initiate data transformation process
    def initiate_data_transformation(self, train_path, test_path):
        try:
            # read train and test data from CSV files
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading the train and test file")

            # obtain the data transformer object
            preprocessing_obj = self.get_data_transformer_object()

            # define target column name and numerical columns
            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            # divide the train dataset into independent and dependent features
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            # divide the test dataset into independent and dependent features
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying Preprocessing on train and test dataframe")

            # apply preprocessing to training and test dataframes
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # combine input features with target features for training and test data
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object")

            # save preprocessing object
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(sys, e)