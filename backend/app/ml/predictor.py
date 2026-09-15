from app.ml.model_loader import model_loader
import numpy as np

def predict_gesture(features, confidence_threshold=0.60):
    if not features:
        return {"gesture": None, "confidence": 0.0, "hand_detected": False}
        
    if not model_loader.model:
        raise ValueError("Model is not loaded")

    X = np.array(features).reshape(1, -1)
    
    probabilities = model_loader.model.predict_proba(X)[0]
    max_prob = np.max(probabilities)
    class_idx = np.argmax(probabilities)
    
    predicted_class = model_loader.model.classes_[class_idx]
    
    if max_prob < confidence_threshold:
        return {"gesture": "UNKNOWN", "confidence": float(max_prob), "hand_detected": True}
        
    return {"gesture": predicted_class, "confidence": float(max_prob), "hand_detected": True}
