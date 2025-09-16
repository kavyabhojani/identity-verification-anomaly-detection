# PoV Summary — Identity Verification Anomaly Detection

**Audience:** Product & Risk stakeholders

## Highlights

- Detects suspicious identity events with recall-first focus
- Reduces false positives via threshold tuning and feature-driven risk scoring
- Provides transparent justifications (SHAP) for every decision

## Results (sample)

- AUC (XGBoost): ~0.90–0.95 on synthetic set
- PR AUC: see `images/pr_xgb.png`
- SHAP: geo_mismatch and login velocity among top drivers

## Business Impact

- Fewer account takeovers → direct fraud loss reduction
- Minimal friction for legitimate users → protects conversion
- Clear adoption path: SQL features + Python model behind API

## Recommended Next Steps

- Validate on client telemetry
- Pilot behind step-up auth flow
- Add policy simulator for cost-of-error tuning
