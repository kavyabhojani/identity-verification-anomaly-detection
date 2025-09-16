# Design Document — Identity Verification Anomaly Detection (PoV)

## Objective

Detect suspicious login events while minimizing false positives. Provide an explainable, SQL-driven pipeline that can be integrated into customer identity flows.

## Scope

- Synthetic dataset approximating enterprise identity telemetry
- SQL feature engineering (DuckDB) for portability
- Supervised models (LogReg, XGBoost) + SHAP explainability
- Deliverables: models, PR curves, SHAP plots, and business KPIs

## Data

- `users.csv`: user_id, home_country, signup_ts
- `synthetic_logins.csv`: user_id, login_time, device_id, country, ip_address, label

## Features (initial)

- `user_unique_devices_to_date`: rolling count of distinct devices per user
- `secs_since_prev_login`: time delta in seconds
- `is_geo_mismatch`: current country != home_country
- `logins_last_24h`: rolling login velocity

## Modeling

- Baselines: Logistic Regression (balanced class weights), XGBoost
- Metrics: AUC, Precision/Recall, PR AUC
- Target policy: recall-first with threshold tuning per business cost ratios

## Explainability

- SHAP global (bar/beeswarm) and local (waterfall) plots
- Use insights to refine rules/thresholds and triage flows

## Risks & Mitigations

- Synthetic data bias → parameterized generator + multiple seeds
- Drift in production → monitor feature distributions
- Latency constraints → precompute heavy features, cache per-user states

## Next Steps

- Add device fingerprint risk score and ASN risk
- Time-windowed features (7/30-day)
- FastAPI scoring endpoint + Streamlit demo
