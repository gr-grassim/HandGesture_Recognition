from fastapi import APIRouter, HTTPException
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.ml.predictor import predict_gesture
from app.ml.model_loader import model_loader

router = APIRouter(prefix="/api")

@router.get("/model-info")
def get_model_info():
    if not model_loader.metadata:
        raise HTTPException(status_code=404, detail="Model metadata not found")
    return model_loader.metadata

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        result = predict_gesture(request.features)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
