import logging
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Any
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))

from backend.app.core.locations import get_hub
from backend.app.services.portwatch_client import PortwatchClient
from backend.app.services.gdelt_client import GDELTClient
from backend.app.services.weather_client import WeatherClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aegis.feature_engine")

class FeatureEngine:
    """
    Coordinates data ingestion across Portwatch, GDELT, and Open-Meteo,
    computes time-series rolling features, and builds inference-ready feature vectors.
    """
    def __init__(self):
        self.portwatch = PortwatchClient()
        self.gdelt = GDELTClient()
        self.weather = WeatherClient()

    def build_features_for_hub(self, hub_id: str) -> Dict[str, Any]:
        hub = get_hub(hub_id)
        logger.info(f"Synthesizing features for {hub['name']} ({hub['id']})...")

        # 1. Fetch Portwatch vessel data (last 14 days for rolling calculations)
        raw_ports = self.portwatch.fetch_raw_congestion_data(
            port_id=hub["portwatch_id"],
            port_name=hub["name"],
            days_back=14
        )
        port_df = self.portwatch.process_congestion_scores(raw_ports)

        # 2. Fetch GDELT geopolitical news risk (last 7 days)
        raw_news = self.gdelt.fetch_geopolitical_events(
            country_code=hub["country_code"],
            days_back=7
        )
        news_df = self.gdelt.process_news_risk(raw_news, country_code=hub["country_code"])

        # 3. Fetch Open-Meteo weather metrics (last 7 days)
        weather_data = self.weather.fetch_weather_severity(
            lat=hub["coordinates"]["lat"],
            lon=hub["coordinates"]["lon"],
            days_back=7
        )
        weather_df = pd.DataFrame(weather_data)

        # 4. Extract current day snapshots
        current_port_score = float(port_df["port_congestion_score"].iloc[-1]) if not port_df.empty else 0.2
        current_news_score = float(news_df["news_risk_score"].iloc[-1]) if not news_df.empty else 0.1
        current_weather_score = float(weather_df["weather_severity_score"].iloc[-1]) if not weather_df.empty else 0.1

        # 5. Calculate 7-day rolling momentum features
        port_7d_rolling = float(port_df["port_congestion_score"].tail(7).mean()) if not port_df.empty else current_port_score
        port_volume_drop_pct = 0.0
        if len(port_df) >= 7 and "vessel_count" in port_df.columns:
            recent_avg = port_df["vessel_count"].tail(3).mean()
            prior_avg = port_df["vessel_count"].head(7).mean()
            if prior_avg > 0:
                port_volume_drop_pct = max(0.0, float((prior_avg - recent_avg) / prior_avg))

        weather_7d_max = float(weather_df["weather_severity_score"].tail(7).max()) if not weather_df.empty else current_weather_score

        feature_payload = {
            "hub_id": hub["id"],
            "hub_name": hub["name"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "port_congestion_score": round(current_port_score, 3),
            "port_7d_rolling_avg": round(port_7d_rolling, 3),
            "port_volume_drop_pct": round(port_volume_drop_pct, 3),
            "news_risk_score": round(current_news_score, 3),
            "weather_severity_score": round(current_weather_score, 3),
            "weather_7d_max": round(weather_7d_max, 3)
        }

        logger.info(f"Generated feature vector for {hub_id}: {feature_payload}")
        return feature_payload


if __name__ == "__main__":
    engine = FeatureEngine()
    features = engine.build_features_for_hub("EG_SUE")
    print("\nUnified Feature Payload (Suez Canal):")
    for k, v in features.items():
        print(f"  {k}: {v}")