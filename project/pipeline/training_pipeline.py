import sys

from project.exception import CustomException
from project.logger import logging

from project.components.data_ingestion import DataIngestion
from project.components.data_validation import DataValidation
from project.entity.config_entity import DataIngestionConfig, DataValidationConfig
from project.entity.artifact_entity import DataIngestionArtifacts, DataValidationArtifacts

class TrainingPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        logging.info('got the data ingestion artifacts')
        return data_ingestion_artifacts
    
    def start_data_validtion(self, data_ingestion_artifact) -> DataValidationArtifacts:
        logging.info('starting data validation')

        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                         data_validation_config=self.data_validation_config)
        data_validation_artifacts = data_validation.initiate_data_validation()
        logging.info('data validation done')

        return data_validation_artifacts

    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion() 
            data_validation_artifacts = self.start_data_validtion(data_ingestion_artifact=data_ingestion_artifacts)
        
        except Exception as e:
            raise CustomException(e, sys) from e
