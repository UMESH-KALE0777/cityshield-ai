# scripts/load_data.py
import os
import sys
import django
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from apps.crime_hotspot.models import CrimeRecord
from apps.sos_system.models import PoliceStation

PROCESSED_CSV  = os.path.join(settings.BASE_DIR, 'data', 'processed', 'cleaned_crime_data.csv')
STATIONS_CSV   = os.path.join(settings.BASE_DIR, 'data', 'raw', 'police_stations.csv')


def load_crime_data():
    if not os.path.exists(PROCESSED_CSV):
        print("❌  Run preprocess_data.py first to generate cleaned_crime_data.csv")
        return

    df = pd.read_csv(PROCESSED_CSV)
    print(f"Loading {len(df)} crime records...")

    # Clear existing records to avoid duplicates on re-run
    CrimeRecord.objects.all().delete()

    records = []
    for _, row in df.iterrows():
        raw_date = row.get('date')
        raw_time = row.get('time')
        parsed_date = None
        parsed_time = None
        
        if pd.notna(raw_date):
            try:
                parsed_date = pd.to_datetime(raw_date).date().isoformat()
            except:
                parsed_date = None
        
        if pd.notna(raw_time):
            try:
                parsed_time = pd.to_datetime(raw_time).time().isoformat()
            except:
                parsed_time = None

        records.append(CrimeRecord(
            crime_type=str(row.get('crime_type', 'Unknown')),
            latitude=float(row['latitude']),
            longitude=float(row['longitude']),
            area=str(row.get('area', 'Unknown')),
            date=parsed_date,
            time=parsed_time,
        ))

    CrimeRecord.objects.bulk_create(records, batch_size=5000)
    print(f"✅  {CrimeRecord.objects.count()} crime records loaded into DB.")


def load_police_data():
    if not os.path.exists(STATIONS_CSV):
        print(f"❌  police_stations.csv not found at: {STATIONS_CSV}")
        return

    df = pd.read_csv(STATIONS_CSV)
    print(f"Loading {len(df)} police stations...")

    PoliceStation.objects.all().delete()

    stations = []
    for _, row in df.iterrows():
        stations.append(PoliceStation(
            name=row['name'],
            latitude=float(row['latitude']),
            longitude=float(row['longitude']),
            address=str(row.get('address', '')),
        ))

    PoliceStation.objects.bulk_create(stations, batch_size=1000)
    print(f"✅  {PoliceStation.objects.count()} police stations loaded.")


if __name__ == '__main__':
    load_crime_data()
    load_police_data()
