import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Load FIR dataset

df = pd.read_csv(
    "data/fir_dataset.csv"
)

# Columns assumed:
# text , crime_type

X = df["text"]
y = df["crime_type"]

# Train/Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# TF-IDF Vectorizer

vectorizer = TfidfVectorizer()

X_train_vec = vectorizer.fit_transform(X_train)

# Train Model

model = LogisticRegression()

model.fit(
    X_train_vec,
    y_train
)

# Save Model

pickle.dump(
    model,
    open("ml_models/fir_classifier.pkl", "wb")
)

pickle.dump(
    vectorizer,
    open("ml_models/vectorizer.pkl", "wb")
)

print("NLP Model Trained ✅")
