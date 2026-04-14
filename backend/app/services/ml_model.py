

import joblib
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# ======================
# LOAD MODELS
# ======================
vectorizer = joblib.load(os.path.join(BASE_DIR, "ml_models/vectorizer.pkl"))
score_model = joblib.load(os.path.join(BASE_DIR, "ml_models/score_model.pkl"))
complexity_model = joblib.load(os.path.join(BASE_DIR, "ml_models/complexity_model.pkl"))

# 🔥 TEXT MODEL (LABEL)
text_vectorizer = joblib.load(os.path.join(BASE_DIR, "ml_models/vectorizer_text.pkl"))
text_model = joblib.load(os.path.join(BASE_DIR, "ml_models/text_model.pkl"))

# ======================
# SCORE + COMPLEXITY
# ======================
def predict_code_metrics(code: str):
    try:
        X = vectorizer.transform([code])

        score = score_model.predict(X)[0]
        complexity = complexity_model.predict(X)[0]

        return {
            "score": float(score),
            "complexity": str(complexity)
        }

    except Exception as e:
        print("METRIC ERROR:", e)
        return {
            "score": 0,
            "complexity": "unknown"
        }

# ======================
# LABEL
# ======================
def predict_text_issue(code: str):
    try:
        X = text_vectorizer.transform([code])  # ✅ IMPORTANT

        label = text_model.predict(X)[0]

        return {
            "label": str(label)
        }

    except Exception as e:
        print("LABEL ERROR:", e)
        return {
            "label": "unknown"
        }