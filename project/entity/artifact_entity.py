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
