from fastapi import FastAPI
import pandas as pd
import joblib
from pathlib import Path
import uvicorn
from pydantic import BaseModel
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from src.feature_extract import feature_extraction
from pycaret.classification import ClassificationExperiment
from pycaret.classification import load_model, predict_model



exp = ClassificationExperiment()

model_path = Path(__file__).parent.parent / 'models' / 'extra_tree_v3'

pipeline = load_model(str(model_path))

class URL(BaseModel):
    domain: str

app = FastAPI()



@app.post("/predict")
def predict(data: URL):
    df = pd.DataFrame([{'domain':data.domain}])
    features = feature_extraction(df)
    prediction_df = predict_model(pipeline, data=features, probability_threshold=0.6)
    label = prediction_df['prediction_label'].iloc[0]
    score = prediction_df['prediction_score'].iloc[0]

    output = 'Benign' if label == 0 else 'Malicious'

    return {"prediction": output}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host = "0.0.0.0",
        port = 8080

    )