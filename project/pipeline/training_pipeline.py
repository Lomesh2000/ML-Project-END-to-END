import sys

from project.exception import CustomException
from project.logger import logging

from project.components.data_ingestion import DataIngestion
from project.entity.config_entity import DataIngestionConfig
from project.entity.artifact_entity import DataIngestionArtifacts

class TrainingPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        logging.info('got the data ingestion artifacts')
        return data_ingestion_artifacts

    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion() 
        except Exception as e:
            raise CustomException(e, sys) from e
