import os
import sys
import numpy as np
import json
import joblib
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def main():
    print("MODEL EVALUATION")
    print("================\n")
    
    splits_dir = os.path.join(os.path.dirname(__file__), '../dataset/processed/splits')
    models_dir = os.path.join(os.path.dirname(__file__), '../models')
    
    try:
        X_test = np.load(os.path.join(splits_dir, 'X_test.npy'))
        y_test = np.load(os.path.join(splits_dir, 'y_test.npy'))
        
        with open(os.path.join(models_dir, 'current.json'), 'r') as f:
            current_model_info = json.load(f)
            
        model_path = os.path.join(models_dir, current_model_info['path'])
        clf = joblib.load(model_path)
        
        with open(os.path.join(models_dir, 'model_metadata_v1.json'), 'r') as f:
            meta = json.load(f)
    except Exception as e:
        print(f"Error loading evaluation data/model: {e}")
        return

    y_pred = clf.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"Test Accuracy: {acc:.4f}")
    print(f"Weighted Precision: {prec:.4f}")
    print(f"Weighted Recall: {rec:.4f}")
    print(f"Weighted F1: {f1:.4f}")
    
    # Per class metrics
    print("\nPer-class metrics:")
    p_class, r_class, f1_class, support = precision_recall_fscore_support(y_test, y_pred, labels=clf.classes_, zero_division=0)
    for i, cls in enumerate(clf.classes_):
        if support[i] > 0:
            print(f"  {cls}: Precision={p_class[i]:.4f}, Recall={r_class[i]:.4f}, F1={f1_class[i]:.4f}, Support={support[i]}")
            
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)
    print(cm)
    
    # Update metadata with metrics
    meta["metrics"] = {
        "accuracy": acc,
        "weighted_f1": f1,
        "weighted_precision": prec,
        "weighted_recall": rec
    }
    
    with open(os.path.join(models_dir, 'model_metadata_v1.json'), 'w') as f:
        json.dump(meta, f, indent=2)

if __name__ == "__main__":
    main()
