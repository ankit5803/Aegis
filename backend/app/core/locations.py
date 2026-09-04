# backend/app/core/locations.py

SUPPLY_CHAIN_HUBS = {
    "US_LAX": {
        "id": "US_LAX",
        "name": "Port of Los Angeles",
        "country_code": "US",
        "portwatch_id": "USA_LAX",
        "coordinates": {"lat": 33.7285, "lon": -118.2620}
    },
    "CN_SHA": {
        "id": "CN_SHA",
        "name": "Port of Shanghai",
        "country_code": "CH",
        "portwatch_id": "CHN_SHA",
        "coordinates": {"lat": 31.2222, "lon": 121.4581}
    },
    "SG_SIN": {
        "id": "SG_SIN",
        "name": "Port of Singapore",
        "country_code": "SN",
        "portwatch_id": "SGP_SIN",
        "coordinates": {"lat": 1.29027, "lon": 103.851959}
    },
    "EG_SUE": {
        "id": "EG_SUE",
        "name": "Suez Canal (Maritime Chokepoint)",
        "country_code": "EG",
        "portwatch_id": "EGY_SUEZ",
        "coordinates": {"lat": 30.5852, "lon": 32.2654}
    },
    "NL_RTM": {
        "id": "NL_RTM",
        "name": "Port of Rotterdam",
        "country_code": "NL",
        "portwatch_id": "NLD_RTM",
        "coordinates": {"lat": 51.9496, "lon": 4.1454}
    },
    "PA_PAN": {
        "id": "PA_PAN",
        "name": "Panama Canal (Maritime Chokepoint)",
        "country_code": "PM",
        "portwatch_id": "PAN_CANAL",
        "coordinates": {"lat": 9.0800, "lon": -79.6800}
    }
}

def get_hub(hub_id: str):
    return SUPPLY_CHAIN_HUBS.get(hub_id, SUPPLY_CHAIN_HUBS["US_LAX"])

def list_all_hubs():
    return list(SUPPLY_CHAIN_HUBS.values())