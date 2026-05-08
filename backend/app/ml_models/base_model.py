
"""
Base ML Model Utilities
"""

import joblib
import os
import logging

logger = logging.getLogger(__name__)


class BaseModel:

    def __init__(self, model_dir='ml_data/models'):

        self.model_dir = model_dir

        os.makedirs(model_dir, exist_ok=True)

    def save_model(self, model, filename):

        try:

            path = f"{self.model_dir}/{filename}"

            joblib.dump(model, path)

            logger.info(f"Model saved: {path}")

            return True

        except Exception as e:

            logger.error(f"Save failed: {e}")

            return False

    def load_model(self, filename):

        try:

            path = f"{self.model_dir}/{filename}"

            model = joblib.load(path)

            logger.info(f"Model loaded: {path}")

            return model

        except Exception as e:

            logger.error(f"Load failed: {e}")

            return None
