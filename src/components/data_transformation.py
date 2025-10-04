import pandas as pd
import os
import sys
from src.logger import logging
from src.exception import CustomException
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from src.components.data_injestion import DataInjestion


logger = logging.getLogger('data_transformation')
transformed_path = 'transformed_data'  

class DataTransform:
    
    def __init__(self):
        
        self.output_dir = os.path.join('artifacts', transformed_path)
        os.makedirs(self.output_dir, exist_ok=True)

        self.transformed_train_path = os.path.join(self.output_dir, 'transformed_train.csv')
        self.transformed_test_path = os.path.join(self.output_dir, 'transformed_test.csv')
        
        ingestion = DataInjestion()
        self.train_data_path, self.test_data_path = ingestion.initiate_data_ingestion()
        

    def transform_data(self):
        try:
            logger.info('Transformation initiated')
            self.test_data = pd.read_csv(self.test_data_path)
            self.train_data = pd.read_csv(self.train_data_path)
            logger.info('Data read successfully from artifacts')

            
            self.ordinal_features = ['parental level of education','lunch','test preparation course']
            self.nominal_features = ['gender','race/ethnicity']
            self.numerical_features = ['reading score','writing score']

            self.order_of_ordinals = [
                ["some high school","high school","some college","bachelor's degree","associate's degree","master's degree"],
                ['free/reduced','standard'],
                ['none','completed']
            ]

            
            logger.info('Column transformer creation started')
            self.transformer = ColumnTransformer(
                transformers=[
                    ("ord", OrdinalEncoder(categories=self.order_of_ordinals), self.ordinal_features),
                    ("nom", OneHotEncoder(), self.nominal_features),
                    ("num", StandardScaler(), self.numerical_features)
                ],
                remainder='drop'
            )

            
            self.transformed_train_data = self.transformer.fit_transform(self.train_data)
            self.transformed_test_data = self.transformer.transform(self.test_data)

            
            feature_names = self.transformer.get_feature_names_out()

            # Save with proper column names
            pd.DataFrame(self.transformed_train_data, columns=feature_names).to_csv(self.transformed_train_path, index=False)
            pd.DataFrame(self.transformed_test_data, columns=feature_names).to_csv(self.transformed_test_path, index=False)

            logger.info('Saved transformed data into files')

            return (
                self.transformed_train_path,
                self.transformed_test_path
            )

        except Exception as e:
            logger.error(e)
            raise CustomException(str(e), sys)


# Run directly
if __name__ == "__main__":
    t = DataTransform()
    print(t.transform_data())
