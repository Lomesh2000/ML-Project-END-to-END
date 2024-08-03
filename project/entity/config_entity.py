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
    