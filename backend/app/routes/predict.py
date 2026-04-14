from fastapi import APIRouter
from app.services.ml_model import predict_code_metrics
from app.models.schema import CodeInput

router = APIRouter()

@router.post("/predict")
def predict(data: CodeInput):
    return predict_code_metrics(data.code)