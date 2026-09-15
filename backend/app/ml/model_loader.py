import os
import json
import joblib

class ModelLoader:
    _instance = None

    def __init__(self):
        self.model = None
        self.metadata = None
        self.load_model()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_model(self):
        models_dir = os.path.join(os.path.dirname(__file__), '../../../ml/models')
        try:
            with open(os.path.join(models_dir, 'current.json'), 'r') as f:
                current = json.load(f)
            
            self.model = joblib.load(os.path.join(models_dir, current['path']))
            
            metadata_file = current.get('metadata_path', 'model_metadata_v1.json')
            with open(os.path.join(models_dir, metadata_file), 'r') as f:
                self.metadata = json.load(f)
        except Exception as e:
            print(f"Warning: Model could not be loaded. {e}")
            self.model = None
            self.metadata = None

model_loader = ModelLoader.get_instance()
