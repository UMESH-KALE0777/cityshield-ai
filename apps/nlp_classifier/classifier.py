# apps/nlp_classifier/classifier.py
# Standalone helper (not used by views.py — views loads models directly).
# Kept for notebook/script use only.
import os
import pickle
from django.conf import settings

MODEL_PATH      = os.path.join(settings.BASE_DIR, 'ml_models', 'fir_classifier.pkl')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'vectorizer.pkl')


def predict_crime(text: str) -> str:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    return model.predict(vectorizer.transform([text]))[0]
