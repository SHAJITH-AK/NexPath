import json, sys
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

BASE = Path(__file__).resolve().parent.parent
CSV = BASE / "career_skill_prediction_250.csv"

# Keep these identical in evaluate_model.py so the reported metrics describe the model used here.
MODEL_PARAMS = dict(n_estimators=400, random_state=42, class_weight="balanced")
TOP_N = 4  # primary career + 3 alternatives

def main():
    if len(sys.argv) != 2:
        raise ValueError("Prediction input file was not supplied.")
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        payload = json.load(f)
    df = pd.read_csv(CSV)
    target = "Role"
    features = list(df.columns)
    if target not in features:
        raise ValueError("Dataset target column 'Role' was not found.")
    features.remove(target)
    incoming = payload.get("features", {})
    missing = [c for c in features if c not in incoming]
    if missing:
        raise ValueError("Missing model features: " + ", ".join(missing))

    X = df[features]
    y = df[target].astype(str)
    # Random Forest needs a value for every feature. A skill the student has NOT assessed
    # is sent as null and is filled with that skill's median score in the training data
    # (a neutral value), instead of pretending the student scored 1/10.
    medians = X.median()
    row, imputed = [], []
    for c in features:
        value = incoming[c]
        if value is None:
            row.append(float(medians[c]))
            imputed.append(c)
            continue
        value = float(value)
        if not 1 <= value <= 10:
            raise ValueError(f"Invalid value for {c}: expected 1-10 after score conversion.")
        row.append(value)

    model = RandomForestClassifier(**MODEL_PARAMS)
    model.fit(X, y)
    input_df = pd.DataFrame([row], columns=features)
    proba = model.predict_proba(input_df)[0]
    ranked = sorted(zip(model.classes_, proba), key=lambda p: (-p[1], p[0]))
    top = [{"role": str(r), "score": round(float(p) * 100, 1)} for r, p in ranked[:TOP_N]]
    print(json.dumps({
        "success": True,
        "role": top[0]["role"],
        "confidence": float(ranked[0][1] * 100),
        "top": top,
        "model": "Random Forest",
        "n_trees": MODEL_PARAMS["n_estimators"],
        "n_features": len(features),
        "n_assessed": len(features) - len(imputed),
        "imputed": imputed,
    }))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}))
