import os
import pandas as pd
import numpy as np

def generate_synthetic_dataset():
    # 21 landmarks * 3 coords = 63 columns
    columns = ['label'] + [f'v{i}' for i in range(63)]
    
    classes = ['open', 'close', 'peace'] # Kaggle raw labels before mapping
    num_samples_per_class = 200
    
    data = []
    
    np.random.seed(42)
    
    for cls in classes:
        for _ in range(num_samples_per_class):
            # Generate random landmarks. 
            # We add some class-specific bias just so the Random Forest can learn something.
            if cls == 'open':
                bias = 0.5
            elif cls == 'close':
                bias = 0.1
            else:
                bias = 0.8
                
            features = np.random.normal(loc=bias, scale=0.1, size=63)
            row = [cls] + features.tolist()
            data.append(row)
            
    df = pd.DataFrame(data, columns=columns)
    
    out_dir = os.path.join(os.path.dirname(__file__), '../dataset/raw')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'hand_gesture_landmarks.csv')
    
    df.to_csv(out_path, index=False)
    print(f"Synthetic dataset created at {out_path} with {len(df)} samples.")

if __name__ == '__main__':
    generate_synthetic_dataset()
