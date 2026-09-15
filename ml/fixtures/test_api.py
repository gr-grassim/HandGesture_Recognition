import requests
import json
import os

with open(os.path.join(os.path.dirname(__file__), 'landmark_fixture.json'), 'r') as f:
    data = json.load(f)

print("Testing /api/model-info")
info = requests.get('http://localhost:8000/api/model-info').json()
print(info)

print("\nTesting /api/predict")
resp = requests.post('http://localhost:8000/api/predict', json=data)
print(resp.json())
