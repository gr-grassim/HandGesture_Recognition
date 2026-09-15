import json
import os
import pytest
from app.vision.landmark_processor import extract_features

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), '../../ml/fixtures/landmark_fixture.json')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '../../ml/fixtures/expected_features.json')

def test_extract_features():
    with open(FIXTURE_PATH, 'r') as f:
        data = json.load(f)
    
    landmarks = data['landmarks']
    features = extract_features(landmarks)
    
    assert len(features) == 63
    
    # Save the output to expected_features.json so JS can test against it
    with open(OUTPUT_PATH, 'w') as f:
        json.dump({"features": features}, f)

def test_extract_features_validation():
    with pytest.raises(ValueError):
        extract_features([])
