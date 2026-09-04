# AEGIS // Enterprise Supply Chain Disruption Intelligence Platform

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
- **Deployment:** Docker, Hugging Face Spaces

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
git clone [https://github.com/your-username/aegis.git](https://github.com/your-username/aegis.git)
cd aegis
```

2. Set Up the Python Backend

# Create and activate virtual environment

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\Activate

# Install dependencies

pip install -r requirements.txt

# Train the Unsupervised Model & Generate Artifacts

python backend/app/core/train.py

# Start the FastAPI Server

python -m uvicorn backend.app.main:app --port 8000

3. Set Up the Next.js Frontend

cd frontend
npm install
npm run dev

🧪 Model Validation & Stress Testing
To validate the unsupervised model's responsiveness without traditional labeled test sets, Aegis features a scenario stress-testing suite (backend/app/core/evaluate.py):

Perfect Sunny Day (Baseline): 16.9/100 ➔ 🟢 NORMAL

Category 5 Hurricane: 93.5/100 ➔ 🚨 CRITICAL ANOMALY

Port Riots & Strikes: 92.5/100 ➔ 🚨 CRITICAL ANOMALY

Run the evaluation suite locally:

Bash
python backend/app/core/evaluate.py
