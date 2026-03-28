import pickle
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'fir_classifier.pkl')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'vectorizer.pkl')

# Load BOTH the vectorizer and the classifier
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
except Exception as e:
    print(f"Model loading error: {e}")
    model = None
    vectorizer = None


@login_required
def classifier_dashboard(request):
    prediction = None
    confidence = None
    fir_text = ''

    if request.method == 'POST':
        fir_text = request.POST.get('fir_text', '').strip()

        if model and vectorizer and fir_text:
            try:
                # Vectorize the raw text first, then predict
                X = vectorizer.transform([fir_text])
                prediction = model.predict(X)[0]

                # Show confidence probabilities if available
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(X)[0]
                    confidence = round(max(proba) * 100, 1)

            except Exception as e:
                print(f"Prediction error: {e}")
                prediction = "Classification error — check model files."
        elif not fir_text:
            messages.warning(request, "Please enter a complaint description.")

    return render(request, 'nlp_classifier/classifier.html', {
        'prediction': prediction,
        'confidence': confidence,
        'fir_text': fir_text,
    })
