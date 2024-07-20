from project.utils.main_utils import get_yaml_data
import pandas as pd
import os
from dotenv import load_dotenv
import pymongo
load_dotenv()

data = pd.read_csv(get_yaml_data('dataset_file_name'))
df = data.to_dict(orient='records')

client = pymongo.MongoClient(os.getenv('CONNECTION_URL'))
data_base = client[os.getenv('DB_NAME')]
collection = data_base[os.getenv('COLLECTION_NAME')]
collection.insert_many(df)