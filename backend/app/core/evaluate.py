import os
import joblib
import pandas as pd

# 1. Load the Model
ARTIFACT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../backend/model")
model = joblib.load(os.path.join(ARTIFACT_DIR, "aegis_isolation_forest.pkl"))
feature_cols = joblib.load(os.path.join(ARTIFACT_DIR, "feature_columns.pkl"))

# 2. Define Explicit Test Scenarios
scenarios = [
    {
        "name": "Scenario A: Perfect Sunny Day (Should be NORMAL)",
        "features": [0.2, 0.2, 0.0, 0.1, 0.1, 0.1] # Low congestion, no drops, no news, no weather
    },
    {
        "name": "Scenario B: Category 5 Hurricane (Should be CRITICAL)",
        "features": [0.4, 0.3, 0.4, 0.1, 0.95, 0.95] # Massive weather spike, volume dropping
    },
    {
        "name": "Scenario C: Sudden Port Strike & Riots (Should be CRITICAL)",
        "features": [0.8, 0.4, 0.6, 0.85, 0.2, 0.2] # Massive news risk, high congestion, volume dropping
    },
    {
        "name": "Scenario D: Minor Operational Hiccup (Should be ELEVATED/NORMAL)",
        "features": [0.5, 0.4, 0.1, 0.3, 0.3, 0.3] # Slightly busy, minor bad weather, nothing extreme
    }
]

print("\n--- AEGIS MODEL STRESS TEST ---")

for s in scenarios:
    # Format as DataFrame
    df = pd.DataFrame([s["features"]], columns=feature_cols)
    
    # Predict
    prediction = model.predict(df)[0]
    raw_score = model.decision_function(df)[0]
    base_risk = (0.2 - raw_score) * 150
    
    if prediction == -1:
        risk_score = round(max(75.0, min(100.0, base_risk + 40)), 1)
        status = "🚨 ANOMALY"
    else:
        risk_score = round(max(0.0, min(70.0, base_risk)), 1)
        status = "🟢 NORMAL"
        
    print(f"\n{s['name']}")
    print(f"Risk Score: {risk_score}/100")
    print(f"Model Verdict: {status}")

print("\n-------------------------------")