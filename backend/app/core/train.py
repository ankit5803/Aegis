import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import shap

# Model artifact directory
ARTIFACT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../backend/model")
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def generate_normal_baseline_data(samples: int = 5000) -> pd.DataFrame:
    """
    Generates historical data representing 'NORMAL' operational states.
    Unsupervised models learn what 'normal' looks like so they can flag the weird stuff.
    """
    np.random.seed(42)

    # In a normal state, ports are busy (low drop pct, moderate congestion), 
    # news risk is baseline, and weather is typical.
    df = pd.DataFrame({
        "port_congestion_score": np.clip(np.random.normal(0.3, 0.1, samples), 0, 1),
        "port_7d_rolling_avg": np.clip(np.random.normal(0.3, 0.08, samples), 0, 1),
        "port_volume_drop_pct": np.clip(np.random.exponential(0.02, samples), 0, 1), # Very low drops normally
        "news_risk_score": np.clip(np.random.beta(2, 8, samples), 0, 1), # Mostly quiet news
        "weather_severity_score": np.clip(np.random.beta(1.5, 8, samples), 0, 1), # Normal weather
        "weather_7d_max": np.clip(np.random.beta(2, 6, samples), 0, 1)
    })

    return df

def train_anomaly_detector():
    print("[1/4] Generating unsupervised baseline dataset (Normal Operations)...")
    df_normal = generate_normal_baseline_data(samples=5000)
    
    feature_cols = list(df_normal.columns)

    print("[2/4] Training Isolation Forest (Anomaly Detector)...")
    # Isolation Forest isolates observations by randomly selecting a feature and then randomly selecting a split value.
    # Anomalies (disruptions) require fewer splits to be isolated.
    model = IsolationForest(
        n_estimators=150, 
        max_samples='auto', 
        contamination=0.05, # We assume 5% of future real-world data might be anomalous
        random_state=42
    )
    
    model.fit(df_normal)

    print("[3/4] Fitting SHAP TreeExplainer for Anomaly Explainability...")
    # TreeExplainer works beautifully with Isolation Forests to explain *why* something is an anomaly
    explainer = shap.TreeExplainer(model)

    print(f"[4/4] Saving Anomaly Engine artifacts to {ARTIFACT_DIR}...")
    joblib.dump(model, os.path.join(ARTIFACT_DIR, "aegis_isolation_forest.pkl"))
    joblib.dump(explainer, os.path.join(ARTIFACT_DIR, "aegis_shap_explainer.pkl"))
    joblib.dump(feature_cols, os.path.join(ARTIFACT_DIR, "feature_columns.pkl"))

    print("\nTraining & artifact serialization complete! Aegis is now an Unsupervised Intelligence Platform.")

if __name__ == "__main__":
    train_anomaly_detector()