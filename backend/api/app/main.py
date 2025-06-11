from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from model_training.model import ExamPredictor
from .schemas import PredictRequest, PredictResponse
import os
from pathlib import Path

app = FastAPI(title="Exam Result Predictor")

ROOT = Path(__file__).resolve().parents[1] 

origins = [
    "http://localhost:3000",          # Your Next.js dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # cannot be ['*'] if allow_credentials=True
    allow_credentials=True,           # if you send cookies or auth headers
    allow_methods=["*"],              # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],              # allow all request headers
)

# TODO: In production, load enc/scaler from disk
enc = OneHotEncoder(sparse_output=False)

scaler = StandardScaler()

# Instantiate and load model
# Use a dummy transform to infer input_dim
_ = enc.fit_transform([["female","group B","bachelor","standard","completed"]])
model = ExamPredictor(input_dim=2 + _.shape[1])
model.load_state_dict(torch.load("api/exam_predictor_weights.pth"))
model.eval()

history = []

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        # Preprocess numeric
        X_num = np.array([[req.reading_score, req.writing_score]])
        X_num_scl = scaler.transform(X_num)
        # Preprocess categorical
        X_cat = np.array([[req.gender, req.race_ethnicity,
                           req.parental_level_of_education,
                           req.lunch, req.test_preparation_course]])
        X_cat_enc = enc.transform(X_cat)
        # Combine
        x = torch.tensor(np.hstack([X_num_scl, X_cat_enc]), dtype=torch.float32)
        pred = float(model(x).item())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    resp = PredictResponse(predicted_score=pred)
    history.append(resp)
    return resp

@app.get("/history", response_model=list[PredictResponse])
def get_history():
    return history
