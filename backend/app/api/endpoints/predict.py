import os
import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from backend.app.services.feature_engine import FeatureEngine
from backend.app.core.locations import get_hub

router = APIRouter()
feature_engine = FeatureEngine()

# Pre-load the ML artifacts on startup
ARTIFACT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../backend/model")

try:
    model = joblib.load(os.path.join(ARTIFACT_DIR, "aegis_isolation_forest.pkl"))
    explainer = joblib.load(os.path.join(ARTIFACT_DIR, "aegis_shap_explainer.pkl"))
    feature_cols = joblib.load(os.path.join(ARTIFACT_DIR, "feature_columns.pkl"))
except Exception as e:
    print(f"Failed to load ML artifacts: {e}")
    model = None

class PredictionResponse(BaseModel):
    hub_id: str
    hub_name: str
    timestamp: str
    status: str
    anomaly_score: float
    features: Dict[str, Any]
    shap_contributions: Dict[str, float]
    recommendation: str

@router.get("/predict/{hub_id}", response_model=PredictionResponse)
def get_prediction(hub_id: str):
    if model is None:
        raise HTTPException(status_code=500, detail="Machine learning artifacts not loaded.")

    try:
        # 1. Fetch live features
        features = feature_engine.build_features_for_hub(hub_id)
        
        # 2. Prepare DataFrame for inference
        df_infer = pd.DataFrame([{col: features.get(col, 0.0) for col in feature_cols}])
        
        # 3. Score Anomaly 
        # Isolation forest returns 1 for inliers (normal) and -1 for outliers (anomalies)
        prediction = model.predict(df_infer)[0]
        raw_score = model.decision_function(df_infer)[0]
        
        # Calculate base risk
        base_risk = (0.2 - raw_score) * 150
        
        # Force alignment: If it's a strict anomaly, ensure the score is 75+
        if prediction == -1:
            risk_score = round(max(75.0, min(100.0, base_risk + 40)), 1)
        else:
            risk_score = round(max(0.0, min(70.0, base_risk)), 1)
            
        status = "🟢 NORMAL"
        recommendation = "Maintain standard operations."
        
        if risk_score >= 75:
            status = "🚨 CRITICAL ANOMALY"
            recommendation = "Immediate Action: Reroute shipments and assess alternative sourcing."
        elif risk_score >= 40:
            status = "⚠️ ELEVATED RISK"
            recommendation = "Monitor Closely: Buffer safety stock for components moving through this hub."

        # 4. Generate SHAP explanations
        shap_values = explainer.shap_values(df_infer)
        
        # Format SHAP values cleanly for the frontend
        contributions = {}
        for idx, col_name in enumerate(feature_cols):
            # IsolationForest SHAP values format varies slightly by version, 
            # usually shap_values[0] accesses the array for the first instance
            val = float(shap_values[idx] if len(shap_values.shape) == 1 else shap_values[0][idx])
            contributions[col_name] = round(val, 3)

        return PredictionResponse(
            hub_id=features["hub_id"],
            hub_name=features["hub_name"],
            timestamp=features["timestamp"],
            status=status,
            anomaly_score=risk_score,
            features={k: v for k, v in features.items() if k in feature_cols},
            shap_contributions=contributions,
            recommendation=recommendation
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))