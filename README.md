# AEGIS // Enterprise Supply Chain Disruption Intelligence Platform

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.100%2B-005571?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Next.js-14%2B-black?style=for-the-badge&logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/Scikit_Learn-Isolation_Forest-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/SHAP-TreeExplainer-8A2BE2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=black" />
  <img src="https://img.shields.io/badge/Vercel-Deployed-black?style=for-the-badge&logo=vercel&logoColor=white" />
</p>

> An unsupervised, multi-signal predictive intelligence engine designed to forecast maritime and supply chain bottlenecks up to 72 hours in advance using real-time global telemetry.

---

## 🏛️ Executive Summary

Global supply chain disruptions cost enterprises billions annually, yet proprietary ground-truth disruption labels are prohibitively expensive or unavailable. **Aegis** solves this challenge by implementing an **Unsupervised Anomaly Detection** architecture.

Rather than relying on fragile, circularly-labeled datasets, Aegis learns the "normal" multivariate operational rhythm of global maritime chokepoints using an **Isolation Forest**, paired with **SHAP (SHapley Additive exPlanations)** to give logistics operators transparent, explainable root-cause risk attributes.

---

## 🚀 Core Architecture & Tech Stack

### Intelligence & MLOps Layer (Backend)

- **Framework:** FastAPI (Python 3.11+)
- **Unsupervised Learning:** Scikit-Learn (Isolation Forest)
- **Model Explainability:** SHAP TreeExplainer
- **Hosting:** Render (Cloud Web Service)

### Presentation & Decision Layer (Frontend)

- **Framework:** Next.js (App Router, TypeScript)
- **Styling:** Tailwind CSS, Lucide Icons
- **Data Visualization:** Recharts (SHAP Feature Attribution Matrix)
- **Hosting:** Vercel

---

## 📊 Data Signal Ingestion Matrix

Aegis aggregates and standardizes heterogeneous live data streams across global trade arteries:

| Signal Source          | Extracted Metric                                        | Strategic Role                                                           |
| ---------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------ |
| **IMF Portwatch API**  | Vessel calls, trade volume index, chokepoint congestion | Direct operational signal tracking maritime traffic flow.                |
| **GDELT Project**      | CAMEO event codes, strikes, sanctions, protests         | Leading geopolitical indicator detecting civil unrest and labor strikes. |
| **Open-Meteo API**     | Wind speed, extreme precipitation, weather codes        | Environmental shock signal tracking severe weather and port closures.    |
| **Time-Series Engine** | 7-day rolling averages, moving velocity metrics         | Standardizes seasonal variations and momentum tracking.                  |

---

## 🛠️ Local Installation & Development

### 1. Clone the Repository

```bash
git clone [https://github.com/ankit5803/Aegis.git](https://github.com/ankit5803/Aegis.git)
cd Aegis
```

### 2. Set Up the Python Backend

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Train the Unsupervised Model & Generate Artifacts
python backend/app/core/train.py

# Start the FastAPI Server
python -m uvicorn backend.app.main:app --port 8000
```

### 3. Set Up the Next.js Frontend

```bash
cd frontend
npm install
npm run dev
Access the executive command center locally at http://localhost:3000.
```

🧪 Model Validation & Stress Testing
To validate the unsupervised model's responsiveness without traditional labeled test sets, Aegis features a rigorous scenario stress-testing suite (backend/app/core/evaluate.py):

Perfect Sunny Day (Baseline): 16.9/100 ➔ 🟢 NORMAL

Category 5 Hurricane: 93.5/100 ➔ 🚨 CRITICAL ANOMALY

Port Riots & Strikes: 92.5/100 ➔ 🚨 CRITICAL ANOMALY

Run the evaluation suite locally:

```bash
python backend/app/core/evaluate.py
```
