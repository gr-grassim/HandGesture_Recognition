import os
import json
import pandas as pd
import numpy as np
import joblib
import sys

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
from app.vision.landmark_processor import extract_features

def main():
    # 1. Load CSV
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../datasets/raw/youssefelebiary/gesture_landmarks.csv'))
    df = pd.read_csv(file_path)
    df.columns = [c.strip() for c in df.columns]
    df['gesture_label'] = df['gesture_label'].str.strip()

    # 2. Map classes and combine inverted variants
    class_mapping = {
        'open': 'open_palm',
        'open_inverted': 'open_palm',
        'close': 'fist',
        'close_inverted': 'fist',
        'point': 'pointing',
        'point_inverted': 'pointing',
        'peace': 'victory',
        'peace_inverted': 'victory',
        'thumb': 'thumbs_up',
        'thumb_inverted': 'thumbs_up',
        'rock': 'rock',
        'rock_inverted': 'rock'
    }
    
    df['mapped_label'] = df['gesture_label'].map(class_mapping)
    df = df.dropna(subset=['mapped_label']).copy()

    # 3. Canonical Feature Extraction
    features_list = []
    labels_list = []
    
    for _, row in df.iterrows():
        landmarks = []
        for i in range(21):
            x = row[f'landmark_{i}_x']
            y = row[f'landmark_{i}_y']
            z = row[f'landmark_{i}_z']
            landmarks.append({'x': x, 'y': y, 'z': z})
        
        # Canonical python extractor
        feat_vec = extract_features(landmarks)
        assert len(feat_vec) == 63
        features_list.append(feat_vec)
        labels_list.append(row['mapped_label'])

    X = np.array(features_list)
    y = np.array(labels_list)
    
    print(f"Total valid samples: {len(X)}")
    print(f"Feature dimensions: {X.shape[1]}")

    # 4. Split 70/15/15
    # First split: 70% train, 30% temp (val+test)
    sss1 = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
    train_idx, temp_idx = next(sss1.split(X, y))
    
    X_train, y_train = X[train_idx], y[train_idx]
    X_temp, y_temp = X[temp_idx], y[temp_idx]
    
    # Second split: split the 30% temp equally into 15% val, 15% test
    sss2 = StratifiedShuffleSplit(n_splits=1, test_size=0.5, random_state=42)
    val_idx, test_idx = next(sss2.split(X_temp, y_temp))
    
    X_val, y_val = X_temp[val_idx], y_temp[val_idx]
    X_test, y_test = X_temp[test_idx], y_temp[test_idx]

    print(f"Train size: {len(X_train)}")
    print(f"Val size:   {len(X_val)}")
    print(f"Test size:  {len(X_test)}")
    
    print("\nTrain class counts:")
    print(pd.Series(y_train).value_counts())
    print("\nValidation class counts:")
    print(pd.Series(y_val).value_counts())
    print("\nTest class counts:")
    print(pd.Series(y_test).value_counts())

    # 5. Train Random Forest
    rf = RandomForestClassifier(
        n_estimators=100,
        max_features='sqrt',
        min_samples_split=2,
        random_state=42
    )
    rf.fit(X_train, y_train)

    # 6. Evaluation on Test Set (Do not tune)
    y_test_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_test_pred)
    prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_test_pred, average='macro', zero_division=0)
    prec_wt, rec_wt, f1_wt, _ = precision_recall_fscore_support(y_test, y_test_pred, average='weighted', zero_division=0)
    
    print("\n--- TEST METRICS ---")
    print(f"Accuracy:        {acc:.4f}")
    print(f"Macro F1:        {f1_macro:.4f}")
    print(f"Weighted F1:     {f1_wt:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_test_pred, zero_division=0))
    
    print("Confusion Matrix:")
    labels_order = np.unique(y_test)
    cm = confusion_matrix(y_test, y_test_pred, labels=labels_order)
    print(pd.DataFrame(cm, index=labels_order, columns=labels_order))

    # 7. Save model and metadata
    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'gesture_model_v2.joblib')
    joblib.dump(rf, model_path)
    
    metadata = {
        "dataset_name": "Hand Gesture Landmarks",
        "source": "https://www.kaggle.com/datasets/youssefelebiary/hand-gesture-landmarks",
        "license": "MIT",
        "original_classes": list(class_mapping.keys()),
        "mapped_classes": list(np.unique(y)),
        "number_of_samples": len(X),
        "class_distribution": pd.Series(y).value_counts().to_dict(),
        "feature_specification_version": "v1_63D_canonical",
        "preprocessing_version": "v1_translated_normalized_by_wrist_max",
        "split_method": "stratified_shuffle_split",
        "split_seed": 42,
        "subject_metadata_available": False,
        "subject_independent_evaluation": False,
        "train_count": len(X_train),
        "validation_count": len(X_val),
        "test_count": len(X_test),
        "evaluation_metrics": {
            "test_accuracy": acc,
            "test_macro_f1": f1_macro,
            "test_weighted_f1": f1_wt
        },
        "is_real_human_data": True,
        "classes_supported": 6,
        "is_production_ready": False,
        "dataset_warning": "Dataset is extremely small (364 samples). Used for pipeline validation only."
    }
    
    metadata_path = os.path.join(models_dir, 'model_metadata_v2.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
        
    print(f"\nModel v2 saved to {model_path}")
    print(f"Metadata saved to {metadata_path}")

if __name__ == '__main__':
    main()
