# backend/api/app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from model_training.model import ExamPredictor
from .schemas import PredictRequest, PredictResponse
import joblib
import os

app = FastAPI(title="Exam Result Predictor")

# Allow CORS for frontend
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === FIXED FILE PATHS ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
encoder_path = os.path.join(BASE_DIR, "encoder.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")
model_weights_path = os.path.join(BASE_DIR, "exam_predictor_weights.pth")

# Load encoder and scaler
enc = joblib.load(encoder_path)
scaler = joblib.load(scaler_path)

# Load model
# only categorical sample to infer enc.feature count
sample_input = [["female", "group B", "bachelor's degree", "standard", "completed"]]
input_dim = 2 + enc.transform(sample_input).shape[1]  # 2 numeric + cat‐onehot
model = ExamPredictor(input_dim=input_dim)
model.load_state_dict(torch.load(model_weights_path))
model.eval()

# In-memory prediction history
history: list[PredictResponse] = []

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        # numeric inputs: reading + writing
        X_num = np.array([[req.reading_score, req.writing_score]])
        X_num_scaled = scaler.transform(X_num)

        # categorical inputs
        X_cat = np.array([[req.gender,
                           req.race_ethnicity,
                           req.parental_level_of_education,
                           req.lunch,
                           req.test_preparation_course]])
        X_cat_encoded = enc.transform(X_cat)

        # combine & predict
        x = torch.tensor(np.hstack([X_num_scaled, X_cat_encoded]), dtype=torch.float32)
        pred = float(model(x).item())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    resp = PredictResponse(predicted_score=pred)
    history.append(resp)
    return resp

@app.get("/history", response_model=list[PredictResponse])
def get_history():
    return history
