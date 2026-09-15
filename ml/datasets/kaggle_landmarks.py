import pandas as pd
import numpy as np
import os
import sys

# Ensure backend modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.vision.landmark_processor import extract_features

from .base import BaseDatasetAdapter

class KaggleLandmarkDataset(BaseDatasetAdapter):
    def _read_data(self):
        if not os.path.exists(self.raw_data_path):
            raise FileNotFoundError(f"Dataset not found at {self.raw_data_path}")
        # Identify format
        if self.raw_data_path.endswith('.csv'):
            df = pd.read_csv(self.raw_data_path)
        elif self.raw_data_path.endswith('.json'):
            df = pd.read_json(self.raw_data_path)
        else:
            raise ValueError("Unsupported format. Expected .csv or .json")
        return df

    def inspect(self):
        try:
            df = self._read_data()
        except FileNotFoundError as e:
            return {"status": "INVALID", "error": str(e)}

        columns = list(df.columns)
        
        # Heuristics for label and landmarks
        label_col = 'label' if 'label' in columns else columns[0]
        landmark_cols = [c for c in columns if c != label_col]
        
        missing_values = df.isnull().sum().sum()
        duplicates = df.duplicated().sum()
        
        classes = df[label_col].value_counts().to_dict()

        # Try to find metadata columns (e.g. user_id, session_id)
        metadata_cols = [c for c in columns if 'id' in c.lower() or 'user' in c.lower() or 'session' in c.lower()]
        metadata_available = {c: df[c].nunique() for c in metadata_cols}

        landmark_vals = df[landmark_cols].values
        coord_range = (float(np.min(landmark_vals)), float(np.max(landmark_vals))) if len(landmark_vals) > 0 else (0,0)

        return {
            "status": "VALID",
            "source": self.raw_data_path,
            "total_samples": len(df),
            "classes": classes,
            "feature_dimension": len(landmark_cols),
            "expected_landmarks": 21 * 3,
            "found_landmarks": len([c for c in landmark_cols if c not in metadata_cols]),
            "missing_values": int(missing_values),
            "duplicates": int(duplicates),
            "metadata": metadata_available,
            "coord_range": coord_range
        }

    def prepare(self):
        df = self._read_data()
        columns = list(df.columns)
        label_col = 'label' if 'label' in columns else columns[0]
        
        # Separate metadata columns from features
        metadata_cols = [c for c in columns if 'id' in c.lower() or 'user' in c.lower() or 'session' in c.lower()]
        
        # Identify landmark columns.
        landmark_cols = [c for c in columns if c != label_col and c not in metadata_cols]
        
        if len(landmark_cols) != 63:
            raise ValueError(f"Expected 63 coordinate columns (21x3), found {len(landmark_cols)}. Inspection required.")

        X_processed = []
        y_processed = []
        rejected = 0
        rejection_reasons = {}

        for _, row in df.iterrows():
            raw_label = str(row[label_col]).strip()
            
            # Use mappings
            if raw_label in self.mappings:
                mapped_label = self.mappings[raw_label]
            else:
                # Unsupported label, reject
                rejected += 1
                rejection_reasons[raw_label] = rejection_reasons.get(raw_label, 0) + 1
                continue
            
            coords = row[landmark_cols].values
            
            # Assume interleaved x,y,z: x0, y0, z0, x1, y1, z1...
            # Convert to list of dicts for the existing feature processor
            landmarks = []
            try:
                for i in range(0, 63, 3):
                    landmarks.append({'x': coords[i], 'y': coords[i+1], 'z': coords[i+2]})
                    
                features = extract_features(landmarks)
                X_processed.append(features)
                y_processed.append(mapped_label)
            except Exception as e:
                rejected += 1
                err_str = f"ParsingError: {str(e)}"
                rejection_reasons[err_str] = rejection_reasons.get(err_str, 0) + 1

        metadata = {
            "valid_samples": len(X_processed),
            "rejected_samples": rejected,
            "rejection_reasons": rejection_reasons
        }

        return np.array(X_processed), np.array(y_processed), metadata
