from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    trained_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifacts:
    validation_status: bool # if true then only it will go to data transformation else exception throw
    message: str # data drift detected or not
    drift_report_file_path: str

@dataclass
class DataTransformationArtifacts:
    tranformed_train_data_path: str
    transformed_test_data_path: str
    preprocessor_obj_file_path: str

@dataclass
class ClassificationMetricArtifacts:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainingArtifacts:
    trained_model_file_path: str
    # metrics_artifact: ClassificationMetricArtifacts