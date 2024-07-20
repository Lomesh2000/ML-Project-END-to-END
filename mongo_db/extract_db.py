from project.utils.main_utils import get_yaml_data
import pandas as pd
import os
from dotenv import load_dotenv
import pymongo
load_dotenv()

client = pymongo.MongoClient(os.getenv('CONNECTION_URL'))
data_base = client[os.getenv('DB_NAME')]
collection = data_base[os.getenv('COLLECTION_NAME')]

data = collection.find()

data = [doc for doc in data]