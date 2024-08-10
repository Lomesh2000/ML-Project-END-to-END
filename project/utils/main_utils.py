import yaml
import numpy as np
from project.exception import CustomException
from project.logger import logging
import sys
import os
import dill
import json

def get_yaml_data(file: str='config', key: str=None):
    if file=='hyper_params':
        path = 'config//hyper_parameter.yaml'
    else:
        path = 'config//config.yaml'
    with open(path, 'r') as f:
        yaml_data = yaml.safe_load(f)
    f.close()
    return yaml_data[key]   

def load_json() -> dict:
    """
    """
    with open('config//hyper_parameter.json', 'r') as f:
        return json.load(f)

  
def read_yaml_file(file_path: str):
    try:
        with open(file_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        return yaml_data  
    except Exception as e:
        raise CustomException(e, sys) from e

def write_yaml_file(file_path: str, content: object, replace: bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys) from e   

def save_object(file_path: str, content: object):
    logging.info('saving object at: ', file_path)
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            dill.dump(content, file)

        logging.info('object saved........')
    except Exception as e:
        raise CustomException(e, sys) from e    


def save_as_numpy_array(file_path: str, array: object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as f:
            np.save(f, array)
    except Exception as e:
        raise CustomException(e, sys) from e   

def load_numpy_array(file_path: str):
    try:
        with open(file_path, 'rb') as file:
            obj = np.load(file)
            return obj
    except Exception as e:
        raise CustomException(e, sys) from e   
    
          