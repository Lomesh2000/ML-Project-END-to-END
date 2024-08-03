import os
import sys
import json
import pandas as pd
from pandas import DataFrame

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import *

from project.entity.config_entity import DataValidationConfig
from project.entity.artifact_entity import DataValidationArtifacts, DataIngestionArtifacts

from project.utils.main_utils import write_yaml_file
from project.exception import CustomException
from project.logger import logging
from project.constants import SCHEMA_PATH

from project.utils.main_utils import read_yaml_file

class DataValidation:

    def __init__(self, data_ingestion_artifact: DataIngestionArtifacts, 
                 data_validation_config: DataValidationConfig) -> None:
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(file_path=SCHEMA_PATH)
        except Exception as e:
            raise CustomException(e, sys) from e

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self.schema_config['columns'])
            logging.info('no of columns are matching')
        except Exception as e:
            raise CustomException(e, sys) from e      

    def is_column_exist(self, dataframe: DataFrame):
        try:
            expected_columns = dataframe.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            for col in self.schema_config['numerical_columns']:
                if col not in expected_columns:
                    missing_numerical_columns.append(col)
                    
            if missing_numerical_columns:
                logging.info(f'missing numerica columns : {missing_numerical_columns}')

            for col in self.schema_config['categorical_columns']:
                if col not in expected_columns:
                    missing_categorical_columns.append(col)    

            if missing_categorical_columns:
                logging.info(f'missing numerica columns : {missing_categorical_columns}')         

            return False if missing_numerical_columns or missing_categorical_columns else True
            
        except Exception as e:
            raise CustomException(e, sys)    
    
    def detect_dataset_drift(self, reference_dataframe: DataFrame, current_dataframe: DataFrame):
        try:
            report = Report(metrics=[
                DataDriftPreset(),
            ])
            report.run(reference_data=reference_dataframe, current_data=current_dataframe)
            json_report = report.json()
            json_report = json.loads(json_report)
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, 
                            content=json_report)

            n_features = json_report['metrics'][0]['result']['number_of_columns']
            n_drifted_features = json_report['metrics'][0]['result']['number_of_drifted_columns']
            logging.info(f'{n_drifted_features/n_features} drift detected')
            drift_status = json_report['metrics'][0]['result']['dataset_drift']
            return drift_status
        except Exception as e:
            raise CustomException(e, sys) 


    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            validaton_error_messages = []
            logging.info('starting data validation')
            train_df, test_df = (pd.read_csv(self.data_ingestion_artifact.trained_file_path),
                                 pd.read_csv(self.data_ingestion_artifact.test_file_path))

            status = self.validate_number_of_columns(train_df)
            if not status:
                logging.info('columns missing in training set')
                validaton_error_messages.append('columns missing in training set')
            else:
                logging.info('validation done for training set columns')

            status = self.validate_number_of_columns(test_df)
            if not status:
                logging.info('columns missing in testing set')
                validaton_error_messages.append('columns missing in testting set')
            else:
                logging.info('validation done for testting set columns')

            status = self.is_column_exist(train_df)
            if not status:
                logging.info('columns missing in training set')
                validaton_error_messages.append('columns missing in training set')
            else:
                logging.info('validation done for training set columns')  

            status = self.is_column_exist(test_df)
            if not status:
                logging.info('columns missing in testing set')
                validaton_error_messages.append('columns missing in testting set')
            else:
                logging.info('validation done for testting set columns')
            
            if validaton_error_messages:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info('drift detected')
                    validaton_error_messages.append('drift_detected')
                else:
                    logging.info('drift not detected')
                    validaton_error_messages.append('drift not detected')    
            
            else:
                logging.info(f'validation error: {validaton_error_messages}')

            data_vaildation_artifacts = DataValidationArtifacts(message='. '.join(validaton_error_messages),
                                                                validation_status=drift_status,
                                                                drift_report_file_path=self.data_validation_config.drift_report_file_path)

            logging.info(f'data validation artifacts captured : {data_vaildation_artifacts}')
            return data_vaildation_artifacts
        except Exception as e:
            raise CustomException(e, sys) from e



            

