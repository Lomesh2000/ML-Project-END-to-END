import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

from project.logger import logging
from project.exception import CustomException

from project.entity.artifact_entity import DataIngestionArtifacts
from project.entity.config_entity import DataIngestionConfig

from project.data_access.convert_mongo_dict_to_df import DataFrameFromMongoDB

class DataIngestion:
    
    def __init__(self, data_ingestion_config=DataIngestionConfig()) -> None:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
        return data frame 
        saves data as csv file in feature store
        """
        try:
            logging.info('Exporting data from mongodb')
            data_from_mongo = DataFrameFromMongoDB()
            dataframe = data_from_mongo.export_collection_as_data_frame(collection_name=
                                                                        self.data_ingestion_config.collection_name)

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path)
            logging.info('saved csv data file in feature store') 
            return dataframe
        except Exception as e:
            raise CustomException(e, sys)

    def split_data_train_test(self, dataframe: pd.DataFrame) -> None:
        """
        split data frame into train and test data and save it in feature store
        """    
        try:
            train_set, test_set = train_test_split(dataframe, test_size=DataIngestionConfig.train_test_split_ratio, random_state=42)
            logging.info('splitted data into train test set')
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)    
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info('splitted and exported data into train and test data')

        except Exception as e:
            raise CustomException(e, sys) 

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        """
        intitated data ingestion components process in training pipeline

        return train and test set as the artifacts of data ingestion components
        """       
        logging.info('Initiating data ingestion')

        try:
            dataframe = self.export_data_into_feature_store()
            logging.info('data imported from mongodb')

            self.split_data_train_test(dataframe=dataframe)
            logging.info('train and test set saved')

            data_ingestion_artifact = DataIngestionArtifacts(trained_file_path=self.data_ingestion_config.training_file_path,
                                                             test_file_path=self.data_ingestion_config.test_file_path)
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomException(e, sys) from e
        
    
            