from sklearn.linear_model import LinearRegression
import pickle
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import os
import sys
from src.components.data_transformation import DataTransform
from sklearn.metrics import r2_score
    



logger=logging.getLogger('model_trainer')


class ModelTrainer:
    def __init__(self):
        self.model_path=os.path.join('artifacts','trained_model.pkl')
        self.data_transform=DataTransform()
        
        self.test_data_path='artifacts/test_data.csv'
        self.train_data_path='artifacts/train_data.csv'

    def initate_training(self):
        try:
            x_train,y_train,x_test,y_test=self.data_transform.transform_data(self.train_data_path,self.test_data_path)
            logger.info('fetched the transfored train and test data')


            model=LinearRegression()
            model.fit(x_train,y_train)
            logger.info('model training completed')
            save_object(file_path=self.model_path,obj=model)
            logger.info('trained model saved into pickel file')

            y_pred=model.predict(x_test)
            r2 = r2_score(y_test, y_pred)
            return r2

        except Exception as e:
            logger.error(e)
            raise CustomException(e,sys)


