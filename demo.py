from project.pipeline.training_pipeline import TrainingPipeline

onj = TrainingPipeline()
onj.run_pipeline()

# import numpy as np
# data = np.load(r"D:\Project\visa approval\ML-Project-END-to-END\artifacts\08_08_2024_22_38_43\transformed\transformed_data\test.npy", 
#                allow_pickle=True)
# print(data)
# import json
# with open('config//hyper_parameter.json', 'r') as f:
#         data = json.load(f)
# print(data)        