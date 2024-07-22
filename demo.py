from project.logger import logging
from project.exception import CustomException
import sys

logging.info('Welcome')
try:
    a = 10/0
except Exception as e:
    raise CustomException(e, sys)    