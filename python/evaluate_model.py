"""
Evaluates NexPath's Random Forest and writes data/model_metrics.json,
which model-performance.php reads.  Nothing here is hard-coded: every number
is computed from career_skill_prediction_250.csv when you run:

    python python/evaluate_model.py

Method: 5-fold STRATIFIED cross-validation (each fold keeps the same career mix).
Every student row is predicted exactly once by a model that never saw that row in training.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_recall_fscore_support)
from sklearn.model_selection import StratifiedKFold

BASE = Path(__file__).resolve().parent.parent
CSV = BASE / "career_skill_prediction_250.csv"
OUT = BASE / "data" / "model_metrics.json"

MODEL_PARAMS = dict(n_estimators=400, random_state=42, class_weight="balanced")  # same as predict.py
N_SPLITS, SEED = 5, 42

def main():
    df = pd.read_csv(CSV)
    X, y = df.drop(columns="Role"), df["Role"].astype(str)
    classes = sorted(y.unique())
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)

    y_true, y_pred, folds = [], [], []
    rng = np.random.default_rng(0)
    partial = {k: [] for k in (5, 10, 15, 25)}   # accuracy when only k skills are known
    for n, (tr, te) in enumerate(skf.split(X, y), start=1):
        model = RandomForestClassifier(**MODEL_PARAMS).fit(X.iloc[tr], y.iloc[tr])
        pred = model.predict(X.iloc[te])
        p, r, f, _ = precision_recall_fscore_support(y.iloc[te], pred, average="macro", zero_division=0)
        folds.append({"fold": n, "test_rows": int(len(te)), "accuracy": float(accuracy_score(y.iloc[te], pred)),
                      "precision": float(p), "recall": float(r), "f1": float(f)})
        y_true += list(y.iloc[te]); y_pred += list(pred)
        # Partial-profile check: hide skills, fill them with the training median (as predict.py does).
        med = X.iloc[tr].median().values
        for k in partial:
            rows = []
            for i in te:
                keep = rng.choice(X.shape[1], k, replace=False)
                v = med.copy(); v[keep] = X.iloc[i].values[keep]
                rows.append(v)
            hit = model.predict(pd.DataFrame(rows, columns=X.columns)) == y.iloc[te].values
            partial[k] += list(hit)

    acc = accuracy_score(y_true, y_pred)
    mp, mr, mf, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    wp, wr, wf, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)
    cp, cr, cf, cs = precision_recall_fscore_support(y_true, y_pred, labels=classes, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=classes)

    final = RandomForestClassifier(**MODEL_PARAMS).fit(X, y)
    imp = sorted(zip(X.columns, final.feature_importances_), key=lambda t: -t[1])

    metrics = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "algorithm": "Random Forest Classifier",
        "model_params": MODEL_PARAMS,
        "sklearn_version": sklearn.__version__,
        "dataset": {"file": CSV.name, "rows": int(len(df)), "features": list(X.columns),
                    "classes": classes, "rows_per_class": {c: int((y == c).sum()) for c in classes}},
        "evaluation": {"method": f"{N_SPLITS}-Fold Stratified Cross Validation", "n_splits": N_SPLITS,
                       "shuffle": True, "random_state": SEED},
        "overall": {"accuracy": float(acc),
                    "macro": {"precision": float(mp), "recall": float(mr), "f1": float(mf)},
                    "weighted": {"precision": float(wp), "recall": float(wr), "f1": float(wf)},
                    "fold_accuracy_mean": float(np.mean([f["accuracy"] for f in folds])),
                    "fold_accuracy_std": float(np.std([f["accuracy"] for f in folds]))},
        "folds": folds,
        "per_class": [{"career": c, "precision": float(cp[i]), "recall": float(cr[i]),
                       "f1": float(cf[i]), "support": int(cs[i])} for i, c in enumerate(classes)],
        "confusion_matrix": {"labels": classes, "matrix": cm.tolist()},
        "feature_importance": [{"skill": s, "importance": float(v)} for s, v in imp],
        "partial_profile_accuracy": [{"skills_known": k, "accuracy": float(np.mean(v))} for k, v in partial.items()],
    }
    OUT.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(f"Accuracy {acc:.3f} | macro P {mp:.3f} R {mr:.3f} F1 {mf:.3f}")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
