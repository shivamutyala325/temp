import sys
import pandas as pd
import os
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split

logger=logging.getLogger('data_injestion')

artifact_dir='artifacts'


class DataInjestion:
    def __init__(self):
        self.raw_data_path=os.path.join(artifact_dir,'raw_data.csv')
        self.train_data_path=os.path.join(artifact_dir,'train_data_dir.csv')
        self.test_dir_path=os.path.join(artifact_dir,'test_data_dir.csv')


    def initiate_data_ingestion(self): 
        try:
            logger.info('data injestion intiated')

            df=pd.read_csv('notebook\data\StudentsPerformance.csv')
            logger.info('read the raw_data into df')

            train_data,test_data=train_test_split(df,test_size=0.2,random_state=34)
            logger.info('splitted rawdata to test and train')

            df.to_csv(self.raw_data_path,index=False)
            train_data.to_csv(self.train_data_path,index=False)
            test_data.to_csv(self.test_dir_path,index=False)
            logger.info("injestion is completed")

            return (
                self.train_data_path,
                self.test_dir_path
            )


        except Exception as e:
            logging.error(e)
            raise CustomException(str(e),sys)


d=DataInjestion()
d.initiate_data_ingestion()