from pydantic import BaseModel, Field
from typing import List

class PredictionRequest(BaseModel):
    features: List[float] = Field(..., min_length=63, max_length=63)

class PredictionResponse(BaseModel):
    gesture: str | None
    confidence: float
    hand_detected: bool
