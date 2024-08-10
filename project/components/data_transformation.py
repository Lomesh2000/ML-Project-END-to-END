import os
import sys

import numpy as np
import pandas as pd

from project.constants import TARGET_COLUMN, CURRENT_YEAR, SCHEMA_PATH

from sklearn.preprocessing import PowerTransformer, StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer    
from sklearn.pipeline import Pipeline

from imblearn.combine import SMOTEENN, SMOTETomek

from project.entity.config_entity import DataTransformationConfig
from project.entity.artifact_entity import DataIngestionArtifacts, DataValidationArtifacts, DataTransformationArtifacts

from project.logger import logging
from project.exception import CustomException

from project.utils.main_utils import save_object, load_numpy_array, save_as_numpy_array, read_yaml_file
from project.entity.estimator import TargetValueMapping

class DataTransformation:

    def __init__(self, data_ingestion_artifacts: DataIngestionArtifacts,
                 data_validation_artifacts: DataValidationArtifacts,
                 data_tranformation_config: DataTransformationConfig):
        try:
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_artifacts = data_validation_artifacts
            self.data_tranformation_config = data_tranformation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_PATH)
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def get_data_transformer_object(self) -> Pipeline:
        logging.info('creating data transformer object')

        try:
            numerical_transformer = StandardScaler()
            one_hot_encoder = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()
            logging.info('Initiliased standardscaler , onehotencoder, ordinalencoder')

            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']

            logging.info('got all the columns and seperated into what to tranformed into what ')

            transformation_pipeline = Pipeline(steps=[
                ('transfomer', PowerTransformer(method='yeo-johnson'))
            ])

            logging.info('set up transformation pipeline')

            preprocessor = ColumnTransformer(
                [
                    ('OneHotEncoder', one_hot_encoder, oh_columns),
                    ('OrdinalEncoder', ordinal_encoder, or_columns),
                    ('Transformer', transformation_pipeline, transform_columns),
                    ('StandardScaler', numerical_transformer, num_features)
                ]
            )
            logging.info('set up the columns tranformer')
            logging.info('preprocessor object created')

            return preprocessor
            

        except Exception as e:
            raise CustomException(e, sys) from e    


    def initiate_data_transformation(self) -> DataTransformationArtifacts:
        """"""
        try:
            if self.data_validation_artifacts.validation_status:
                # code
                logging.info('data transformation started')
                preprocessor = self.get_data_transformer_object()

                train_df, test_df = (pd.read_csv(self.data_ingestion_artifacts.trained_file_path),
                                     pd.read_csv(self.data_ingestion_artifacts.test_file_path))
                
                input_features_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                # creating company age
                input_features_train_df['company_age'] = CURRENT_YEAR - input_features_train_df['yr_of_estab']

                columns_to_be_dropped = self._schema_config['drop_columns']
                input_features_train_df = input_features_train_df.drop(columns=columns_to_be_dropped, axis=1)

                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )

                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis = 1)
                target_feature_test_df = test_df[TARGET_COLUMN]
                input_feature_test_df['company_age'] = CURRENT_YEAR - input_feature_test_df['yr_of_estab']

                input_feature_test_df = input_feature_test_df.drop(columns=columns_to_be_dropped, axis=1)

                target_feature_test_df = target_feature_test_df.replace(
                    TargetValueMapping()._asdict()
                )

                input_feature_train_arr = preprocessor.fit_transform(input_features_train_df)
                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                #handling imbalance
                smt = SMOTEENN(sampling_strategy='minority')
                input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )
                
                input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )
                # print(target_feature_test_final)

                train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
                test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
                
                save_object(self.data_tranformation_config.data_preprocessor_obj_file_path, preprocessor)
                save_as_numpy_array(self.data_tranformation_config.transformed_data_train_file_path, 
                                    array=train_arr)
                save_as_numpy_array(self.data_tranformation_config.transformed_data_test_file_path,
                                    array=test_arr)
                
                logging.info('saved the preprocessor object')

                data_transformation_artifacts = DataTransformationArtifacts(
                    preprocessor_obj_file_path=self.data_tranformation_config.data_preprocessor_obj_file_path,
                    tranformed_train_data_path=self.data_tranformation_config.transformed_data_train_file_path,
                    transformed_test_data_path=self.data_tranformation_config.transformed_data_test_file_path
                )
                return data_transformation_artifacts
            else:
                raise Exception(self.data_validation_artifacts.message)    
        except Exception as e:
            raise CustomException(e, sys) from e     