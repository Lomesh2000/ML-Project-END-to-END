import sys

from project.exception import CustomException
from project.logger import logging

from project.components.data_ingestion import DataIngestion
from project.components.data_validation import DataValidation
from project.components.data_transformation import DataTransformation
from project.components.model_trainer import ModelTrainer
from project.entity.config_entity import DataIngestionConfig, DataValidationConfig,\
    DataTransformationConfig, ModelTrainerConfig
from project.entity.artifact_entity import DataIngestionArtifacts, DataValidationArtifacts\
       ,DataTransformationArtifacts, ModelTrainingArtifacts

class TrainingPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()

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

    def start_data_transformation(self, data_ingestion_artifacts: DataIngestionArtifacts,
                                  data_validation_artifacts: DataValidationArtifacts):
        logging.info('starting data transformation')
        try:
            data_transformation = DataTransformation(data_ingestion_artifacts=data_ingestion_artifacts,
                                                     data_validation_artifacts=data_validation_artifacts,
                                                     data_tranformation_config=self.data_transformation_config)
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            return data_transformation_artifacts
        except Exception as e:
            raise CustomException(e, sys) from e    

    def start_model_training(self, data_ingestion_artifacts: DataIngestionArtifacts,
                                           data_validation_artifacts: DataValidationArtifacts,
                                           data_transformation_artifacts: DataTransformationArtifacts):
        logging.info('starting model training')
        try:
            model_training = ModelTrainer(data_ingestion_artifact=data_ingestion_artifacts,
                                          data_validation_artifact=data_validation_artifacts,
                                          data_transformation_artifact=data_transformation_artifacts,
                                          model_trainer_config=ModelTrainerConfig())
            model_training_artifacts = model_training.initiate_model_training()
            return model_training_artifacts
        except Exception as e:
            raise CustomException(e, sys) from e    

    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion() 
            data_validation_artifacts = self.start_data_validtion(data_ingestion_artifact=data_ingestion_artifacts)
            data_transformation_artifacts = self.start_data_transformation(data_ingestion_artifacts=data_ingestion_artifacts,
                                                                           data_validation_artifacts=data_validation_artifacts)
            model_training_artifacts = self.start_model_training(data_ingestion_artifacts=data_ingestion_artifacts,
                                                                 data_validation_artifacts=data_validation_artifacts,
                                                                 data_transformation_artifacts=data_transformation_artifacts)
        except Exception as e:
            raise CustomException(e, sys) from e
