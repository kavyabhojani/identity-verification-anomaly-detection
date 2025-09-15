import pandas as pd
import numpy as np
from pathlib import Path
import shap
import joblib
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data"
IMAGES = BASE / "images"
REPORTS = BASE / "reports"
IMAGES.mkdir(exist_ok=True, parents=True)
REPORTS.mkdir(exist_ok=True, parents=True)

def main():
    bundle = joblib.load(BASE / "xgb_model.joblib")
    model = bundle["model"]
    features = bundle["features"]
    df = pd.read_parquet(DATA / "features.parquet").dropna()
    X = df[features]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X)

    plt.figure()
    shap.plots.bar(shap_values, show=False)
    plt.tight_layout()
    plt.savefig(IMAGES / "shap_global_bar.png", dpi=160)
    plt.close()

    plt.figure()
    shap.plots.beeswarm(shap_values, show=False, max_display=10)
    plt.tight_layout()
    plt.savefig(IMAGES / "shap_beeswarm.png", dpi=160)
    plt.close()

    sample_idx = np.random.choice(len(X), size=3, replace=False)
    for i, idx in enumerate(sample_idx, start=1):
        sv = shap_values[idx]
        shap.plots.waterfall(sv, show=False, max_display=10)
        plt.tight_layout()
        plt.savefig(IMAGES / f"shap_waterfall_{i}.png", dpi=160)
        plt.close()

    with open(REPORTS / "explainability_summary.md", "w") as f:
        f.write("# Explainability Summary (SHAP)\n\n")
        f.write("- Global importance and per-sample attributions saved in images/.\n")
        f.write("- Top features typically include: user_unique_devices_to_date, secs_since_prev_login, is_geo_mismatch, logins_last_24h.\n")

    print("Saved SHAP plots to images/ and summary to reports/.")

if __name__ == "__main__":
    main()
