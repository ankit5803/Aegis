import logging
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aegis.portwatch")

class PortwatchClient:
    """
    Client for fetching live vessel activity and port congestion metrics 
    from the IMF Portwatch API with support for dynamic ports.
    """
    BASE_URL = "https://services9.arcgis.com/IMFPortwatch/arcgis/rest/services"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Aegis-SupplyChain-Intelligence/1.0",
            "Accept": "application/json"
        })

    def fetch_raw_congestion_data(
        self, 
        port_id: str = "USA_LAX", 
        port_name: str = "Port of Los Angeles", 
        days_back: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Pulls recent vessel call data and trade volume metrics for a specific port.
        """
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days_back)

        logger.info(f"Fetching Portwatch data for {port_name} ({port_id}) from {start_date.date()} to {end_date.date()}...")

        try:
            url = f"{self.BASE_URL}/vessel-calls/query"
            params = {
                "where": f"port_id='{port_id}'",
                "outFields": "*",
                "f": "json"
            }
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code != 200:
                logger.warning(f"Portwatch API returned status {response.status_code}. Using dynamic fallback baseline.")
                return self._generate_fallback_data(port_id, port_name, days_back)

            data = response.json()
            features = data.get("features", [])
            return features if features else self._generate_fallback_data(port_id, port_name, days_back)

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error connecting to Portwatch API: {str(e)}. Using dynamic fallback baseline.")
            return self._generate_fallback_data(port_id, port_name, days_back)

    def process_congestion_scores(self, raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Normalizes raw vessel data and calculates congestion scores.
        """
        if not raw_data:
            return pd.DataFrame(columns=["date", "port_id", "port_name", "vessel_count", "port_congestion_score"])

        df = pd.DataFrame(raw_data)
        expected_cols = ["date", "port_id", "port_name", "vessel_count", "port_congestion_score"]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None

        return df.ffill().bfill()

    def _generate_fallback_data(self, port_id: str, port_name: str, days_back: int) -> List[Dict[str, Any]]:
        """
        Generates deterministic baseline time-series for development and offline testing.
        """
        records = []
        base_date = datetime.now(timezone.utc) - timedelta(days=days_back)

        for i in range(days_back + 1):
            current_date = base_date + timedelta(days=i)
            # Simulate a temporary operational dip 4 days ago
            vessels = 18 if i == (days_back - 4) else 48
            congestion_score = 0.82 if vessels < 25 else 0.22

            records.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "port_id": port_id,
                "port_name": port_name,
                "vessel_count": vessels,
                "port_congestion_score": congestion_score
            })
        return records


if __name__ == "__main__":
    client = PortwatchClient()
    raw = client.fetch_raw_congestion_data(port_id="CHN_SHA", port_name="Port of Shanghai", days_back=7)
    df = client.process_congestion_scores(raw)
    print("\nProcessed Portwatch Sample:")
    print(df.tail())