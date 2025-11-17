import os
from pathlib import Path

import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import IsolationForest

from xgboost import XGBClassifier


def get_engine():
    """Create a SQLAlchemy engine from DATABASE_URL."""
    load_dotenv()
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://app:app@localhost:5433/frauddb",
    )
    print(f"Using DATABASE_URL = {db_url}")
    return create_engine(db_url)


def load_features(engine):
    """
    Load feature rows from mart.transactions_enriched.

    We keep it generic:
      - pull the whole table
      - keep only numeric columns
      - treat 'label' as target
    """
    sql = """
        SELECT *
        FROM mart.transactions_enriched
    """
    print("Running query to load features...")
    df = pd.read_sql(sql, engine)
    print(f"Loaded {len(df):,} rows, {len(df.columns)} columns")

    # Only numeric columns to avoid strings/emails/etc.
    df_num = df.select_dtypes(include=["number"]).copy()
    print(f"Numeric columns: {list(df_num.columns)}")

    if "label" not in df_num.columns:
        raise ValueError("Expected a numeric 'label' column in mart.transactions_enriched")

    # Target
    y = df_num["label"].astype(int)

    # Features: drop label + txn_id if present
    X = df_num.drop(columns=["label", "txn_id"], errors="ignore")

    print(f"Final feature matrix shape: {X.shape}")
    return X, y


def train_xgboost_classifier(X, y):
    """Train a simple XGBoost classifier and print metrics."""
    print("\n=== Training XGBoost classifier (supervised) ===")

    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Basic, sensible defaults for tabular data
    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="binary:logistic",
        tree_method="hist",  # fast on CPU
        eval_metric="logloss",
        n_jobs=-1,
        random_state=42,
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_valid)
    y_proba = model.predict_proba(X_valid)[:, 1]

    print("\nClassification report:")
    print(classification_report(y_valid, y_pred, digits=3))

    auc = roc_auc_score(y_valid, y_proba)
    print(f"Validation ROC-AUC: {auc:.4f}")

    return model


def train_isolation_forest(X):
    """
    Train an IsolationForest as an unsupervised anomaly detector.

    Note: this ignores labels and just learns 'what looks normal'.
    """
    print("\n=== Training IsolationForest (unsupervised) ===")

    iso = IsolationForest(
        n_estimators=200,
        max_samples="auto",
        contamination="auto",
        random_state=42,
        n_jobs=-1,
    )
    iso.fit(X)

    # IsolationForest's score_sample gives anomaly scores:
    #   lower = more anomalous
    scores = iso.score_samples(X)
    print(f"IsolationForest fitted. Example scores (first 5): {scores[:5]}")

    return iso


def main():
    project_root = Path(__file__).resolve().parents[1]
    models_dir = project_root / "models"
    models_dir.mkdir(exist_ok=True)

    engine = get_engine()
    X, y = load_features(engine)

    # --- Supervised model: XGBoost ---
    xgb_model = train_xgboost_classifier(X, y)
    xgb_path = models_dir / "xgb_classifier.joblib"
    joblib.dump(xgb_model, xgb_path)
    print(f"\nSaved XGBoost model to {xgb_path}")

    # --- Unsupervised model: IsolationForest ---
    iso_model = train_isolation_forest(X)
    iso_path = models_dir / "isolation_forest.joblib"
    joblib.dump(iso_model, iso_path)
    print(f"Saved IsolationForest model to {iso_path}")

    print("\nAll models trained and saved. ✅")


if __name__ == "__main__":
    main()
