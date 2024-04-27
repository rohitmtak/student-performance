#import necessary modules
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import pymysql # for MySQL database connection

import pickle
import numpy as np

load_dotenv()  # load environment variables from .env file

# MySQL database connection details from environment variables
host=os.getenv("host")
user=os.getenv("user")
password=os.getenv("password")
db=os.getenv('db')


def read_sql_data():
    logging.info("Reading SQL database started")
    try:
        mydb=pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )
        logging.info("Connection Established",mydb)
        df=pd.read_sql_query('Select * from students',mydb)
        print(df.head())

        return df

    except Exception as ex:
        raise CustomException(ex)
    
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path) #get the directory path from the file path
        
        os.makedirs(dir_path, exist_ok=True) # create directory if it doesn't exist

        with open(file_path, "wb") as file_obj: # serialize and save the object to a fil
            pickle.dump(obj, file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {} # dictionary to store model evaluation scores

        for i in range(len(list(models))):
            model = list(models.values())[i]
            model_params=param[list(models.keys())[i]]
            
            # perform grid search to find the best hyperparameters using cross-validation
            gs = GridSearchCV(model, model_params, cv=3)
            gs.fit(X_train, y_train)
            
            # set the model's parameters to the best found and train the model
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    
    except Exception as e:
        raise CustomException(e,sys)