import numpy as np
from sklearn.model_selection import train_test_split

def perform_split(X, y, random_state=42):
    """
    Splits data into 70% Train, 15% Validation, 15% Test.
    Since we lack grouping metadata from the generic Numpy array, 
    we use stratified splitting as a fallback.
    """
    # First split: 70% train, 30% temp (for val + test)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=random_state, stratify=y
    )
    
    # Second split: split the 30% into 15% val and 15% test
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=random_state, stratify=y_temp
    )
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)
