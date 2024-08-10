import sys

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from project.exception import CustomException
from project.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.Certified = 0
        self.Denied = 1

    def _asdict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))    