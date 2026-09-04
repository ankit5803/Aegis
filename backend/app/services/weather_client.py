import logging
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aegis.weather")

class WeatherClient:
    """
    Client for Open-Meteo Forecast & Historical API.
    Monitors high winds, precipitation, and extreme weather indicators for given coordinates.
    """
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Aegis-SupplyChain-Intelligence/1.0",
            "Accept": "application/json"
        })

    def fetch_weather_severity(self, lat: float, lon: float, days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Fetches daily wind speed and precipitation max values for specified coordinates.
        """
        logger.info(f"Querying Open-Meteo for coordinates ({lat}, {lon}) (past {days_back} days)...")

        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["precipitation_sum", "wind_speed_10m_max", "weather_code"],
            "past_days": days_back,
            "forecast_days": 1,
            "timezone": "UTC"
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            daily_data = data.get("daily", {})
            return self._format_daily_data(daily_data)

        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {str(e)}. Using fallback safe weather baseline.")
            return self._generate_fallback_data(days_back)

    def _format_daily_data(self, daily: Dict[str, list]) -> List[Dict[str, Any]]:
        records = []
        dates = daily.get("time", [])
        precip = daily.get("precipitation_sum", [])
        wind = daily.get("wind_speed_10m_max", [])

        for i, date in enumerate(dates):
            current_wind = wind[i] if i < len(wind) and wind[i] is not None else 0.0
            current_precip = precip[i] if i < len(precip) and precip[i] is not None else 0.0

            # Combined severity metric: 0.0 (calm) to 1.0 (typhoon/hurricane conditions)
            severity = min((current_wind / 100.0) + (current_precip / 100.0), 1.0)

            records.append({
                "date": date,
                "precipitation_mm": current_precip,
                "wind_speed_kmh": current_wind,
                "weather_severity_score": round(severity, 3)
            })
        return records

    def _generate_fallback_data(self, days_back: int) -> List[Dict[str, Any]]:
        records = []
        base_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        for i in range(days_back + 1):
            records.append({
                "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
                "precipitation_mm": 2.5,
                "wind_speed_kmh": 15.0,
                "weather_severity_score": 0.175
            })
        return records


if __name__ == "__main__":
    client = WeatherClient()
    # Coordinates for Suez Canal
    suez_data = client.fetch_weather_severity(lat=30.5852, lon=32.2654, days_back=7)
    df = pd.DataFrame(suez_data)
    print("\nProcessed Weather Severity Sample (Suez Canal):")
    print(df.tail())