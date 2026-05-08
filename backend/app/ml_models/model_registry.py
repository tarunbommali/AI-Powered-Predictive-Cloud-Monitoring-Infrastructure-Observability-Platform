
"""
Model Registry
"""

from datetime import datetime


class ModelRegistry:

    def __init__(self):

        self.models = {}

    def register_model(
        self,
        name,
        version,
        model_path
    ):

        self.models[name] = {
            'version': version,
            'model_path': model_path,
            'registered_at': (
                datetime.now().isoformat()
            )
        }

    def get_model(self, name):

        return self.models.get(name)

    def list_models(self):

        return self.models
        

model_registry = ModelRegistry()
