# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.endpoints import predict
from backend.app.core.locations import list_all_hubs

app = FastAPI(
    title="Aegis Supply Chain Intelligence API",
    description="Enterprise API for real-time disruption prediction and anomaly detection.",
    version="1.0.0"
)

# Allowed origins for local development and live Vercel production frontend
origins = [
    "http://localhost:3000",
    "https://frontend-sage-beta-68.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the prediction endpoints
app.include_router(predict.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "online", "system": "Aegis Intelligence Platform"}

@app.get("/api/v1/hubs")
def get_hubs():
    """Returns the list of monitored supply chain hubs."""
    return {"hubs": list_all_hubs()}