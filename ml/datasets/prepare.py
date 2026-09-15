import sys
import os
import json
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ml.datasets.kaggle_landmarks import KaggleLandmarkDataset

def main():
    print("DATASET PREPARATION")
    print("===================\n")
    
    raw_data_path = os.path.join(os.path.dirname(__file__), '../dataset/raw/hand_gesture_landmarks.csv')
    mapping_path = os.path.join(os.path.dirname(__file__), 'mappings.yaml')
    out_dir = os.path.join(os.path.dirname(__file__), '../dataset/processed')
    
    adapter = KaggleLandmarkDataset(raw_data_path, mapping_path)
    
    try:
        X, y, metadata = adapter.prepare()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
        
    os.makedirs(out_dir, exist_ok=True)
    
    np.save(os.path.join(out_dir, 'X.npy'), X)
    np.save(os.path.join(out_dir, 'y.npy'), y)
    
    metadata['classes'] = list(np.unique(y)) if len(y) > 0 else []
    
    with open(os.path.join(out_dir, 'dataset_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
        
    print(f"Preparation complete.")
    print(f"Valid samples: {metadata['valid_samples']}")
    print(f"Rejected samples: {metadata['rejected_samples']}")
    if metadata['rejected_samples'] > 0:
        print("Rejection reasons:")
        for reason, count in metadata['rejection_reasons'].items():
            print(f"  {reason}: {count}")

if __name__ == "__main__":
    main()
