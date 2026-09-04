# PROJECT CONTEXT: AEGIS

## 1. Executive Summary

- **Project Name:** Aegis
- **Domain:** Enterprise Global Supply Chain Disruption & Early Warning Intelligence Platform
- **Mission:** Predict global supply chain bottlenecks and disruptions up to 72 hours in advance using public real-time data feeds, providing risk scores, incident change logs, and automated mitigation playbooks for supply chain operators.

---

## 2. The Machine Learning Architecture Pivot (The "CV Flex")

Real-world supply chain disruption data (ground truth labels) is highly proprietary and costs millions of dollars to license. Instead of fabricating a circularly-labeled dataset to force a supervised model (like XGBoost) to work, Aegis uses an **Unsupervised Anomaly Detection** architecture.

- **The Engine:** We use an **Isolation Forest** trained purely on the "normal" multivariate operational rhythm of global maritime chokepoints.
- **The Logic:** By establishing a baseline of normal vessel traffic, typical weather patterns, and baseline geopolitical news, the model isolates and flags statistical anomalies (e.g., a sudden 15% drop in Suez vessels aligning with a spike in Middle Eastern GDELT unrest).
- **The Explainability:** The anomaly engine is wrapped in a **SHAP TreeExplainer**. When a port is flagged as an anomaly, SHAP calculates the exact feature contributions, giving human operators transparent, actionable intelligence (e.g., "Flagged High Risk due to: 60% Weather Severity, 40% Port Congestion").

---

## 3. System Architecture & Tech Stack

### Frontend (User Presentation Layer)

- **Framework:** Next.js (App Router, TypeScript)
- **Styling:** Tailwind CSS, Lucide Icons, Shadcn-style component patterns
- **Hosting:** Vercel
- **Key Features:** Global risk heatmap/matrix, real-time disruption audit log, SHAP feature attribution drawer, AI-driven mitigation advisor.

### Backend (Intelligence & MLOps Layer)

- **Framework:** FastAPI (Python 3.11+)
- **Hosting:** Hugging Face Spaces (Docker / Python Runtime)
- **Machine Learning:** Scikit-Learn (Isolation Forest)
- **Model Explainability:** SHAP (TreeExplainer)
- **Core Tasks:** Multi-source data ingestion, rolling feature engineering (lag, moving averages), anomaly scoring, and recommendation generation.

---

## 4. Data Signal Ingestion Matrix

| Signal Source          | Metric / Feature Extracted                              | Strategic Value                                                                      |
| ---------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **IMF Portwatch API**  | Vessel calls, trade volume index, chokepoint congestion | Direct operational signal; sudden drop in vessel count indicates avoidance/blockage. |
| **GDELT Project**      | CAMEO event codes (strikes, sanctions, protests)        | Leading geopolitical indicator; labor unrest and embargoes precede physical delays.  |
| **Open-Meteo API**     | Wind speed, extreme precipitation, weather codes        | Environmental shock signal; storms/typhoons force immediate port closures.           |
| **Time-Series Engine** | 7-day rolling averages, rate-of-change indicators       | Captures momentum and standardizes seasonal variations.                              |

---

## 5. Risk Classification Tiers (Based on Anomaly Scores)

- **🚨 CRITICAL (Severe Anomaly):** Immediate operational contingency activation (reroute shipments, draw emergency safety stock).
- **⚠️ HIGH (Moderate Anomaly):** Priority monitoring, procurement alert, buffer inventory adjustments.
- **🟡 MEDIUM (Minor Deviation):** Routine review in operational standups.
- **🟢 LOW (Normal Baseline):** Standard operational flow.

---

## 6. Incremental Build Roadmap

- [x] **Step 1: Environment & Dependency Setup**
- [x] **Step 2: Core Data Fetchers** (Portwatch, GDELT, Open-Meteo with local baselines).
- [x] **Step 3: Feature Matrix & Time-Series Engine** (Unifying APIs, calculating 7-day lags).
- [x] **Step 4: ML Architecture & Training** (Trained Isolation Forest for unsupervised anomaly detection + SHAP explainability).
- [ ] **Step 5: FastAPI Backend & Inference Engine** _(Next Step)_
  - Load ML artifacts, build `/predict` and `/recommendations` API endpoints.
- [ ] **Step 6: Next.js Frontend Development**
  - Real-time dashboard, log drawer, mitigation playbooks.
- [ ] **Step 7: Production Deployment**
  - Hugging Face Spaces (Backend) + Vercel (Frontend).
