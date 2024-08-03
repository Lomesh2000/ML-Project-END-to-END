import yaml
from project.exception import CustomException
import sys
import os

def get_yaml_data(key):
    with open('config//config.yaml', 'r') as f:
        yaml_data = yaml.safe_load(f)
    f.close()
    return yaml_data[key]     

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