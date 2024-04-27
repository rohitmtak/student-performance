#import necessary modules
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dotenv import load_dotenv
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
        logging.info("Connection Established", mydb)
        df=pd.read_sql_query('Select * from students', mydb)
        print(df.head())

        return df

    except Exception as ex:
        raise CustomException(ex)
    
    
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path) #get the directory path from the file path
        
        os.makedirs(dir_path, exist_ok=True) # create directory if it doesn't exist

        with open(file_path, "wb") as file_obj: # serialize and save the object to a fill
            pickle.dump(obj, file_obj)
        
    except Exception as e:
        raise CustomException(e, sys)
    
