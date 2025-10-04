import sys
import pickle
from src.exception import CustomException
from src.logger import logging
import numpy as np
logger=logging.getLogger('perdictor')
import pandas as pd

class Predictor:
    def __init__(self):
        
        self.model_path='artifacts/trained_model.pkl'
        self.column_processor_path='artifacts/column_processor.pkl'

    def predict(self,input):

        try:
            data = {
                'gender': input['gender'],
                'race/ethnicity': input['race/ethnicity'],
                'parental level of education': input['parental level of education'],
                'lunch': input['lunch'],
                'test preparation course': input['test preparation course'],
                'reading score': input['reading score'],
                'writing score': input['writing score']
            }

            logger.info('initated predictor')
            df = pd.DataFrame([data])

            with open(self.column_processor_path,'rb') as p:
                processor=pickle.load(p)

            processed_input=processor.transform(df)
            with open(self.model_path,'rb') as f:
                model=pickle.load(f)

            logger.info('loaded the trained model')
            prediction=model.predict(processed_input)
            logger.info(f'prediction completed predicted value: {prediction}')

            return prediction


        except Exception as e:
            raise CustomException(e,sys)



input_data = {
    "gender": "male",
    "race/ethnicity": "group D",
    "parental level of education": "high school",
    "lunch": "free/reduced",
    "test preparation course": "completed",
    "reading score": 64,
    "writing score": 67
}

p=Predictor()
print(p.predict(input_data))
