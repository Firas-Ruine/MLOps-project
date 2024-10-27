from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# Model and Data Paths (from environment variables or default values)
MODEL_PATH = os.getenv("MODEL_PATH", "/src/models/saved_model/model.pkl")
DATA_PATH = os.getenv("DATA_PATH", "/data/processed")

# Load the model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")

# Define the input data structure
class PredictionRequest(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    # Add other features as needed

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML Model API"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Parse input data
    input_data = pd.DataFrame([request.dict()])

    # Run prediction
    try:
        prediction = model.predict(input_data)
        confidence = max(model.predict_proba(input_data)[0])  # Example confidence
        return PredictionResponse(prediction=prediction[0], confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
