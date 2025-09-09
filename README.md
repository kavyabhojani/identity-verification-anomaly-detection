# Identity Verification Anomaly Detection (In Progress)

## Overview
This project explores **identity verification anomaly detection** using supervised machine learning on synthetic login datasets.  
The goal is to flag suspicious behaviors such as **device mismatch**, **geographic variance**, and **unusual login patterns** that could indicate account takeover or fraud.  

The work is framed in a **client-facing Proof of Value (PoV)** style, demonstrating not just technical accuracy but also clear business communication — similar to what financial clients (e.g., Mastercard’s fraud prevention teams) expect.

---

## Key Features
- **Synthetic Login Dataset**  
  - Generated with realistic user, device, and geo patterns  
  - Includes injected anomalies (device swap, geo jumps, rapid logins)

- **SQL-Driven Feature Engineering**  
  - Features like `unique_devices_per_user`, `geo_entropy`, `time_variance`  
  - SQL queries (DuckDB/SQLite) to mimic enterprise-scale pipelines

- **Supervised Modeling (scikit-learn)**  
  - Logistic Regression, Random Forest, XGBoost baselines  
  - Evaluation with precision/recall for fraud-sensitive domains

- **Explainability with SHAP**  
  - Model decisions explained at feature-level  
  - Example: “Unusual geo variance added +0.42 to risk score”

- **Client-Style Reporting**  
  - `reports/design_doc.md`: technical design & pipeline  
  - `reports/pov_summary.pdf`: business-oriented PoV summary  

---

## Tech Stack
- **Python**: data simulation, modeling, SHAP  
- **SQL (DuckDB/SQLite)**: feature engineering  
- **scikit-learn / XGBoost**: model training & evaluation  
- **SHAP**: explainability  
- **Jupyter Notebooks**: exploration & visualization  

---

## Repository Structure
- identity-verification-anomaly-detection/
- │
- ├── data/ # Synthetic dataset generator + samples
- ├── notebooks/ # Exploration & model training
- ├── src/
- │ ├── features/ # SQL + Python feature engineering scripts
- │ ├── models/ # Training, evaluation, SHAP explainability
- │ └── utils/ # Helper functions
- │
- ├── reports/
- │ ├── design_doc.md # Client-style design doc
- │ ├── pov_summary.pdf # Proof of Value summary
- │
- ├── requirements.txt
- └── README.md

---

## Business Value
- **Reduces fraud risk** by identifying anomalies before transaction approval.  
- **Improves customer trust** with explainable AI (transparent risk scoring).  
- **Demonstrates PoV delivery**: quick, actionable prototype for client stakeholders.  

---

## Next Steps
- Expand dataset with time-series patterns (e.g., login streaks, velocity).  
- Deploy model as an API (FastAPI/Flask) for real-time scoring demo.  
- Add Streamlit dashboard for interactive anomaly visualization.  
