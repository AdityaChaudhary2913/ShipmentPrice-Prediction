from src.logger import logging
import sys
from typing import Dict
from pandas import DataFrame
import pandas as pd
from src.constants import *
from src.configuration.s3_operations import S3Operation
from src.exception import CustomException
from src.utils.main_utils import MainUtils

class shippingData:
    def __init__(
        self,
        artist,
        height,
        width,
        weight,
        material,
        priceOfSculpture,
        baseShippingPrice,
        international,
        expresssrc,
        installationIncluded,
        transport,
        fragile,
        customerInformation,
        remoteLocation,
    ):
        self.artist = artist
        self.height = height
        self.width = width
        self.weight = weight
        self.material = material
        self.priceOfSculpture = priceOfSculpture
        self.baseShippingPrice = baseShippingPrice
        self.international = international
        self.expresssrc = expresssrc
        self.installationIncluded = installationIncluded
        self.transport = transport
        self.fragile = fragile
        self.customerInformation = customerInformation
        self.remoteLocation = remoteLocation


    def get_data(self) -> Dict:
        logging.info("Entered get_data method of SensorData class")
        try:
            # Saving the features as dictionary
            input_data = {
                "Artist Reputation": [self.artist],
                "Height": [self.height],
                "Width": [self.width],
                "Weight": [self.weight],
                "Material": [self.material],
                "Price Of Sculpture": [self.priceOfSculpture],
                "Base Shipping Price": [self.baseShippingPrice],
                "International": [self.international],
                "Express Shipment": [self.expresssrc],
                "Installation Included": [self.installationIncluded],
                "Transport": [self.transport],
                "Fragile": [self.fragile],
                "Customer Information": [self.customerInformation],
                "Remote Location": [self.remoteLocation],
            }
            logging.info("Exited get_data method of SensorData class")
            return input_data
        except Exception as e:
            raise CustomException(e, sys)

    def get_input_data_frame(self) -> DataFrame:
        logging.info("Entered get_input_data_frame method of  class")
        try:
            # Getting the data in dictionary format
            input_dict = self.get_data()
            logging.info("Got data as dict")
            logging.info("Exited get_input_data_frame method of  class")
            return pd.DataFrame(input_dict)
        except Exception as e:
            raise CustomException(e, sys) from e


class CostPredictor:
    def __init__(self):
        self.s3 = S3Operation()
        self.bucket_name = BUCKET_NAME
        self.best_model_path = "ShipmentPrice-Prediction/best_model/shipping_price_model.pkl"

    def predict(self, X) -> float:
        logging.info("Entered predict method of the class")
        try:
            # Loading the best model from s3 bucket
            best_model = None
            try:
                best_model = self.s3.load_model(MODEL_FILE_NAME, self.bucket_name)
                logging.info("Loaded best model from s3 bucket")
            except:
                best_model = MainUtils.load_object(self.best_model_path)
            print(best_model)
            # Predicting with best model
            result = best_model.predict(X)
            logging.info("Exited predict method of the class")
            return result

        except Exception as e:
            raise CustomException(e, sys) from e
