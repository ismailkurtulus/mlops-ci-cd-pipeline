import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.datasource import get_user_profile
from src.feature_engineering import build_features
from src.model import ToyModel


def get_db_path() -> str:
    return os.getenv("DB_PATH", "/app/db/app.db")


app = FastAPI(title="High-Cardinality Prediction Service", version="1.0.0")
model = ToyModel(num_buckets=100)


class PredictRequest(BaseModel):
    user_id: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    db_path = get_db_path()
    profile = get_user_profile(db_path, req.user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="user not found")

    feats = build_features(profile, num_buckets=100)
    proba = model.predict_proba(feats)
    pred = 1 if proba >= 0.5 else 0

    return {
        "user_id": req.user_id,
        "prediction": pred,
        "proba": round(proba, 6),
        "features": feats,
    }
