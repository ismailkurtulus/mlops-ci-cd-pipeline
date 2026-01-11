from fastapi import FastAPI
from pydantic import BaseModel
import antigravity
from app.feature_engineering import hashed_bucket

app = FastAPI()

class PredictRequest(BaseModel):
    user_id: str
    item_id: str

@app.post("/predict")
def predict(req: PredictRequest):
    x = f"{req.user_id}:{req.item_id}"
    pred = hashed_bucket(x, 1000)
    return {"prediction": pred}
