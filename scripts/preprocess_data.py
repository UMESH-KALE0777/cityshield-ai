# scripts/preprocess_data.py
import os
import sys
import django
import pandas as pd

# ── Django setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

RAW_DIR = os.path.join(settings.BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(settings.BASE_DIR, 'data', 'processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_raw(filename='crime_dataset.csv'):
    path = os.path.join(RAW_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"\n❌  Could not find: {path}"
            f"\n    Put your CSV in:  data/raw/crime_dataset.csv"
        )
    return pd.read_csv(path)


def normalise_columns(df):
    """
    Map whatever your CSV headers are to our standard names.
    Add/adjust mappings below to match your actual column names.
    """
    rename_map = {}
    col_lower = {c.lower(): c for c in df.columns}

    checks = {
        'crime_type':  ['crime_type', 'crime type', 'crimetype', 'offence', 'offense',
                        'crime description', 'crime_description', 'type', 'primary type'],
        'latitude':    ['latitude', 'lat'],
        'longitude':   ['longitude', 'lon', 'long', 'lng'],
        'area':        ['area', 'district', 'zone', 'locality', 'location',
                        'neighborhood', 'neighbourhood', 'city', 'occurrence city'],
        'date':        ['date', 'incident_date', 'crime_date', 'date of occurrence', 'date reported'],
        'time':        ['time', 'incident_time', 'crime_time', 'time of occurrence'],
        'description': ['description', 'fir_text', 'fir text', 'details',
                        'complaint', 'narrative'],
    }

    for standard, candidates in checks.items():
        for c in candidates:
            if c in col_lower:
                rename_map[col_lower[c]] = standard
                break

    df = df.rename(columns=rename_map)
    
    # Generate dummy coordinates for Bangalore if missing
    import numpy as np
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        print("⚠️  Latitude/Longitude missing. Generating dummy coordinates for Bangalore.")
        df['latitude'] = 12.9716 + np.random.uniform(-0.05, 0.05, size=len(df))
        df['longitude'] = 77.5946 + np.random.uniform(-0.05, 0.05, size=len(df))

    print("✅  Columns mapped:", list(df.columns))
    return df


def clean(df):
    # Drop rows where both lat and lon are missing
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df = df.dropna(subset=['latitude', 'longitude'])
        # Filter to Bangalore bounding box (roughly)
        df = df[
            df['latitude'].between(12.7, 13.2) &
            df['longitude'].between(77.3, 77.8)
        ]

    # Fill remaining nulls
    if 'crime_type' in df.columns:
        df['crime_type'] = df['crime_type'].fillna('Unknown').str.strip().str.title()
    if 'area' in df.columns:
        df['area'] = df['area'].fillna('Unknown').str.strip().str.title()
    if 'description' in df.columns:
        df['description'] = df['description'].fillna('')

    df = df.reset_index(drop=True)
    print(f"✅  Cleaned dataset: {len(df)} rows")
    return df


def save(df):
    out = os.path.join(PROCESSED_DIR, 'cleaned_crime_data.csv')
    df.to_csv(out, index=False)
    print(f"✅  Saved to: {out}")
    return df


def run():
    print("\n── Preprocessing ──────────────────────────────")
    df = load_raw()
    df = normalise_columns(df)
    df = clean(df)
    save(df)
    print("── Done ────────────────────────────────────────\n")
    return df


if __name__ == '__main__':
    run()
