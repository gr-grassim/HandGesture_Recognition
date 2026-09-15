import os
import sys
import numpy as np
import json
import joblib
from sklearn.ensemble import RandomForestClassifier

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ml.training.split import perform_split

def main():
    print("MODEL TRAINING")
    print("==============\n")
    
    processed_dir = os.path.join(os.path.dirname(__file__), '../dataset/processed')
    models_dir = os.path.join(os.path.dirname(__file__), '../models')
    
    try:
        X = np.load(os.path.join(processed_dir, 'X.npy'))
        y = np.load(os.path.join(processed_dir, 'y.npy'))
        with open(os.path.join(processed_dir, 'dataset_metadata.json'), 'r') as f:
            ds_meta = json.load(f)
    except Exception as e:
        print(f"Error loading processed dataset: {e}")
        return

    print(f"Loaded {len(X)} samples.")
    
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = perform_split(X, y)
    print(f"Split: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")
    
    clf = RandomForestClassifier(
        n_estimators=100, 
        max_depth=None, 
        min_samples_split=2, 
        max_features='sqrt',
        random_state=42
    )
    
    print("Training Random Forest...")
    clf.fit(X_train, y_train)
    
    # Save the splits for evaluation script
    os.makedirs(os.path.join(processed_dir, 'splits'), exist_ok=True)
    np.save(os.path.join(processed_dir, 'splits', 'X_test.npy'), X_test)
    np.save(os.path.join(processed_dir, 'splits', 'y_test.npy'), y_test)
    
    # Save model and metadata
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(clf, os.path.join(models_dir, 'gesture_model_v1.joblib'))
    
    model_metadata = {
        "model_type": "RandomForestClassifier",
        "model_version": "1.0",
        "feature_spec_version": "1.0",
        "training_data_type": "synthetic_fixture",
        "is_production_model": False,
        "classes": list(clf.classes_),
        "dataset": "kaggle_synthetic_fixture",
        "train_samples": len(X_train),
        "validation_samples": len(X_val),
        "test_samples": len(X_test),
        "hyperparameters": clf.get_params()
    }
    
    with open(os.path.join(models_dir, 'model_metadata_v1.json'), 'w') as f:
        json.dump(model_metadata, f, indent=2)
        
    with open(os.path.join(models_dir, 'current.json'), 'w') as f:
        json.dump({"active_model_version": "1.0", "path": "gesture_model_v1.joblib"}, f, indent=2)

    print("Training complete. Model saved to ml/models/gesture_model_v1.joblib")

if __name__ == "__main__":
    main()
