import os
from project.entity.config_entity import ModelTrainerConfig
from project.entity.artifact_entity import ModelTrainingArtifacts, DataIngestionArtifacts, \
                                            DataValidationArtifacts, DataTransformationArtifacts
from project.logger import logging
from project.exception import CustomException
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import precision_score, f1_score, recall_score, roc_auc_score, roc_curve
from project.utils.main_utils import load_json, save_object

class ModelTrainer:

    models = {
    'logistic regression': LogisticRegression(),
    'KNeighborsClassifier': KNeighborsClassifier(),
    'DecisionTreeClassifier': DecisionTreeClassifier(),
    'RandomForestClassifier': RandomForestClassifier(),
    'AdaBoostClassifier': AdaBoostClassifier(),
    'GradientBoostingClassifier': GradientBoostingClassifier(),
    'SVC': SVC(),
    'XGBClassifier': XGBClassifier()
    }

    models_list = []
    train_accuracy_list = []
    test_accuracy_list = []
    auc = []
    f1_scrore = []
    precision = []
    recall = []
    roc_auc = []
    _best_model_before_hyperparameter_tuning = None
    models_after_hyperparameter_tuning = {}

    def __init__(self, data_ingestion_artifact: DataIngestionArtifacts, 
                 data_validation_artifact: DataValidationArtifacts, 
                 data_transformation_artifact: DataTransformationArtifacts,
                 model_trainer_config: ModelTrainerConfig):
        """

        """
        self.data_ingestion_artifact =data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
        self.train_arr: np.ndarray = np.load(data_transformation_artifact.transformed_test_data_path, allow_pickle=True)
        self.test_arr = np.load(data_transformation_artifact.tranformed_train_data_path, allow_pickle=True)

    def train_test_divide(self):
        print(self.train_arr.shape, self.test_arr.shape,'-----------')
        X_train, y_train, X_test, y_test = self.train_arr[:, :-1], self.train_arr[:, -1], \
                                            self.test_arr[:, :-1], self.test_arr[:, -1]
        return (X_train, X_test, y_train, y_test)
    
    def model_training(self, models=None):
        """
        
        """
        X_train, X_test, y_train, y_test = self.train_test_divide()

        for model_no in range(len(self.models)):
            model = list(self.models.values())[model_no]
            model.fit(X_train, y_train)

            # training_scores 
            y_train_pred = model.predict(X_train)
            self.train_accuracy_list.append(accuracy_score(y_train_pred, y_train))

            # test scores
            y_test_pred = model.predict(X_test)
            print(y_test_pred, 'main culprit')
            self.test_accuracy_list.append(accuracy_score(y_test_pred, y_test))

            self.f1_scrore.append(f1_score(y_test, y_test_pred))
            self.precision.append(precision_score(y_test, y_test_pred))
            self.recall.append(recall_score(y_test, y_test_pred))
            self.auc.append(roc_auc_score(y_test, y_test_pred))

    def create_report(self) -> pd.DataFrame:
        """
        creates and returns a report in form of pandas dataframe different metrices
        """
        report = pd.DataFrame(list(zip(self.models.keys(),
                                       self.train_accuracy_list,
                                       self.test_accuracy_list,
                                       self.f1_scrore,
                                       self.precision,
                                       self.recall,
                                       self.auc)), 
                                       columns= ['model_name', 'train_accuracy', 'test_accuracy', 'f1_score',
                                                 'precision', 'recall', 'auc']).sort_values(
                                                     by='test_accuracy', ascending=False)
        # os.makedirs(os.path.dirname(self.model_trainer_config.all_model_performance_csv_file))
        # report.to_csv(self.model_trainer_config.all_model_performance_csv_file)
        return report
    
    def best_models(self, n: int = 3) -> pd.DataFrame:
        """
        return n best models
        """
        report = self.create_report()
        report = report.iloc[:n]
        self._best_model_before_hyperparameter_tuning = (report.iloc[[1]]['model_name'], 
                                                         report.iloc[[1]]['test_accuracy'])
        return report
    
    def hyperparamter_tuning(self, report) -> dict:
        params = load_json()
        X_train, X_test, y_train, y_test = self.train_test_divide()
        model_params_after_tuning = {}
        grid_params = []
        print(report)
        for model_name in report['model_name']:
            grid_params.append((model_name, self.models[model_name], params[model_name]))
        
        for model_name, model, params in grid_params:
            grid = GridSearchCV(estimator=model,
                                param_grid=params,
                                cv=3,
                                verbose=2,
                                n_jobs=1)
            grid.fit(X_train, y_train)
            model_params_after_tuning[model_name] = (grid.best_params_, grid)
            self.models_after_hyperparameter_tuning[model_name] = accuracy_score(y_test, grid.predict(X_test))
        return model_params_after_tuning 

    def initiate_model_training(self):
        self.model_training(self.models)
        best_models_report = self.best_models()
        models = self.hyperparamter_tuning(best_models_report)

        models_accu = dict(sorted(self.models_after_hyperparameter_tuning.items(), key=lambda item: item[1]))
        model_obj = models[list(models_accu.keys())[0]][1]

        save_object(ModelTrainerConfig.model_trained_model_file_path, content=model_obj)
        model_training_artifacts = ModelTrainingArtifacts(
            trained_model_file_path=self.model_trainer_config.model_trained_model_file_path
        )

        return model_training_artifacts




        








    







            







