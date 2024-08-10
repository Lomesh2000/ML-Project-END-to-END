import os
from project.constants import *
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACTS_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP

training_pipeline_config = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIRECTORY_NAME)
    feature_store_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_DIRECTORY, DATA_FILE)
    training_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAINING_FILE)
    test_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE)
    train_test_split_ratio = TRAIN_TEST_SPLIT_RATIO
    collection_name = COLLECTION_NAME

@dataclass
class DataValidationConfig:
    data_vaidation_dir = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    drift_report_file_path = os.path.join(data_vaidation_dir, DATA_DRIFT_DIR_NAME, DATA_DRIFT_REPORT_NAME)

@dataclass
class DataTransformationConfig:    
    data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORAMTION_DIR_NAME_DIR)
    transformed_data_train_file_path = os.path.join(data_transformation_dir, DATA_TRASFORMATION_TRANSFORMED_DATA_DIR, TRAINING_FILE.replace('.csv', '.npy'))
    transformed_data_test_file_path = os.path.join(data_transformation_dir, DATA_TRASFORMATION_TRANSFORMED_DATA_DIR, TEST_FILE.replace('.csv', '.npy') )
    data_preprocessor_obj_file_path = os.path.join(data_transformation_dir, DATA_TRAINFORMATION_PREPROCESSOR_OBJECT_DIR,
                                                   PREPROCESSIG_FILE_NAME)

@dataclass
class ModelTrainerConfig:
    model_traning_dir = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINING_DIR_NAME)
    model_trained_model_file_path = os.path.join(model_traning_dir, MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                 MODEL_TRAINER_TRAINED_MODEL_NAME)
    expected_accuracy = MODEL_TRAINER_EXPECTED_SCORE
    model_config_file_path = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    all_model_performance_csv_file = os.path.join(model_traning_dir, MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                 ALL_MODEL_PERFORMACE_FILE_PATH)