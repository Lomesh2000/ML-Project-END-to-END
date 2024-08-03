# file to connect mongo db 
import sys
import os
from project.exception import CustomException
from project.logger import logging

from project.constants import DB_NAME 
from dotenv import load_dotenv
import pymongo
# import certifi
# ca = certifi.where()

load_dotenv()

class MongoDBClient:
    """
    Class Name :   export_data_into_feature_store
    Description :   This method exports the dataframe from mongodb feature store as dataframe 
    
    Output      :   connection to mongodb database
    On Failure  :   raises an exception
    """
    client = None

    def __init__(self, database_name=DB_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv('CONNECTION_URL')
                if mongo_db_url is None:
                    raise Exception(f'environment key CONNECTION URL not set')
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
            self.client = MongoDBClient.client    
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info('MongoDB connection successfull')
        except Exception as e:
            raise CustomException(e, sys)
