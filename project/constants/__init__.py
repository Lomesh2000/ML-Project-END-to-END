## contains constant value for our project 
## dedicated solely to storing such values which are supposed to be unchanged

import os

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



