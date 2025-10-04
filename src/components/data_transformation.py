import pandas as pd
import os
import sys
from src.logger import logging
from src.exception import CustomException
from sklearn.compose import ColumnTransformer, _column_transformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from src.components.data_injestion import DataInjestion
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.utils import save_object

logger = logging.getLogger('data_transformation')
 

class DataTransform:
    
    def __init__(self):
        self.column_processor_obj_path=os.path.join('artifacts','column_processor.pkl')
        
        
        ingestion = DataInjestion()
        self.train_data_path, self.test_data_path = ingestion.initiate_data_ingestion()
        

    def get_transformer_object(self):
        try:

            
            ordinal_features = ['parental level of education','lunch','test preparation course']
            nominal_features = ['gender','race/ethnicity']
            numerical_features = ['reading score','writing score']
            


            order_of_ordinals = [
                ["some high school","high school","some college","bachelor's degree","associate's degree","master's degree"],
                ['free/reduced','standard'],
                ['none','completed']
            ]

            ordinal_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='most_frequent')),
                    ("ordinal_encoding",OrdinalEncoder(categories=order_of_ordinals))
                ]
            )

            nominal_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='most_frequent')),
                    ("onehot_encoding",OneHotEncoder(handle_unknown='ignore', sparse_output=False))

                ]
            )

            numerical_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='mean')),
                    ("scaler",StandardScaler())
                ]
            )
            
            logger.info('Column transformer creation started')
            
            column_transformer=ColumnTransformer(
                [("ord_transform",ordinal_pipeline,ordinal_features),
                ("nom_transform",nominal_pipeline,nominal_features),
                ("num_transform",numerical_pipeline,numerical_features)],
                remainder='passthrough',
                verbose_feature_names_out=False
            )


            return column_transformer
                
                
            

        except Exception as e:
            logger.error(e)
            raise CustomException(str(e), sys)


    def transform_data(self,train_path,test_path):
        try:

            column_transformer=self.get_transformer_object()
            logger.info('obtained the column_transormer object')
            train_data=pd.read_csv(train_path)
            test_data=pd.read_csv(test_path)

            x_train=train_data.drop('math score',axis=1)
            y_train=train_data['math score']
            x_test=test_data.drop('math score',axis=1)
            y_test=test_data['math score']

            logger.info('colum transformation begins')
            transformed_x_train=column_transformer.fit_transform(x_train)
            transformed_x_test=column_transformer.transform(x_test)

            save_object(file_path=self.column_processor_obj_path,
                    obj=column_transformer

            )
            logger.info('saved the transformer object to pkl file')
            return (
                transformed_x_train,
                y_train,
                transformed_x_test,
                y_test

            )




        except Exception as e:
            raise CustomException(e,sys)





if __name__ == "__main__":
    t = DataTransform()
    a,b,c,d=t.transform_data(r'artifacts\train_data.csv',r'artifacts\test_data.csv')
    print(a.shape)
    print(b.shape)
    print(c.shape)
    print(d.shape)

