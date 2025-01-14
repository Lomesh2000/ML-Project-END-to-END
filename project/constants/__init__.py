## contains constant value for our project 
## dedicated solely to storing such values which are supposed to be unchanged

import os
from datetime import date

DB_NAME='ML_END_to_END'
COLLECTION_NAME='visa_data'
CONNECTION_URL='mongodb+srv://lomeshsoniwork:qJjqV3vzCEOYtOmv@phase1.8ijowa1.mongodb.net/'

PIPELINE_NAME = 'US_VISA'
ARTIFACTS_DIR = 'artifacts'
MODEL_FILE_NAME = 'model.pkl'

#csv file
DATA_FILE = 'us_visa.csv'

# train test file
TRAINING_FILE = 'train.csv'
TEST_FILE = 'test.csv'

# folders t be created during data ingestion 
DATA_INGESTION_COLLECTION_NAME = 'visa_data'
DATA_INGESTION_DIRECTORY_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_DIRECTORY: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'

# train test split ratio 
TRAIN_TEST_SPLIT_RATIO: float = 0.2

# target feature
TARGET_COLUMN = 'case_status'
CURRENT_YEAR = date.today().year
PREPROCESSIG_FILE_NAME = 'preprocessing.pkl'

# validation
DATA_VALIDATION_DIR_NAME = 'data_validation'
DATA_DRIFT_DIR_NAME = 'drift_report'
DATA_DRIFT_REPORT_NAME = 'drift_report.yaml'

# schema file path
SCHEMA_PATH = os.path.join('config', 'schema.yaml')

# transformation 
DATA_TRANSFORAMTION_DIR_NAME_DIR = 'transformed'
DATA_TRASFORMATION_TRANSFORMED_DATA_DIR = 'transformed_data'
DATA_TRAINFORMATION_PREPROCESSOR_OBJECT_DIR = 'preprocessor_obj'
PREPROCESSING_OBJECT_FILE_NAME = 'preprocessor.pkl'

# model training constants
MODEL_TRAINING_DIR_NAME = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR = 'trained_dir'
MODEL_TRAINER_TRAINED_MODEL_NAME = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE = 0.8
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH  = os.path.join('config', 'model.yaml')
ALL_MODEL_PERFORMACE_FILE_PATH = 'models_performancs.csv'                                                      

