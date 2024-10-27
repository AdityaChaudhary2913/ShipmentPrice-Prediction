import sys
from src.configuration.s3_operations import S3Operation
from src.entity.artifacts_entity import (DataTransformationArtifacts, ModelPusherArtifacts, ModelTrainerArtifacts)
from src.entity.config_entity import ModelPusherConfig
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils

class ModelPusher:
    def __init__(
        self,
        model_pusher_config: ModelPusherConfig,
        model_trainer_artifacts: ModelTrainerArtifacts,
        data_transformation_artifacts: DataTransformationArtifacts,
        s3: S3Operation
    ):

        self.model_pusher_config = model_pusher_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts = data_transformation_artifacts
        self.s3 = s3

    def initiate_model_pusher(self) -> ModelPusherArtifacts:
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")
        try:
            # Uploading the best model to s3 bucket
            try:
                self.s3.upload_file(
                    self.model_trainer_artifacts.trained_model_file_path,
                    self.model_pusher_config.S3_MODEL_KEY_PATH,
                    self.model_pusher_config.BUCKET_NAME,
                    remove=False,
                )
                logging.info("Uploaded best model to s3 bucket")
                model_pusher_artifact = ModelPusherArtifacts(
                    bucket_name=self.model_pusher_config.BUCKET_NAME,
                    s3_model_path=self.model_pusher_config.S3_MODEL_KEY_PATH,
                )
                return model_pusher_artifact
            
            except:
                model = MainUtils.load_object(self.model_trainer_artifacts.trained_model_file_path)
                MainUtils.save_object("ShipmentPrice-Prediction/best_model/shipping_price_model.pkl", model)
                logging.info("Uploaded best model to best_model folder in the local system becuase s3 doesn't exist")
                model_pusher_artifact = ModelPusherArtifacts(
                    bucket_name=self.model_pusher_config.BUCKET_NAME,
                    s3_model_path=self.model_pusher_config.S3_MODEL_KEY_PATH,
                    best_model_path="ShipmentPrice-Prediction/best_model/shipping_price_model.pkl"
                )
                return model_pusher_artifact

        except Exception as e:
            raise CustomException(e, sys) from e