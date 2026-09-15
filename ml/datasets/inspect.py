import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ml.datasets.kaggle_landmarks import KaggleLandmarkDataset

def main():
    print("DATASET INSPECTION")
    print("==================\n")
    
    raw_data_path = os.path.join(os.path.dirname(__file__), '../dataset/raw/hand_gesture_landmarks.csv')
    mapping_path = os.path.join(os.path.dirname(__file__), 'mappings.yaml')
    
    adapter = KaggleLandmarkDataset(raw_data_path, mapping_path)
    
    report = adapter.inspect()
    
    print(f"Dataset: {adapter.__class__.__name__}")
    print(f"Source: {report.get('source', raw_data_path)}")
    print(f"Status: {report['status']}")
    
    if report['status'] == 'INVALID':
        print(f"\nError: {report.get('error')}")
        print("\nNote: Please authenticate with Kaggle and download the dataset:")
        print("kaggle datasets download youssefelebiary/hand-gesture-landmarks -p ml/dataset/raw --unzip")
        return

    print(f"\nTotal samples: {report['total_samples']}")
    print(f"Feature dimension: {report['feature_dimension']} (Expected landmarks: {report['expected_landmarks']}, Found: {report['found_landmarks']})")
    print(f"Missing values: {report['missing_values']}")
    print(f"Duplicates: {report['duplicates']}")
    
    print("\nLabels:")
    for k, v in report['classes'].items():
        print(f"  {k}: {v}")
        
    print("\nMetadata:")
    for k, v in report['metadata'].items():
        print(f"  {k}: {v} unique values")
        
    print(f"\nCoordinate range: {report['coord_range']}")

if __name__ == "__main__":
    main()
