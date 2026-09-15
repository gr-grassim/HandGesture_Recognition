import os
import yaml
from abc import ABC, abstractmethod

class BaseDatasetAdapter(ABC):
    def __init__(self, raw_data_path: str, mapping_config_path: str):
        self.raw_data_path = raw_data_path
        self.mapping_config_path = mapping_config_path
        self.mappings = self._load_mappings()
        
    def _load_mappings(self) -> dict:
        if not os.path.exists(self.mapping_config_path):
            return {}
        with open(self.mapping_config_path, 'r') as f:
            config = yaml.safe_load(f)
            return config.get('label_mapping', {})

    @abstractmethod
    def inspect(self) -> dict:
        """
        Inspects the dataset and returns a dictionary containing:
        - Total samples
        - Classes
        - Missing values count
        - Feature dimension
        - Metadata (e.g. user_id)
        """
        pass

    @abstractmethod
    def prepare(self) -> tuple:
        """
        Reads raw data, applies target mappings, converts landmarks to canonical format, 
        and extracts features using the canonical feature processor.
        
        Returns:
            X (numpy array): The final processed feature vectors
            y (numpy array): The string labels
            metadata (dict): Any relevant metadata like rejection stats.
        """
        pass
