# scripts/train_models.py
import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()
from django.conf import settings

PROCESSED_DIR = os.path.join(settings.BASE_DIR, 'data', 'processed')
ML_DIR = os.path.join(settings.BASE_DIR, 'ml_models')
os.makedirs(ML_DIR, exist_ok=True)

CLEANED_CSV = os.path.join(PROCESSED_DIR, 'cleaned_crime_data.csv')


# ── Forecast model ────────────────────────────────────────────────────────────
def train_forecast_model(df):
    """
    Predicts future crime count per area using a simple Linear Regression
    on (area_encoded, month) → crime_count.
    Falls back to a frequency-based lookup if date column is absent.
    """
    print("\n── Training forecast model ─────────────────────")

    area_counts = df['area'].value_counts().reset_index()
    area_counts.columns = ['area', 'crime_count']

    le = LabelEncoder()
    area_counts['area_encoded'] = le.fit_transform(area_counts['area'])

    # Use crime count as both feature (rank) and noisy target for regression
    X = area_counts[['area_encoded']].values
    y = area_counts['crime_count'].values

    model = LinearRegression()
    model.fit(X, y)

    # Save everything the view needs
    payload = {
        'model': model,
        'label_encoder': le,
        'area_counts': area_counts,   # used as fast lookup fallback
    }

    out = os.path.join(ML_DIR, 'forecast_model.pkl')
    joblib.dump(payload, out)
    print(f"✅  Forecast model saved → {out}")
    print(f"    Areas in model: {len(le.classes_)}")
    return payload


# ── Hotspot clustering model ──────────────────────────────────────────────────
def train_hotspot_model(df):
    """
    KMeans clustering on (latitude, longitude) to identify crime hotspot zones.
    Saves cluster centres and the fitted model.
    """
    print("\n── Training hotspot model ──────────────────────")

    coords = df[['latitude', 'longitude']].dropna().values

    # Pick k: one cluster per ~200 crimes, between 5 and 20
    k = max(5, min(20, len(coords) // 200))
    print(f"    Using k={k} clusters for {len(coords)} crime points")

    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(coords)

    payload = {
        'model': km,
        'cluster_centers': km.cluster_centers_,   # shape (k, 2)
        'k': k,
    }

    out = os.path.join(ML_DIR, 'hotspot_model.pkl')
    joblib.dump(payload, out)
    print(f"✅  Hotspot model saved → {out}")
    print(f"    Cluster centres (lat, lon):")
    for i, c in enumerate(km.cluster_centers_):
        print(f"      Cluster {i}: ({c[0]:.4f}, {c[1]:.4f})")
    return payload


# ── Cluster feature CSV (optional, used by safe_route) ───────────────────────
def save_clustered_data(df, hotspot_payload):
    km = hotspot_payload['model']
    coords = df[['latitude', 'longitude']].dropna()
    df_clean = df.loc[coords.index].copy()
    df_clean['cluster'] = km.predict(coords.values)
    out = os.path.join(PROCESSED_DIR, 'clustered_data.csv')
    df_clean.to_csv(out, index=False)
    print(f"\n✅  Clustered data saved → {out}")


def run():
    if not os.path.exists(CLEANED_CSV):
        print("❌  Run preprocess_data.py first.")
        sys.exit(1)

    df = pd.read_csv(CLEANED_CSV)
    print(f"Loaded {len(df)} rows from cleaned data.")

    forecast_payload = train_forecast_model(df)
    hotspot_payload  = train_hotspot_model(df)
    save_clustered_data(df, hotspot_payload)

    print("\n🎉  All models trained and saved.\n")


if __name__ == '__main__':
    run()
