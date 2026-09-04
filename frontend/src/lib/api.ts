// frontend/src/lib/api.ts

export interface Hub {
  id: string;
  name: string;
  country_code: string;
  portwatch_id: string;
  coordinates: { lat: number; lon: number };
}

export interface PredictionData {
  hub_id: string;
  hub_name: string;
  timestamp: string;
  status: string;
  anomaly_score: number;
  features: Record<string, number>;
  shap_contributions: Record<string, number>;
  recommendation: string;
}

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "https://aegis-5qdc.onrender.com/api/v1";

export async function fetchHubs(): Promise<{ hubs: Hub[] }> {
  const res = await fetch(`${API_BASE}/hubs`);
  if (!res.ok) throw new Error("Failed to fetch hubs");
  return res.json();
}

export async function fetchPrediction(hubId: string): Promise<PredictionData> {
  const res = await fetch(`${API_BASE}/predict/${hubId}`);
  if (!res.ok) throw new Error("Failed to fetch prediction");
  return res.json();
}
