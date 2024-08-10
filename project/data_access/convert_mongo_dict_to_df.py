from project.configuration.mongodb_connection import MongoDBClient
from project.constants import DB_NAME
from project.logger import logging
from project.exception import CustomException
import sys
import pandas as pd
import numpy as np
from typing import Optional

class DataFrameFromMongoDB:
    """
    this class convert data from mongo db into dataframe from dict 
    """

    def __init__(self) -> None:
        try:
            self.mongo_client = MongoDBClient(database_name=DB_NAME)
        except Exception as e:
            raise CustomException(e, sys)

    def export_collection_as_data_frame(self, collection_name: str, database_name:Optional[str] = None) -> pd.DataFrame:
        retry = 0
        while retry < 5:
            try:
                if not database_name:
                    collection = self.mongo_client.database[collection_name]
                else:
                    collection = self.mongo_client[database_name][collection_name]

                df = pd.DataFrame(list(collection.find()))
                if '_id' in df.columns:
                    df.drop(columns=['_id'], axis=1, inplace=True)
                df.replace({'na':np.nan}, inplace=True)
                logging.info(f'collection from database : {database_name} is converted to DATA FRAME')    
                return df   
            except Exception as e:
                if retry == 5:
                    raise CustomException(e, sys)
                continue
        