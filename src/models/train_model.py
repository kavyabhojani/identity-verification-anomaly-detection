import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve, auc
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data"
IMAGES = BASE / "images"
REPORTS = BASE / "reports"
IMAGES.mkdir(exist_ok=True, parents=True)
REPORTS.mkdir(exist_ok=True, parents=True)

RANDOM_SEED = 42

def load_data():
    df = pd.read_parquet(DATA / "features.parquet")
    df = df.dropna()
    features = ["user_unique_devices_to_date","secs_since_prev_login","is_geo_mismatch","logins_last_24h"]
    X = df[features].copy()
    y = df["label"].astype(int).copy()
    return df, X, y, features

def plot_pr_curve(y_true, scores, title, out_png):
    precision, recall, _ = precision_recall_curve(y_true, scores)
    pr_auc = auc(recall, precision)
    plt.figure()
    plt.plot(recall, precision, label=f"PR AUC={pr_auc:.3f}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()

def main():
    df, X, y, features = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    logreg = LogisticRegression(max_iter=200, class_weight="balanced", random_state=RANDOM_SEED)
    logreg.fit(X_train_s, y_train)
    y_proba_lr = logreg.predict_proba(X_test_s)[:,1]
    auc_lr = roc_auc_score(y_test, y_proba_lr)

    xgb_clf = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_lambda=1.0,
        random_state=RANDOM_SEED,
        eval_metric="auc"
    )
    xgb_clf.fit(X_train, y_train)
    y_proba_xgb = xgb_clf.predict_proba(X_test)[:,1]
    auc_xgb = roc_auc_score(y_test, y_proba_xgb)

    joblib.dump({"scaler": scaler, "model": logreg, "features": features}, BASE / "logreg_model.joblib")
    joblib.dump({"model": xgb_clf, "features": features}, BASE / "xgb_model.joblib")

    with open(REPORTS / "model_report.txt", "w") as f:
        print("Logistic Regression AUC:", auc_lr, file=f)
        print("XGBoost AUC:", auc_xgb, file=f)
        f.write("\n=== Classification Report (XGBoost, 0.5 threshold) ===\n")
        y_pred_xgb = (y_proba_xgb >= 0.5).astype(int)
        f.write(classification_report(y_test, y_pred_xgb))

    plot_pr_curve(y_test, y_proba_lr, "Precision-Recall (LogReg)", IMAGES / "pr_logreg.png")
    plot_pr_curve(y_test, y_proba_xgb, "Precision-Recall (XGBoost)", IMAGES / "pr_xgb.png")

    print(f"Saved models and reports to {BASE}")

if __name__ == "__main__":
    main()
